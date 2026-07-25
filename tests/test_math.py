"""Independent checks for the cataloged assessment lessons."""

from __future__ import annotations

import math
import unittest
from fractions import Fraction
from itertools import combinations, permutations, product


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


class Tcfs113MathChecks(unittest.TestCase):
    def test_q01_exhaustive_positive_exponent_triples(self) -> None:
        triples = [
            (x, y, z)
            for x in range(1, 12)
            for y in range(1, 6)
            for z in range(1, 4)
            if x + 2 * y + 3 * z == 11
        ]
        self.assertEqual(
            triples,
            [(1, 2, 2), (2, 3, 1), (3, 1, 2), (4, 2, 1), (6, 1, 1)],
        )

    def test_q02_exhaustive_balanced_binary_digits(self) -> None:
        balanced = []
        for tail in product((0, 1), repeat=5):
            digits = (1, *tail)
            if sum(digits[::2]) == sum(digits[1::2]):
                balanced.append(digits)
        self.assertEqual(len(balanced), 10)

    def test_q03_exhaustive_median_at_least_mean(self) -> None:
        valid = []
        for triple in combinations(range(2024, 2030), 3):
            left, middle, right = triple
            if 3 * middle >= sum(triple):
                valid.append(triple)
            self.assertEqual(
                3 * middle >= sum(triple),
                middle - left >= right - middle,
            )
        self.assertEqual(len(valid), 13)

    def test_q04_exhaustive_acute_consecutive_triangles(self) -> None:
        valid_middle_sides = []
        for middle in range(2, 114):
            sides = (middle - 1, middle, middle + 1)
            if sum(sides) > 113:
                continue
            if sides[0] + sides[1] <= sides[2]:
                continue
            if sides[0] ** 2 + sides[1] ** 2 > sides[2] ** 2:
                valid_middle_sides.append(middle)
        self.assertEqual(valid_middle_sides, list(range(5, 38)))
        self.assertEqual(len(valid_middle_sides), 33)

    def test_q05_coefficient_by_subset_expansion(self) -> None:
        coefficients = {0: 1}
        for multiplier, exponent in enumerate((1, 2, 4, 8, 16, 32, 64), 1):
            expanded = dict(coefficients)
            for degree, coefficient in coefficients.items():
                new_degree = degree + exponent
                expanded[new_degree] = (
                    expanded.get(new_degree, 0) + multiplier * coefficient
                )
            coefficients = expanded
        self.assertEqual(coefficients[113], 210)

    def test_q06_progression_orders_force_roots(self) -> None:
        discriminant = 3**2 + 4 * 18
        arithmetic_candidates = (
            Fraction(-3 + math.isqrt(discriminant), 2),
            Fraction(-3 - math.isqrt(discriminant), 2),
        )
        self.assertEqual(arithmetic_candidates, (Fraction(3), Fraction(-6)))
        a = next(candidate for candidate in arithmetic_candidates if candidate > 0)
        b = 2 * a + 6
        self.assertEqual((a, b), (Fraction(3), Fraction(12)))
        self.assertEqual(a * b, 36)
        self.assertEqual((a + b) + a * b, 51)

    def test_q07_interval_extrema_force_fixed_endpoints(self) -> None:
        def quadratic(x: int) -> int:
            return x**2 - 6 * x + 12

        fixed_points = [x for x in range(-20, 21) if quadratic(x) == x]
        self.assertEqual(fixed_points, [3, 4])
        self.assertEqual(min(quadratic(x) for x in range(3, 5)), 3)
        self.assertEqual(max(quadratic(x) for x in range(3, 5)), 4)

    def test_q08_area_bisection_forces_minimum_integer_side(self) -> None:
        ce_over_side = Fraction(36, 59)
        od_over_side = Fraction(23, 13)
        height_at_left_edge = ce_over_side * od_over_side / (
            od_over_side + 1
        )
        self.assertEqual(height_at_left_edge + ce_over_side, 1)

        integer_pairs = [
            (od, side)
            for side in range(1, 100)
            for od in range(1, 200)
            if Fraction(od, side) == od_over_side
        ]
        self.assertEqual(integer_pairs[0], (23, 13))
        self.assertEqual(integer_pairs[0][1] ** 2, 169)

    def test_q09_exhaustive_consecutive_positive_sums(self) -> None:
        representations: list[tuple[int, int, int]] = []
        for length in range(60, 2025):
            minimum = length * (length + 1) // 2
            if minimum > 2024:
                break
            for first in range(1, 2025):
                total = length * (2 * first + length - 1) // 2
                if total > 2024:
                    break
                representations.append((total, length, first))

        self.assertEqual(
            representations,
            [
                (1830, 60, 1),
                (1890, 60, 2),
                (1950, 60, 3),
                (2010, 60, 4),
                (1891, 61, 1),
                (1952, 61, 2),
                (2013, 61, 3),
                (1953, 62, 1),
                (2015, 62, 2),
                (2016, 63, 1),
            ],
        )
        self.assertEqual(len({total for total, _, _ in representations}), 10)

    def test_q10_reflection_path_has_exact_minimum(self) -> None:
        reflected_b = (Fraction(48, 5), Fraction(-24, 5))
        q = (Fraction(48, 5), Fraction(8))
        p = (Fraction(48, 5), Fraction(16, 5))
        self.assertEqual(p[0] + 2 * p[1], 16)
        self.assertTrue(0 <= q[0] <= 16)

        pq = q[1] - p[1]
        pb_squared = (16 - p[0]) ** 2 + (8 - p[1]) ** 2
        self.assertEqual(pb_squared, 64)
        self.assertEqual(pq + 8, Fraction(64, 5))
        self.assertEqual(q[1] - reflected_b[1], Fraction(64, 5))

    def test_q11_direct_square_digit_stream(self) -> None:
        chunks: list[str] = []
        integer = 1
        while sum(map(len, chunks)) < 2024:
            chunks.append(str(integer * integer))
            integer += 1
        digits = "".join(chunks)
        self.assertEqual(digits[:15], "149162536496481")
        self.assertEqual((digits[112], digits[2023]), ("1", "3"))

    def test_q12_centroid_constraint_and_endpoint_extrema(self) -> None:
        centroid = (
            Fraction(1 + 7 - 2, 3),
            Fraction(-3 - 3 + 9, 3),
        )
        self.assertEqual(centroid, (Fraction(2), Fraction(1)))

        values = []
        for a in (Fraction(1), Fraction(3, 2), Fraction(2)):
            b = 9 - 2 * a
            self.assertGreaterEqual(b, 5)
            values.append(2 * a * a + b * b)
        self.assertEqual(values, [51, Fraction(81, 2), 33])
        self.assertEqual((max(values), min(values)), (51, 33))

    def test_q13_cube_bounds_have_one_positive_solution(self) -> None:
        def expression(a: int) -> int:
            return a**3 + 7 * a**2 - 5 * a + 8

        for a in range(1, 1001):
            value = expression(a)
            self.assertEqual(value - (a + 1) ** 3, 4 * (a - 1) ** 2 + 3)
            self.assertEqual(value - (a + 2) ** 3, a * (a - 17))
            self.assertEqual((a + 3) ** 3 - value, 2 * a**2 + 32 * a + 19)
            if a < 17:
                self.assertTrue((a + 1) ** 3 < value < (a + 2) ** 3)
            elif a == 17:
                self.assertEqual(value, (a + 2) ** 3)
            else:
                self.assertTrue((a + 2) ** 3 < value < (a + 3) ** 3)
        self.assertEqual((17, 19 - 1), (17, 18))

    def test_part2_q01_same_ray_zigzag_selects_first_closure(self) -> None:
        def points(step_count: int, multiplier: int) -> list[tuple[float, float]]:
            theta = multiplier * math.pi / step_count
            sin_theta = math.sin(theta)
            result = []
            for step in range(step_count + 1):
                radius = math.sin(step * theta) / sin_theta
                if step % 2:
                    result.append((radius, 0.0))
                else:
                    result.append(
                        (radius * math.cos(theta), radius * math.sin(theta))
                    )
            return result

        for step_count in range(3, 14, 2):
            simple = points(step_count, 1)
            self.assertAlmostEqual(simple[-1][0], 0.0)
            self.assertAlmostEqual(simple[-1][1], 0.0)
            simple_radii = [
                math.sin(step * math.pi / step_count)
                / math.sin(math.pi / step_count)
                for step in range(1, step_count)
            ]
            self.assertTrue(all(radius > 0 for radius in simple_radii))
            for start, end in zip(simple, simple[1:]):
                self.assertAlmostEqual(math.dist(start, end), 1.0)
            self.assertAlmostEqual(
                step_count * math.degrees(math.pi / step_count),
                180.0,
            )

            for multiplier in range(2, (step_count - 1) // 2 + 1):
                alternative = points(step_count, multiplier)
                self.assertAlmostEqual(alternative[-1][0], 0.0)
                self.assertAlmostEqual(alternative[-1][1], 0.0)
                alternative_radii = [
                    math.sin(step * multiplier * math.pi / step_count)
                    / math.sin(multiplier * math.pi / step_count)
                    for step in range(1, step_count)
                ]
                self.assertFalse(all(radius > 0 for radius in alternative_radii))

        self.assertAlmostEqual(math.degrees(math.pi / 5), 36.0)
        self.assertAlmostEqual(math.degrees(math.pi / 7), 180 / 7)


class Tcfs114MathChecks(unittest.TestCase):
    @staticmethod
    def admissible_final_indices(solution_sum: int) -> list[int]:
        doubled_sum = 2 * solution_sum
        admissible: list[int] = []
        for final_index in range(1, doubled_sum + 1):
            scale = Fraction(
                doubled_sum,
                final_index * (final_index + 1),
            )
            if not 1 < scale <= 2:
                continue
            current_fit = all(
                n <= scale * n < n + 1
                for n in range(1, final_index + 1)
            )
            next_fails = scale * (final_index + 1) >= final_index + 2
            if current_fit and next_fails:
                admissible.append(final_index)
        return admissible

    def test_q01_exhaustive_antidiagonal_grid(self) -> None:
        coordinate_by_value: dict[int, tuple[int, int]] = {}
        value = 1
        for coordinate_sum in range(2, 25):
            rows = [
                row
                for row in range(12, 0, -1)
                if 1 <= coordinate_sum - row <= 12
            ]
            for row in rows:
                column = coordinate_sum - row
                coordinate_by_value[value] = (row, column)
                value += 1
        self.assertEqual(value, 145)
        self.assertEqual(len(set(coordinate_by_value.values())), 144)
        self.assertEqual(coordinate_by_value[104], (8, 8))

    def test_q02_corrected_quadrant_boundary_and_minimum(self) -> None:
        def has_exactly_three_quadrants(parameter: float) -> bool:
            discriminant = parameter**2 - 4 * (parameter + 3)
            return parameter + 3 >= 0 and discriminant > 0

        self.assertFalse(has_exactly_three_quadrants(-4))
        self.assertTrue(has_exactly_three_quadrants(-3))
        self.assertTrue(has_exactly_three_quadrants(-2.5))
        self.assertFalse(has_exactly_three_quadrants(-2))
        self.assertFalse(has_exactly_three_quadrants(6))
        self.assertTrue(has_exactly_three_quadrants(7))
        self.assertTrue(has_exactly_three_quadrants(2021))
        self.assertEqual((2021 - 2025) ** 2 + 8 * (2021 - 2025) + 6, -10)

    def test_q03_octahedron_volume_ratio_is_scale_free(self) -> None:
        for side in (Fraction(1), Fraction(2), Fraction(7, 3)):
            middle_square_area = side * side / 2
            pyramid_height = side / 2
            octahedron = 2 * Fraction(1, 3) * middle_square_area * pyramid_height
            cube = side**3
            self.assertEqual(octahedron / cube, Fraction(1, 6))

    def test_q13_original_sum_is_inconsistent(self) -> None:
        self.assertEqual(self.admissible_final_indices(345), [])

    def test_q13_corrected_sum_closes_at_boundary(self) -> None:
        self.assertEqual(self.admissible_final_indices(420), [28])
        scale = Fraction(210, 203)
        t = 1 - 1 / scale
        parameter = t * (1 - t)
        self.assertEqual(t, Fraction(1, 30))
        self.assertEqual(parameter, Fraction(29, 900))
        for n in range(1, 29):
            x = scale * n
            self.assertLess(x, n + 1)
            self.assertEqual(n * (x - n), parameter * x * x)
        self.assertEqual(scale * 29, 30)


class Tcfs112MathChecks(unittest.TestCase):
    def test_q01_progression_and_unique_place_value_maximum(self) -> None:
        distances = [
            distance
            for distance in range(-20, 21)
            if (5 - distance) * 5 * (5 + distance) == 80
        ]
        self.assertEqual(distances, [-3, 3])

        value_sets = {
            tuple(sorted((5 - distance, 5, 5 + distance)))
            for distance in distances
        }
        self.assertEqual(value_sets, {(2, 5, 8)})

        numerals = sorted(
            100 * hundreds + 10 * tens + ones
            for hundreds, tens, ones in permutations((2, 5, 8))
        )
        self.assertEqual(numerals, [258, 285, 528, 582, 825, 852])
        self.assertEqual(numerals.count(max(numerals)), 1)

    def test_q02_weekday_cycle_and_large_power_remainder(self) -> None:
        weekday_names = (
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        )
        wednesday = weekday_names.index("Wednesday")

        expected_examples = {
            0: "Wednesday",
            1: "Thursday",
            7: "Wednesday",
            8: "Thursday",
            15: "Thursday",
        }
        for days, expected in expected_examples.items():
            self.assertEqual(weekday_names[(wednesday + days) % 7], expected)

        self.assertEqual(2024, 7 * 289 + 1)
        remainder = pow(2024, 112, 7)
        self.assertEqual(remainder, 1)
        self.assertEqual(weekday_names[(wednesday + remainder) % 7], "Thursday")

    def test_q03_overlapping_shares_and_prize_scale(self) -> None:
        solutions = [
            (a, b, c, d)
            for a in range(101)
            for b in range(101 - a)
            for c in range(101 - a - b)
            for d in [100 - a - b - c]
            if a + b == 40 and a + c == 60 and a + d == 50
        ]
        self.assertEqual(solutions, [(25, 15, 35, 25)])

        a, b, c, d = (Fraction(share, 100) for share in solutions[0])
        self.assertEqual(a + b + c + d, 1)
        self.assertEqual(
            (a + b, a + c, a + d),
            (Fraction(2, 5), Fraction(3, 5), Fraction(1, 2)),
        )

        total_prize = Fraction(315, 1) / c
        self.assertEqual(total_prize, 900)
        self.assertEqual(d * total_prize, 225)


if __name__ == "__main__":
    unittest.main()
