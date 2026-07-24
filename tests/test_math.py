"""Independent checks for the current ROC 115 assessment collection."""

from __future__ import annotations

import math
import unittest
from fractions import Fraction


class Tcfs115MathChecks(unittest.TestCase):
    def test_q01_angle_expression_is_invariant(self) -> None:
        for x in (1, 15, 29, 45, 59):
            angle_c = 60 - x
            angle_b = 120 - x
            angle_a = 2 * x
            self.assertEqual(4 * angle_c - 2 * angle_b + angle_a, 0)

    def test_q03_parameter_counts(self) -> None:
        three_quadrants: list[int] = []
        positive_integer_root: list[int] = []
        for k in range(-5, 6):
            discriminant_quarter = k * k - k - 1
            if discriminant_quarter > 0 and k + 1 >= 0:
                three_quadrants.append(k)
            if discriminant_quarter >= 0:
                root_part = math.isqrt(discriminant_quarter)
                if root_part * root_part == discriminant_quarter:
                    roots = (-k + root_part, -k - root_part)
                    if any(root > 0 for root in roots):
                        positive_integer_root.append(k)
        self.assertEqual(three_quadrants, [-1, 2, 3, 4, 5])
        self.assertEqual(positive_integer_root, [-1])

    def test_q02_three_equal_rectangles(self) -> None:
        first_area = 5 * 12
        rectangle_areas = [first_area, first_area, first_area]
        self.assertEqual(sum(rectangle_areas), 180)

    def test_q04_every_four_move_block_is_four(self) -> None:
        for n in range(1, 100, 4):
            block = n**2 - (n + 1) ** 2 - (n + 2) ** 2 + (n + 3) ** 2
            self.assertEqual(block, 4)
        total = sum(
            value**2 if value % 4 in {0, 1} else -(value**2)
            for value in range(1, 101)
        )
        self.assertEqual(total, 100)

    def test_q05_integer_boundary(self) -> None:
        self.assertLess(210 * 9, 2026)
        self.assertGreater(210 * 10, 2026)

    def test_q06_exhaustive_factor_and_triangle_filter(self) -> None:
        solutions: list[tuple[int, int, int]] = []
        for z in range(2, 481):
            for y in range(z + 1, 481):
                if 480 % (y * z):
                    continue
                x = 480 // (y * z)
                if x <= y:
                    continue
                a, b, c = x - 1, y - 1, z - 1
                if b + c > a:
                    solutions.append((a, b, c))
        self.assertEqual(solutions, [(11, 9, 3), (9, 7, 5)])

    def test_q07_target_is_fixed_by_partner_products(self) -> None:
        for u in (0.5, 1.0, 2.0, 4.0, 8.0):
            v = 7 / u
            a = (u - 4 / u) / 2
            b = (v - 9 / v) / 2
            big_a = (u + 4 / u) / 2
            big_b = (v + 9 / v) / 2
            target = a * big_b + b * big_a
            self.assertAlmostEqual(target, 13 / 14)

    def test_q08_collision_count_and_uniqueness(self) -> None:
        centers = range(0, 101, 2)

        def distinct_count(offset: float) -> int:
            points = {center - offset for center in centers}
            points.update(center + offset for center in centers)
            return len(points)

        self.assertEqual(distinct_count(25), 76)
        self.assertEqual(
            [offset for offset in range(1, 51) if distinct_count(offset) == 76],
            [25],
        )
        self.assertEqual(distinct_count(12.5), 102)

    def test_q09_half_then_double(self) -> None:
        sector = (300 / 360) * math.pi * 4**2
        triangle = 4 * math.sqrt(3)
        semicircle = 0.5 * math.pi * 2**2
        upper = sector + triangle - semicircle
        expected_upper = 34 * math.pi / 3 + 4 * math.sqrt(3)
        expected_total = 68 * math.pi / 3 + 8 * math.sqrt(3)
        self.assertAlmostEqual(upper, expected_upper)
        self.assertAlmostEqual(2 * upper, expected_total)

    def test_q10_normalized_intervals_are_separated(self) -> None:
        intervals = {
            "b": (Fraction(1, 7), Fraction(1, 6)),
            "d": (Fraction(2, 11), Fraction(2, 9)),
            "a": (Fraction(5, 21), Fraction(5, 19)),
            "c": (Fraction(5, 13), Fraction(5, 12)),
        }
        self.assertLess(intervals["b"][1], intervals["d"][0])
        self.assertLess(intervals["d"][1], intervals["a"][0])
        self.assertLess(intervals["a"][1], intervals["c"][0])

    def test_q11_cube_plane_ratio(self) -> None:
        side = Fraction(1)
        z_at_n = Fraction(2, 3) * side
        fn = side - z_at_n
        nb = z_at_n
        self.assertEqual(fn / nb, Fraction(1, 2))

    def test_q12_rotated_path_values(self) -> None:
        minimum = 2 * math.sqrt(6) + 2 * math.sqrt(2)
        ap = 2 * math.sqrt(3) - 2
        self.assertAlmostEqual(minimum**2, 32 + 16 * math.sqrt(3))
        self.assertGreater(ap, 0)
        self.assertLess(ap, 2 * math.sqrt(3))

    def test_part2_q01_corrected_roots(self) -> None:
        roots = ((5 + math.sqrt(37)) / 6, (5 - math.sqrt(37)) / 6)
        for root in roots:
            self.assertAlmostEqual(3 * root**2 - 5 * root - 1, 0)
        wrong_roots = ((-5 + math.sqrt(37)) / 6, (-5 - math.sqrt(37)) / 6)
        self.assertTrue(
            any(abs(3 * root**2 - 5 * root - 1) > 1 for root in wrong_roots)
        )

    def test_part2_q02_positive_angle_bisector_length(self) -> None:
        ab = Fraction(4)
        ac = Fraction(5)
        bc = Fraction(6)
        bd = bc * ab / (ab + ac)
        dc = bc * ac / (ab + ac)
        ad_squared = ab * ac - bd * dc
        self.assertEqual(ad_squared, Fraction(100, 9))
        self.assertAlmostEqual(math.sqrt(ad_squared), float(Fraction(10, 3)))


if __name__ == "__main__":
    unittest.main()
