import uuid
import logging
import dataclasses

import cv2
import numpy as np

@dataclasses.dataclass
class Layout:
    object_l: list = dataclasses.field(default_factory=list)
    label_set: set = dataclasses.field(default_factory=set)
    

    @property
    def label_list(self):
        return [label for label in self.label_set]
    
    def __len__(self):
        return len(self.object_l)
    
    def add_object(self, object):
        assert isinstance(object, LayoutObject), 'Object must be an instance of LayoutObject.'
        self.label_set.add(object.label)
        self.object_l.append(object)

    
    def to_baselineseg(self):

        from shapely import geometry as geo
        from kraken.containers import BaselineLine, Segmentation

        baseline_line_l = []
        for object in self.object_l:
            polygon = geo.Polygon(object.boundary)
            xmin, ymin, xmax, ymax = polygon.bounds
            median_x = xmin + ((xmax - xmin) / 2)
            center_line = [(median_x, ymin), (median_x, ymax)]
            baseline_line = BaselineLine(id=object.id,
                                        baseline=center_line,
                                        boundary=object.boundary)
            baseline_line_l.append(baseline_line)

        baseline_seg = Segmentation(
            type='baselines',
            imagename='image.png',
            text_direction='vertical-rl',
            script_detection=False,
            lines=baseline_line_l
        )

        return baseline_seg

@dataclasses.dataclass
class LayoutObject:
    boundary: list
    label: str
    type: str
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    text: str = None
    direction: str = None
