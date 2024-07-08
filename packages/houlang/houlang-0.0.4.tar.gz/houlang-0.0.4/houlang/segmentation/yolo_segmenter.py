import copy
import math
import pathlib
import logging

import cv2
import torch
import ultralytics
import numpy as np

from houlang.lib.data.images import DocumentImage
from houlang.lib.data.annotations import Layout, LayoutObject

class YoloInferenceDataset(torch.utils.data.Dataset):

    def __init__(self, img_l, imgsz):
        self.img_l = self._check_img_l(img_l)
        self.imgsz = imgsz
    
    def _check_img_l(self, img_l):
        if isinstance(img_l, DocumentImage) or isinstance(img_l, str) or isinstance(img_l, pathlib.Path):
            img_l = [img_l]

        for img_idx, img in enumerate(img_l):
            if not isinstance(img, str) and not isinstance(img, pathlib.Path) and not isinstance(img, DocumentImage):
                raise ValueError(f'img must be a string, pathlib.Path, or DocumentImage object, got: {type(img)}')
        return img_l
    
    def _load_img(self, idx):
        img = self.img_l[idx]
        if isinstance(img, str) or isinstance(img, pathlib.Path):
            doc_img = DocumentImage(img)
        elif isinstance(img, DocumentImage):
            doc_img = img
        else:
            raise ValueError('img must be a string, pathlib.Path, or DocumentImage object')
        return doc_img
    
    def __len__(self):
        return len(self.img_l)
    
    def __getitem__(self, idx):
        doc_img = self._load_img(idx)
        im = copy.deepcopy(doc_img.img)
        h0, w0 = im.shape[:2]
        r = self.imgsz / max(h0, w0)
        w, h = (min(math.ceil(w0 * r), self.imgsz), min(math.ceil(h0 * r), self.imgsz))
        im = cv2.resize(im, (w, h), interpolation=cv2.INTER_LINEAR)
        im_t = torch.from_numpy(im).permute(2, 0, 1).float().div(255.0)
        if im_t.shape[1] != self.imgsz or im_t.shape[2] != self.imgsz:
            pad_w = self.imgsz - im_t.shape[2]
            pad_h = self.imgsz - im_t.shape[1]
            im_t = torch.nn.functional.pad(im_t, (0, pad_w, 0, pad_h), mode='constant', value=0.5)
        return im_t, doc_img, r

class YOLOSegmenter(object):
    DEFAULT_MODEL_NAME = "yolov8n_lineseg.pt"

    def __init__(self, model_path=None):
        if model_path is None:
            self.model_path = self._get_default_model_path()
        elif isinstance(model_path, str):
            self.model_path = pathlib.Path(model_path)
        elif isinstance(model_path, pathlib.Path):
            self.model_path = model_path
        else:
            raise ValueError('model_path must be a string or pathlib.Path object')
        
        self.model = ultralytics.YOLO(self.model_path)
        self.imgsz = self._get_imgsz()

    def __repr__(self):
        return f"YOLOSegmenter(model={self.model_path.name}, image size={self.imgsz})"
    
    def __call__(self, img_l):
        return self.segment(img_l)

    def _get_default_model_path(self):
        return pathlib.Path(__file__).parent / self.DEFAULT_MODEL_NAME

    def _get_imgsz(self):
        state_dict = torch.load(self.model_path)
        return state_dict['train_args']['imgsz']
    
    def _post_processing(self, seg_result, doc_img, scaling_factor):
        annotations = Layout()
        for boxe in seg_result.boxes:
            xyxy = boxe.xyxy.tolist()[0]
            scaled_xmin = xyxy[0] / scaling_factor
            scaled_ymin = xyxy[1] / scaling_factor
            scaled_xmax = xyxy[2] / scaling_factor
            scaled_ymax = xyxy[3] / scaling_factor
            boundary = [[scaled_xmin, scaled_ymin], [scaled_xmax, scaled_ymin], [scaled_xmax, scaled_ymax], [scaled_xmin, scaled_ymax]]
            object = LayoutObject(boundary=boundary, label='line', type='line')
            annotations.add_object(object)
        doc_img.annotations = annotations
        return doc_img
    
    @staticmethod
    def _collate_fn(batch):
        im_t_l = []
        doc_img_l =  []
        scaling_factor_l = []
        for im_t, doc_img, scaling_factor in batch:
            im_t_l.append(im_t)
            doc_img_l.append(doc_img)
            scaling_factor_l.append(scaling_factor)
        return torch.stack(im_t_l), doc_img_l, scaling_factor_l
    
    def segment(self, img_l, device='cpu', batch_size=1, workers=1):
        dataset = YoloInferenceDataset(img_l, self.imgsz)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, num_workers=workers, collate_fn=self._collate_fn)
        annotated_img_l = []
        with torch.no_grad():
            for batch_idx, (img_batch, doc_img_l, sacling_factor_l) in enumerate(dataloader):
                result_l = self.model.predict(img_batch, verbose=False, device=device)
                result_l = [result.cpu() for result in result_l]
                for result, doc_img, sacling_factor in zip(result_l, doc_img_l, sacling_factor_l):
                    annotated_img = self._post_processing(result, doc_img, sacling_factor)
                    annotated_img_l.append(annotated_img)
        return annotated_img_l
