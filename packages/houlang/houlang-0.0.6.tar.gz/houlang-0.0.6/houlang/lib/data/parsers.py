import re
import logging
import pathlib

import numpy as np
from lxml import etree

from houlang.lib.data.annotations import Layout, LayoutObject

class AltoParser(object):

    def __init__(self, path):
        self.path = path
        self.doc = self._parse_alto(self.path)
        self.float_pattern = re.compile(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
        self._is_valid()

    def _is_valid(self):
        # Check if the file is an ALTO file
        root_el_tag = self.doc.getroot().tag
        assert root_el_tag.endswith('alto'), f"{self.path} file is not an ALTO file."
        
    def _parse_alto(self, path):
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.parse(str(path), parser=parser)

    def _parse_alto_pointstype(self, coords):
        points = [float(point.group()) for point in self.float_pattern.finditer(coords)]
        points = zip(points[::2], points[1::2])
        return np.array(list(points)).astype(np.int32)
        
    def to_annotations(self):

        annotations = Layout()

        # Parse Tags
        id_to_label = {}
        for el in self.doc.find('.//{*}Tags'):
            id_to_label[el.get('ID')] = el.get('LABEL')

        # # find all regions
        # for el in self.doc.iterfind('./{*}Layout/{*}Page/{*}PrintSpace/{*}*'):
        #     for region in ['TextBlock', 'Illustration', 'GraphicalElement', 'ComposedBlock']:
        #         if el.tag.endswith(region):
        #             try:
        #                 # parse region boundary
        #                 coords = el.find('./{*}Shape/{*}Polygon')
        #                 if coords is not None and coords.get('POINTS') is not None:
        #                     boundary = self._parse_alto_pointstype(coords.get('POINTS'))
        #                 # if no polygon is given, try to parse rectangle
        #                 elif (el.get('HPOS') is not None and el.get('VPOS') is not None and
        #                         el.get('WIDTH') is not None and el.get('HEIGHT') is not None):
        #                     x_min = int(float(el.get('HPOS')))
        #                     y_min = int(float(el.get('VPOS')))
        #                     width = int(float(el.get('WIDTH')))
        #                     height = int(float(el.get('HEIGHT')))
        #                     boundary = [(x_min, y_min),
        #                                 (x_min, y_min + height),
        #                                 (x_min + width, y_min + height),
        #                                 (x_min + width, y_min)]
        #                 # if no polygon or rectangle is given, skip region
        #                 else:
        #                     raise Exception('Region has no boundary')

        #                 # parse region id
        #                 id = el.get('ID')

        #                 # parse region type
        #                 tagrefs = el.get('TAGREFS')                    
        #                 if tagrefs is None:
        #                     raise Exception('Region has no tagrefs attribute')

        #                 label = id_to_label.get(tagrefs)
        #                 if label is None:
        #                     raise Exception('Unknown tagrefs')

        #                 # create region and add it to annotations object
        #                 region_object = LayoutObject(boundary, label=label, type='region', id=id)
        #                 annotations.add_object(region)

        #             except Exception as e:
        #                 # if self.strict:
        #                 #     raise e
        #                 # else:
        #                 logging.debug(f"Failed to parse region {el.get('ID')} from {self.path}: {e}")
        #                 continue

        #             break

        # parse lines
        for el in self.doc.iterfind('.//{*}TextLine'):
            try:
                # parse boundary
                coords = el.find('./{*}Shape/{*}Polygon')
                if coords is not None and coords.get('POINTS') is not None:
                    boundary = self._parse_alto_pointstype(coords.get('POINTS'))
                else:
                    raise Exception('Line has no boundary')

                # parse region id
                id = el.get('ID')

                # parse region type
                tagrefs = el.get('TAGREFS')                    
                if tagrefs is None:
                    label = 'default'
                else:
                    label = id_to_label.get(tagrefs)
                    if label is None:
                        breakpoint()
                        raise Exception('Unknown tagrefs')
                
                # parse text
                string = el.find('./{*}String')
                if string is not None:
                    text = string.get('CONTENT')
                else:
                    text = None

                # create region
                line_object = LayoutObject(boundary, id=id, label=label, text=text, type='line')
                annotations.add_object(line_object)

            except Exception as e:
                # if self.strict:
                #     raise e
                # else:
                logging.debug(f"Failed to parse line {el.get('ID')} from {self.path}: {e}")
                continue

        return annotations