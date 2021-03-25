import unittest

from typing import Tuple

import python_back.src.detection as det


class DetectionUtilsTest(unittest.TestCase):
    def test_rect_center(self):
        rect_coords = (10, 10, 35, 35)
        expected_center = (27, 27)
        center = det.get_rect_center(*rect_coords)
        self.assertEqual(center, expected_center)

    def test_remove_similar_centers(self):
        test_material = {"a": [((0, 1), 5), ((0, 2), 3), ((30, 50), 1), ((1, 3), 5), ((0, 4), 8)],
                         "b": [((0, 5), 5), ((0, 2), 3), ((30, 50), 1), ((1, 3), 5), ((0, 4), 8)],
                         "c": [((0, 0), 5), ((0, 4), 8)]}
        points_expected = [[(0, 2), (30, 50)], [(0, 4), (30, 50)], [(0, 2)]]
        det.remove_similar_centers(test_material)
        dict_value: str
        pt_exp: Tuple[tuple]
        for dict_value, pt_exp in zip(test_material, points_expected):
            self.assertEqual(len(test_material[dict_value]), len(pt_exp))
            pt_res = [elmt[0] for elmt in test_material[dict_value]]
            for pt in pt_exp:
                self.assertTrue(pt in pt_res)
    def is_in_area(self):
        # simple test case
        base_rect = [0, 0, 20, 20]
        forbiddens = [15, 15, 10, 10]
        self.assertTrue(det.is_in_area(base_rect, forbiddens))
        rep = is_in_area([3, 3, 13, 13], [[0, 0, 20, 20], [15, 15, 10, 10]])
        print(rep)