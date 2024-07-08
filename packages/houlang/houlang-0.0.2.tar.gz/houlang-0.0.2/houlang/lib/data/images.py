import copy
import logging
import pathlib

import cv2
import numpy as np
from matplotlib import pyplot as plt

import houlang.lib.data.parsers as parsers
import houlang.lib.data.annotations as annotations


_COLORS = np.array(
    [
        0.000, 0.447, 0.741,
        0.850, 0.325, 0.098,
        0.929, 0.694, 0.125,
        0.494, 0.184, 0.556,
        0.466, 0.674, 0.188,
        0.301, 0.745, 0.933,
        0.635, 0.078, 0.184,
        0.300, 0.300, 0.300,
        0.600, 0.600, 0.600,
        1.000, 0.000, 0.000,
        1.000, 0.500, 0.000,
        0.749, 0.749, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 1.000,
        0.667, 0.000, 1.000,
        0.333, 0.333, 0.000,
        0.333, 0.667, 0.000,
        0.333, 1.000, 0.000,
        0.667, 0.333, 0.000,
        0.667, 0.667, 0.000,
        0.667, 1.000, 0.000,
        1.000, 0.333, 0.000,
        1.000, 0.667, 0.000,
        1.000, 1.000, 0.000,
        0.000, 0.333, 0.500,
        0.000, 0.667, 0.500,
        0.000, 1.000, 0.500,
        0.333, 0.000, 0.500,
        0.333, 0.333, 0.500,
        0.333, 0.667, 0.500,
        0.333, 1.000, 0.500,
        0.667, 0.000, 0.500,
        0.667, 0.333, 0.500,
        0.667, 0.667, 0.500,
        0.667, 1.000, 0.500,
        1.000, 0.000, 0.500,
        1.000, 0.333, 0.500,
        1.000, 0.667, 0.500,
        1.000, 1.000, 0.500,
        0.000, 0.333, 1.000,
        0.000, 0.667, 1.000,
        0.000, 1.000, 1.000,
        0.333, 0.000, 1.000,
        0.333, 0.333, 1.000,
        0.333, 0.667, 1.000,
        0.333, 1.000, 1.000,
        0.667, 0.000, 1.000,
        0.667, 0.333, 1.000,
        0.667, 0.667, 1.000,
        0.667, 1.000, 1.000,
        1.000, 0.000, 1.000,
        1.000, 0.333, 1.000,
        1.000, 0.667, 1.000,
        0.333, 0.000, 0.000,
        0.500, 0.000, 0.000,
        0.667, 0.000, 0.000,
        0.833, 0.000, 0.000,
        1.000, 0.000, 0.000,
        0.000, 0.167, 0.000,
        0.000, 0.333, 0.000,
        0.000, 0.500, 0.000,
        0.000, 0.667, 0.000,
        0.000, 0.833, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 0.167,
        0.000, 0.000, 0.333,
        0.000, 0.000, 0.500,
        0.000, 0.000, 0.667,
        0.000, 0.000, 0.833,
        0.000, 0.000, 1.000,
        0.000, 0.000, 0.000,
        0.143, 0.143, 0.143,
        0.857, 0.857, 0.857,
        1.000, 1.000, 1.000
    ]
).astype(np.float32).reshape(-1, 3)   

class DocumentImage(object):

    def __init__(self, arg):
        if isinstance(arg, str):
            self.path = pathlib.Path(arg)
        elif isinstance(arg, pathlib.Path):
            self.path = arg
        else:
            raise ValueError('arg must be a string or a pathlib.Path object')
        
        self.img = cv2.imread(str(self.path))
        self.type = self._get_type()
        self.height, self.width = self._get_image_dimensions()
        self.annotations = annotations.Layout()

    def __repr__(self):
        return f'DocumentImage(name:{self.path.name}, type:{self.type}, heigth:{self.height}, width:{self.width}, annotations:{len(self.annotations)})'

    def _get_type(self):
        if self.img.ndim == 3:
            return 'BGR'
        if self.img.ndim == 2:
            return 'BIN'
        raise ValueError('Image must have 2 or 3 dimensions')
    
    def _get_image_dimensions(self):
        return self.img.shape[:2]
    
    def save_img(self, path):
        cv2.imwrite(path, self.image)

    def plot(self):
        img = copy.deepcopy(self.img)

        if self.type == 'BIN':
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        if len(self.annotations) > 0:
            for label_idx, label in enumerate(self.annotations.label_list):
                overlay = img.copy()
                color = (_COLORS[label_idx] * 255).tolist()
                object_l = [object for object in self.annotations.object_l if object.label == label]
                boundary_l = [np.array(object.boundary, np.int32) for object in object_l]
                cv2.fillPoly(overlay, boundary_l, color)
                alpha = 0.2
                cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def load_annotations_from_alto(self, alto_path=None):
        if alto_path is None:
            alto_path = self.path.with_suffix('.xml')
        alto_parser = parsers.AltoParser(alto_path)
        self.annotations = alto_parser.to_annotations()
