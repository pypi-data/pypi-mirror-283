import pathlib

from kraken.lib import models
from kraken import rpred
from PIL import Image

class KrakenRecognizer:
    DEFAULT_MODEL = 'meltingpot.mlmodel'

    def __init__(self, model_path=None):
        self.model, self.model_path = self._load_model(model_path)
        self.vocab = [label for label in self.model.codec.c2l.keys()]

    def _load_model(self, model_path):

        if isinstance(model_path, str):
            model_path = pathlib.Path(model_path)
        elif isinstance(model_path, pathlib.Path):
            model_path = model_path
        elif model_path is None:
            model_path = pathlib.Path(__file__).parent / self.DEFAULT_MODEL
        else:
            raise ValueError('model_path must be a string or pathlib.Path object')
        
        if not model_path.exists():
            raise FileNotFoundError(f'{model_path} does not exist')

        model = models.load_any(str(model_path))

        return model, model_path

    def recognise(self, doc_img, verbose=False):
        pil_img = Image.fromarray(doc_img.img)
        baseline_seg = doc_img.annotations.to_baselineseg()
        pred_it = rpred.rpred(self.model, pil_img, baseline_seg)
        text_buffer = []
        for record in pred_it:
            if verbose:
                print(record.prediction)
            text_buffer.append(record.prediction)
        return '\n'.join(text_buffer)

    def __repr__(self):
        return f'KrakenRecognizer(model_path={self.model_path.name}, vocab={len(self.vocab)})'

    def __call__(self, doc_img, verbose=False):
        return self.recognise(doc_img, verbose)
    
if __name__ == '__main__':

    kr = KrakenRecognizer()