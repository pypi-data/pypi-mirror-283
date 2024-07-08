import numpy as np
from sklearn.cluster import DBSCAN
from shapely import geometry as geo

from houlang import DocumentImage
from houlang.lib.data.annotations import Layout

class HeuristicReadingOrderClassifier():

    def __init__(self, x_axis_overlap_threshold=0.5, y_axis_overlap_threshold=0.5):
        self.x_axis_overlap_threshold = x_axis_overlap_threshold
        self.y_axis_overlap_threshold = y_axis_overlap_threshold

    def order_lines(self, doc_img, sort_region=False):

        if not isinstance(doc_img, DocumentImage):
            raise ValueError('doc_img must be a DocumentImage object')

        if len(doc_img.annotations) == 0:
            raise ValueError('DocumentImage must have annotations to order layout objects')
        
        object_l = doc_img.annotations.object_l

        if sort_region:
            object_region_label_l, sorted_region_label_l = self.sort_object_by_regions(doc_img)
        else:
            object_region_label_l = np.zeros(len(object_l))
            sorted_region_label_l = [0]

        polygon_l = [geo.Polygon(object.boundary) for object in object_l]
        
        sorted_object_l = []
        for region_label in sorted_region_label_l:
            region_object_polygon_l = [polygon for polygon, object_region_label in zip(polygon_l, object_region_label_l) if object_region_label == region_label]
            x_overlap_matrix = np.zeros((len(region_object_polygon_l), len(region_object_polygon_l)))
            for i, polygon_i in enumerate(region_object_polygon_l):
                polygon_i_min_x = polygon_i.bounds[0]
                polygon_i_max_x = polygon_i.bounds[2]
                polygon_i_width = polygon_i_max_x - polygon_i_min_x
                for j, polygon_j in enumerate(region_object_polygon_l):
                    polygon_j_min_x = polygon_j.bounds[0]
                    polygon_j_max_x = polygon_j.bounds[2]
                    polygon_j_width = polygon_j_max_x - polygon_j_min_x
                    overlap_min = max(polygon_i_min_x, polygon_j_min_x)
                    overlap_max = min(polygon_i_max_x, polygon_j_max_x)
                    if overlap_min >= overlap_max:
                        overlap_length = 0
                    else:
                        overlap_length = overlap_max - overlap_min
                    smallest_width = min(polygon_i_width, polygon_j_width)
                    overlap_ratio = overlap_length / smallest_width
                    x_overlap_matrix[i, j] = overlap_ratio

            polygon_max_x = np.array([polygon.bounds[2] for polygon in region_object_polygon_l])
            x_sorted_polygon_idx = np.argsort(polygon_max_x, kind='mergesort')[::-1].tolist()
            x_grouped_object_polygon_l = []
            while True:
                group_idx_buffer = []
                rigthmost_polygon_idx = x_sorted_polygon_idx[0]
                overlap_idx_l = np.where(x_overlap_matrix[rigthmost_polygon_idx] > self.x_axis_overlap_threshold)[0].tolist()
                group_idx_buffer.extend(overlap_idx_l)
                if len(overlap_idx_l) > 1:
                    for idx in overlap_idx_l:
                        overlap_idx_l = np.where(x_overlap_matrix[idx] > self.x_axis_overlap_threshold)[0].tolist()
                        group_idx_buffer.extend(overlap_idx_l)
                group_idx_buffer = list(set(group_idx_buffer))
                x_grouped_object_polygon_l.append([region_object_polygon_l[idx] for idx in group_idx_buffer])
                x_sorted_polygon_idx = [idx for idx in x_sorted_polygon_idx if idx not in group_idx_buffer]
                if len(x_sorted_polygon_idx) == 0:
                    break            

            for x_group_polygon_l in x_grouped_object_polygon_l:
                y_sorted_group_polygon_l = sorted(x_group_polygon_l, key=lambda x: x.bounds[1]) # sort top to bottom
                y_grouped_object_polygon_l = []
                while True:
                    object_polygon = y_sorted_group_polygon_l[0]
                    y_sorted_group_polygon_l = y_sorted_group_polygon_l[1:]
                    
                    polygon_min_y = object_polygon.bounds[1]
                    polygon_max_y = object_polygon.bounds[3]
                    polygon_height = polygon_max_y - polygon_min_y

                    group_polygon_buffer = [object_polygon]
                    last_grouped_object_idx = 0
                    for next_object_idx, next_object_polygon in enumerate(y_sorted_group_polygon_l):
                        next_object_polygon_min_y = next_object_polygon.bounds[1]
                        next_object_polygon_max_y = next_object_polygon.bounds[3]
                        next_object_polygon_height = next_object_polygon_max_y - next_object_polygon_min_y
                        
                        overlap_min = max(polygon_min_y, next_object_polygon_min_y)
                        overlap_max = min(polygon_max_y, next_object_polygon_max_y)
                        if overlap_min >= overlap_max:
                            overlap_length = 0
                        else:
                            overlap_length = overlap_max - overlap_min
                        smaller_height = min(polygon_height, next_object_polygon_height)
                        if overlap_length / smaller_height > self.y_axis_overlap_threshold:
                            group_polygon_buffer.append(next_object_polygon)
                            last_grouped_object_idx = next_object_idx
                        else:
                            last_grouped_object_idx = next_object_idx
                            break
                    y_grouped_object_polygon_l.append(group_polygon_buffer)
                    y_sorted_group_polygon_l = y_sorted_group_polygon_l[last_grouped_object_idx:]
                    if len(y_sorted_group_polygon_l) == 0:
                        break

                for y_group_polygon_l in y_grouped_object_polygon_l:
                    x_sorted_y_group_polygon_l = sorted(y_group_polygon_l, key=lambda x: x.bounds[2], reverse=True)
                    for obj_polygon in x_sorted_y_group_polygon_l:
                        sorted_object_l.append(object_l[polygon_l.index(obj_polygon)])
                    
        new_annotations = Layout()
        for objetc in sorted_object_l:
            new_annotations.add_object(objetc)
        
        doc_img.annotations = new_annotations
        return doc_img

    def sort_object_by_regions(self, doc_img):
            """Cluster objects into regions based on their centroids using DBSCAN and sort 
            regions from right to left and top to bottom."""
            
            object_l = doc_img.annotations.object_l
            img_width = doc_img.width
            img_height = doc_img.height
            
            polygon_l = [geo.Polygon(object.boundary) for object in object_l]
            centroid_l = [polygon.centroid for polygon in polygon_l]
            feature_matrix = np.array([[centroid.x / img_width, centroid.y / img_height] for centroid in centroid_l])
            
            dbscan = DBSCAN(eps=0.1, min_samples=1)
            dbscan.fit(feature_matrix)
            object_region_label_l = dbscan.labels_
            
            region_label_l = np.unique(object_region_label_l).tolist()
            if len(region_label_l) == 1:
                return object_region_label_l, region_label_l
            
            sorted_region_label_l = []
            region_polygon_l = [geo.MultiPolygon([polygon_l[i] for i, label in enumerate(object_region_label_l) if label == region_label]) for region_label in region_label_l]
            
            y_sorted_region_polygon_l = sorted(region_polygon_l, key=lambda x: x.bounds[1]) # sort top to bottom
            y_grouped_region_polygon_l = []
            while True:
                region_polygon = y_sorted_region_polygon_l[0]
                y_sorted_region_polygon_l = y_sorted_region_polygon_l[1:]
                
                region_min_y = region_polygon.bounds[1]
                region_max_y = region_polygon.bounds[3]
                region_height = region_max_y - region_min_y

                group_polygon_buffer = [region_polygon]
                last_grouped_region_idx = 0
                for next_region_idx, next_region_polygon in enumerate(y_sorted_region_polygon_l):
                    next_region_min_y = next_region_polygon.bounds[1]
                    next_region_max_y = next_region_polygon.bounds[3]
                    next_region_height = next_region_max_y - next_region_min_y
                    
                    overlap_min_y = max(region_min_y, next_region_min_y)
                    overlap_max_y = min(region_max_y, next_region_max_y)
                    overlap_length = max(0, overlap_max_y - overlap_min_y)

                    smaller_height = min(region_height, next_region_height)
                    if overlap_length / smaller_height > self.y_axis_overlap_threshold:
                        group_polygon_buffer.append(next_region_polygon)
                        last_grouped_region_idx = next_region_idx
                    else:
                        break
                y_grouped_region_polygon_l.append(group_polygon_buffer)
                y_sorted_region_polygon_l = y_sorted_region_polygon_l[last_grouped_region_idx + 1:]
                if len(y_sorted_region_polygon_l) == 0:
                    break

            for y_group_polygon_l in y_grouped_region_polygon_l:
                x_sorted_y_group_polygon_l = sorted(y_group_polygon_l, key=lambda x: x.bounds[2], reverse=True) # sort right to left
                for region_polygon in x_sorted_y_group_polygon_l:
                    sorted_region_label_l.append(region_polygon_l.index(region_polygon))

            return object_region_label_l, sorted_region_label_l
            
    
    def __call__(self, doc_img, sort_region=False):
        return self.order_lines(doc_img, sort_region=sort_region)

if __name__ == '__main__':
    # import cv2
    
    # doc_img = DocumentImage('/home/colibri/files/houlang_ocr/assets/image_2095.jpg')
    # doc_img.load_annotations_from_alto()
    # reading_order = HeuristicReadingOrderClassifier()
    # reading_order.order_lines(doc_img)
    # cv2.imwrite('./test.png', doc_img.plot())

    from houlang import DocumentImage, YOLOSegmenter, KrakenRecognizer

    doc_img = DocumentImage('/home/colibri/files/houlang/assets/汉书.一百卷.东汉.班固编撰.南宋庆元时期建安黄善夫刻.刘元起刊本.黑白版0072-4876.png')
    segmenter = YOLOSegmenter()
    doc_img = segmenter(doc_img)[0]
    reading_order = HeuristicReadingOrderClassifier()
    doc_img = reading_order(doc_img, sort_region=False)
    recognizer = KrakenRecognizer()
    text = recognizer(doc_img)
    print(text)
    breakpoint()