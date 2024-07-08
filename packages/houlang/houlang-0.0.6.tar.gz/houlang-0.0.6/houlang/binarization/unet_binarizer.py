import logging
import pathlib

import cv2
import torch
import tqdm
import numpy as np
import scipy.signal
import torch.nn.functional as F

from houlang import DocumentImage

class UNet(torch.nn.Module):
    """Based on Milesi Alexandre implementation of the U-Net architecture from Ronneberger et al. (2015)."""

    def __init__(self, n_channels, n_classes):
        super().__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes

        self.inc = (DoubleConv(n_channels, 64))
        self.down1 = (Down(64, 128))
        self.down2 = (Down(128, 256))
        self.down3 = (Down(256, 512))
        self.down4 = (Down(512, 1024))
        self.up1 = (Up(1024, 512))
        self.up2 = (Up(512, 256))
        self.up3 = (Up(256, 128))
        self.up4 = (Up(128, 64))
        self.outc = (OutConv(64, n_classes))

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        output = self.outc(x)
        return torch.sigmoid(output)

class DoubleConv(torch.nn.Module):
    """(convolution => [BN] => ReLU) * 2"""

    def __init__(self, in_channels, out_channels, mid_channels=None):
        super().__init__()
        if not mid_channels:
            mid_channels = out_channels
        self.double_conv = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),
            torch.nn.BatchNorm2d(mid_channels),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1, bias=False),
            torch.nn.BatchNorm2d(out_channels),
            torch.nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.double_conv(x)


class Down(torch.nn.Module):
    """Downscaling with maxpool then double conv"""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.maxpool_conv = torch.nn.Sequential(
            torch.nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels)
        )

    def forward(self, x):
        return self.maxpool_conv(x)


class Up(torch.nn.Module):
    """Upscaling then double conv"""

    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.up = torch.nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)
        self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        diffY = x2.size()[2] - x1.size()[2]
        diffX = x2.size()[3] - x1.size()[3]
        x1 = F.pad(x1, [diffX // 2, diffX - diffX // 2,
                        diffY // 2, diffY - diffY // 2])
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class OutConv(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        return self.conv(x)

class UnetBinarizer(object):
    """A U-Net based binarizer."""

    def __init__(self, state_dict_path=None, **kwargs):
        self.model = None
        self.weights = None
        self.hparams = {
            'debug': True,
            'img_size': 224,
            'n_channels': 3,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'amp': True,
            'amp_dtype': torch.bfloat16,
            'batch_size': 8,
            'workers': 16,
            'learning_rate': 1e-3,
            'epoch_max': 100,
            'val_ratio': 0.1,
            'best_train_loss': float('inf'),
            'best_val_loss': float('inf'),
            'log_interval': 20,
        }

        self._load_state_dict(state_dict_path)

        self.hparams.update(kwargs)

        self._init_model()
        self.stride = self.hparams['img_size'] // 2
        self.model.eval()
        self.model.to(self.hparams['device'])
        self.wind_2d = self._window_2D(self.hparams['img_size']).to(self.hparams['device'])

    def _load_state_dict(self, state_dict_path):
        """Load weights and hyperparameters from state dict."""
        if state_dict_path is not None:
            state_dict_path = pathlib.Path(state_dict_path)
        else:
            state_dict_path = pathlib.Path(__file__).parent / 'binarization.pth'

        state_dict = torch.load(state_dict_path, map_location='cpu')
        self.weights = state_dict['weights']
        self.hparams = state_dict['hparams']
        logging.info(f'State dict loaded from {state_dict_path}')

    def _init_model(self):
        """Build the model."""
        self.model = UNet(n_channels=self.hparams['n_channels'], n_classes=1)
        if self.weights is not None:
            self.model.load_state_dict(self.weights, strict=False)

    def _load_image(self, img):
        if isinstance(img, str) or isinstance(img, pathlib.Path):
            doc_img = DocumentImage(img)
        elif isinstance(img, DocumentImage):
            doc_img = img
        else:
            raise ValueError('img must be a string, a pathlib.Path object or a DocumentImage object')

        if doc_img.type == 'BIN':
            raise ValueError('img must be a color image')
        
        return doc_img
    
    def _normalize_image(self, img):
        img = (255 - img) / 255
        return img
    
    def _pad_image(self, img):

        h, w = img.shape[:2]
        n_vertical_patches = (h - self.hparams['img_size']) / self.stride + 1
        n_horizontal_patches = (w - self.hparams['img_size']) / self.stride + 1

        if n_vertical_patches.is_integer():
            pad_vertical = self.stride
        else:
            n_vertical_patches = int(n_vertical_patches)
            pad_vertical = n_vertical_patches * self.stride + self.hparams['img_size'] - h + self.stride

        if n_horizontal_patches.is_integer():
            pad_horizontal = self.stride
        else:
            n_horizontal_patches = int(n_horizontal_patches)
            pad_horizontal = n_horizontal_patches * self.stride + self.hparams['img_size'] - w + self.stride

        left_pad = pad_horizontal // 2
        right_pad = pad_horizontal - left_pad
        top_pad = pad_vertical // 2
        bottom_pad = pad_vertical - top_pad

        padded_img = np.pad(img, ((top_pad, bottom_pad), (left_pad, right_pad), (0, 0)), mode='reflect')
        
        return padded_img, (left_pad, top_pad, right_pad, bottom_pad)
    
    def _unpad_image(self, img, pad):
        left_pad, top_pad, right_pad, bottom_pad = pad
        return img[top_pad:-bottom_pad, left_pad:-right_pad]
    
    def _augment_image(self, img):
        """ Use dihedral group D4 to augment the img (8 possibilities) """
        augmented_patch_l = []
        augmented_patch_l.append(img)
        augmented_patch_l.append(np.rot90(img, 1))
        augmented_patch_l.append(np.rot90(img, 2))
        augmented_patch_l.append(np.rot90(img, 3))
        augmented_patch_l.append(np.flipud(img))
        augmented_patch_l.append(np.fliplr(img))
        augmented_patch_l.append(np.flipud(np.rot90(img, 1)))
        augmented_patch_l.append(np.fliplr(np.rot90(img, 1)))
        return augmented_patch_l
    
    def _extract_patches(self, img_l):
        patch_l = []
        for img in img_l:
            h, w = img.shape[:2]
            for i in range(0, h - self.hparams['img_size'], self.stride):
                for j in range(0, w - self.hparams['img_size'], self.stride):
                    img_patch = img[i:i+self.hparams['img_size'], j:j+self.hparams['img_size']]
                    patch_l.append(img_patch)
        return patch_l
    
    def _reconstruct_images(self, pred_mask_l, augmente_img_l):

        bin_img_l = []
        mask_n_by_img = int(len(pred_mask_l) / len(augmente_img_l))
        for img_idx, mask_start_idx in enumerate(range(0, len(pred_mask_l), mask_n_by_img)):
            mask_l = pred_mask_l[mask_start_idx:mask_start_idx+mask_n_by_img]
            original_img = augmente_img_l[img_idx]
            h, w = original_img.shape[:2]
            bin_img = np.zeros((h, w), dtype=np.float32)
            mask_idx = 0
            for j in range(0, h - self.hparams['img_size'], self.stride):
                for k in range(0, w - self.hparams['img_size'], self.stride):
                    mask = mask_l[mask_idx]
                    bin_img[j:j+self.hparams['img_size'], k:k+self.hparams['img_size']] += mask
                    mask_idx += 1
            # bin_img = bin_img / (2 ** 2)
            bin_img_l.append(bin_img)

        bin_img_l[1] = np.rot90(bin_img_l[1], -1)
        bin_img_l[2] = np.rot90(bin_img_l[2], -2)
        bin_img_l[3] = np.rot90(bin_img_l[3], -3)
        bin_img_l[4] = np.flipud(bin_img_l[4])
        bin_img_l[5] = np.fliplr(bin_img_l[5])
        bin_img_l[6] = np.rot90(np.flipud(bin_img_l[6]), -1)
        bin_img_l[7] = np.rot90(np.fliplr(bin_img_l[7]), -1)
        
        bin_img = np.mean(bin_img_l, axis=0)

        return bin_img
    
    def _spline_window(self, window_size, power=2):
        """
        Squared spline (power=2) window function:
        """
        intersection = int(window_size/4)
        wind_outer = (abs(2*(scipy.signal.triang(window_size))) ** power)/2
        wind_outer[intersection:-intersection] = 0

        wind_inner = 1 - (abs(2*(scipy.signal.triang(window_size) - 1)) ** power)/2
        wind_inner[:intersection] = 0
        wind_inner[-intersection:] = 0

        wind = wind_inner + wind_outer
        wind = wind / np.average(wind)
        return wind

    def _window_2D(self, window_size, power=2):
        """
        Make a 1D window function, then infer and return a 2D window function.
        Done with an augmentation, and self multiplication with its transpose.
        Could be generalized to more dimensions.
        """
        wind = self._spline_window(window_size, power)
        wind_2d = np.outer(wind, wind)
        wind_2d_tensor = torch.tensor(wind_2d, dtype=torch.float32)
        return wind_2d_tensor
        
    def binarize(self, img, device='cpu', batch_size=1):
        doc_img = self._load_image(img)
        img = doc_img.img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        norm_img = self._normalize_image(img)
        padded_img, pad = self._pad_image(norm_img)
        augmented_img_l = self._augment_image(padded_img)
        augmented_img_patch_l = self._extract_patches(augmented_img_l)
        tensor_patch_l = [torch.tensor(patch.copy(), dtype=torch.float32, requires_grad=False).permute(2, 0, 1) for patch in augmented_img_patch_l]

        pred_mask_l = []
        for i in tqdm.tqdm(range(0, len(tensor_patch_l), batch_size)):
            with torch.no_grad():
                batch = torch.stack(tensor_patch_l[i:i+batch_size], dim=0)
                batch = batch.to(self.hparams['device'])
                pred_mask = self.model(batch)
                pred_mask = pred_mask * self.wind_2d
                pred_mask = pred_mask.to('cpu').numpy()
                pred_mask_l.extend([mask.squeeze() for mask in pred_mask])

        bin_img = self._reconstruct_images(pred_mask_l, augmented_img_l)
        bin_img = self._unpad_image(bin_img, pad)
        bin_img = np.clip(255 * bin_img, 0, 255).astype(np.uint8)
        bin_img = 255 - bin_img

        bin_img =  cv2.adaptiveThreshold(bin_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        doc_img.img = bin_img
        doc_img.type = 'BIN'
        return doc_img

    def __call__(self, img, **kwargs):
        return self.binarize(img, **kwargs)