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

    def test_q04_trapezoid_division_is_shear_invariant(self) -> None:
        def subtract(
            left: tuple[Fraction, Fraction],
            right: tuple[Fraction, Fraction],
        ) -> tuple[Fraction, Fraction]:
            return left[0] - right[0], left[1] - right[1]

        def cross(
            left: tuple[Fraction, Fraction],
            right: tuple[Fraction, Fraction],
        ) -> Fraction:
            return left[0] * right[1] - left[1] * right[0]

        def first_line_parameter(
            point: tuple[Fraction, Fraction],
            direction: tuple[Fraction, Fraction],
            other_point: tuple[Fraction, Fraction],
            other_direction: tuple[Fraction, Fraction],
        ) -> Fraction:
            denominator = cross(direction, other_direction)
            self.assertNotEqual(denominator, 0)
            return cross(subtract(other_point, point), other_direction) / denominator

        for unit, shear, height in (
            (Fraction(1), Fraction(-2), Fraction(3)),
            (Fraction(2), Fraction(0), Fraction(5)),
            (Fraction(3, 2), Fraction(7, 3), Fraction(4, 3)),
            (Fraction(5, 3), Fraction(-1, 4), Fraction(-2)),
        ):
            a = (Fraction(0), Fraction(0))
            b = (3 * unit, Fraction(0))
            d = (shear, height)
            c = (shear + unit, height)
            e = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)

            af_over_ad = first_line_parameter(
                a,
                subtract(d, a),
                b,
                subtract(e, b),
            )
            self.assertEqual(af_over_ad, Fraction(3, 5))
            self.assertGreater(af_over_ad, 0)
            self.assertLess(af_over_ad, 1)

            g_parameter_on_dc = first_line_parameter(
                d,
                subtract(c, d),
                b,
                subtract(e, b),
            )
            self.assertEqual(g_parameter_on_dc, -2)
            self.assertEqual(abs(g_parameter_on_dc) * unit, 2 * unit)

    def test_q05_integer_roots_exhaust_all_signed_factor_pairs(self) -> None:
        signed_divisors = {
            sign * divisor
            for divisor in range(1, 262)
            if 261 % divisor == 0
            for sign in (-1, 1)
        }
        decoded_pairs = {
            ((left + 6) // 5, (right + 6) // 5)
            for left in signed_divisors
            for right in signed_divisors
            if left * right == 261
            and (left + 6) % 5 == 0
            and (right + 6) % 5 == 0
            and (left + 6) // 5 > 0
            and (right + 6) // 5 > 0
        }
        self.assertEqual(decoded_pairs, {(3, 7), (7, 3)})

        alpha, beta = 3, 7
        parameter = alpha + beta
        self.assertEqual(parameter, 10)
        positive_roots = {
            x
            for x in range(1, 100)
            if 5 * x * x - 5 * parameter * x + 6 * parameter + 45 == 0
        }
        self.assertEqual(positive_roots, {alpha, beta})

        def f(x: int) -> int:
            return (x + 1) * (5 * x * x + 45)

        def g(x: int) -> int:
            return (x + 1) * (5 * x - 6)

        for root in positive_roots:
            self.assertEqual(f(root), parameter * g(root))

    def test_q06_opening_direction_selects_the_quadratic_parameter(self) -> None:
        candidates = {
            value
            for value in (Fraction(-3, 5), Fraction(1))
            if 5 * value * value - 2 * value - 3 == 0
        }
        self.assertEqual(candidates, {Fraction(-3, 5), Fraction(1)})

        def f(x: Fraction, parameter: Fraction) -> Fraction:
            return (
                parameter * x * x
                - 2 * parameter * x
                + 6 * parameter
                - 3 / parameter
            )

        wrong = Fraction(1)
        self.assertEqual(f(Fraction(1), wrong), 2)
        self.assertGreater(f(Fraction(0), wrong), 2)

        parameter = Fraction(-3, 5)
        for x in (Fraction(-4), Fraction(0), Fraction(1), Fraction(7, 3)):
            self.assertEqual(
                f(x, parameter),
                parameter * (x - 1) ** 2 + 2,
            )
            self.assertLessEqual(f(x, parameter), 2)

        def g(x: Fraction) -> Fraction:
            return (
                -parameter * x * x
                + 4 * parameter * x
                + 6 * parameter
                - 3 / parameter
            )

        for x in (Fraction(-2), Fraction(0), Fraction(2), Fraction(11, 4)):
            self.assertEqual(g(x), Fraction(3, 5) * (x - 2) ** 2 - 1)
            self.assertGreaterEqual(g(x), -1)
        self.assertEqual(g(Fraction(2)), -1)

    def test_q07_digitwise_shift_has_one_square_output(self) -> None:
        factor_pairs = [
            (left, 555 // left)
            for left in range(1, 24)
            if 555 % left == 0
        ]
        self.assertEqual(factor_pairs, [(1, 555), (3, 185), (5, 111), (15, 37)])
        decoded = {
            ((right - left) // 2, (right + left) // 2)
            for left, right in factor_pairs
            if (right - left) % 2 == 0
        }
        self.assertEqual(decoded, {(277, 278), (91, 94), (53, 58), (11, 26)})

        def add_five_to_each_digit(value: int) -> int | None:
            digits = [int(digit) for digit in str(value)]
            if len(digits) != 3 or any(digit > 4 for digit in digits):
                return None
            return int("".join(str(digit + 5) for digit in digits))

        legal_transforms = [
            (a, a * a, transformed)
            for a in range(10, 100)
            if (transformed := add_five_to_each_digit(a * a)) is not None
        ]
        self.assertEqual(
            legal_transforms,
            [
                (10, 100, 655),
                (11, 121, 676),
                (12, 144, 699),
                (18, 324, 879),
                (20, 400, 955),
                (21, 441, 996),
            ],
        )
        square_outputs = [
            (a, transformed)
            for a, _, transformed in legal_transforms
            if math.isqrt(transformed) ** 2 == transformed
        ]
        self.assertEqual(square_outputs, [(11, 676)])

    def test_q08_transferred_ball_means_are_feasible_only_for_nine(self) -> None:
        admissible_counts = []
        for count_a in range(2, 25):
            mean_a = Fraction(count_a + 59, 4)
            mean_b = Fraction(count_a + 34, 4)
            if count_a * mean_a + (25 - count_a) * mean_b == 325:
                admissible_counts.append(count_a)
        self.assertEqual(admissible_counts, [9])

        basket_a = set(range(13, 22))
        basket_b = set(range(1, 13)) | set(range(22, 26))
        self.assertEqual(basket_a | basket_b, set(range(1, 26)))
        self.assertFalse(basket_a & basket_b)
        self.assertIn(15, basket_a)

        old_mean_a = Fraction(sum(basket_a), len(basket_a))
        old_mean_b = Fraction(sum(basket_b), len(basket_b))
        basket_a.remove(15)
        basket_b.add(15)
        new_mean_a = Fraction(sum(basket_a), len(basket_a))
        new_mean_b = Fraction(sum(basket_b), len(basket_b))
        self.assertEqual(new_mean_a - old_mean_a, Fraction(1, 4))
        self.assertEqual(new_mean_b - old_mean_b, Fraction(1, 4))

    def test_q09_palindromic_square_search_is_exhaustive(self) -> None:
        candidates = []
        solutions = []
        for a in range(1, 10):
            for b in range(10):
                for c in range(10):
                    value = 10001 * a + 1010 * b + 100 * c
                    digit_sum = 2 * a + 2 * b + c
                    if digit_sum == 36:
                        candidates.append(value)
                    if (
                        10 <= digit_sum <= 99
                        and math.isqrt(digit_sum) ** 2 == digit_sum
                        and math.isqrt(
                            sum(int(digit) for digit in str(digit_sum))
                        )
                        ** 2
                        == sum(int(digit) for digit in str(digit_sum))
                        and math.isqrt(value) ** 2 == value
                    ):
                        solutions.append((digit_sum, value))

        filtered_candidates = sorted(
            value
            for value in candidates
            if int(str(value)[0]) in {5, 6, 9}
        )
        self.assertEqual(
            filtered_candidates,
            [59895, 68886, 69696, 95859, 96669, 97479, 98289, 99099],
        )
        self.assertEqual(
            [value for value in filtered_candidates if value % 4 in {0, 1}],
            [69696, 96669, 98289],
        )
        self.assertLess(310**2, 96669)
        self.assertLess(96669, 311**2)
        self.assertLess(313**2, 98289)
        self.assertLess(98289, 314**2)
        self.assertEqual(264**2, 69696)
        self.assertEqual(solutions, [(36, 69696)])

    def test_q10_translated_triangle_union_has_exact_boundary_and_area(self) -> None:
        def union_boundary(count: int) -> list[tuple[Fraction, Fraction]]:
            points = [(Fraction(0), Fraction(0)), (Fraction(1, 2), Fraction(1, 2))]
            for index in range(count - 1):
                points.extend(
                    [
                        (Fraction(3 + 2 * index, 4), Fraction(1, 4)),
                        (Fraction(2 + index, 2), Fraction(1, 2)),
                    ]
                )
            points.append((Fraction(count + 1, 2), Fraction(0)))
            return points

        def exact_edge_length(
            first: tuple[Fraction, Fraction],
            second: tuple[Fraction, Fraction],
        ) -> Fraction:
            dx = second[0] - first[0]
            dy_coefficient = second[1] - first[1]
            squared = dx * dx + 3 * dy_coefficient * dy_coefficient
            numerator_root = math.isqrt(squared.numerator)
            denominator_root = math.isqrt(squared.denominator)
            self.assertEqual(numerator_root**2, squared.numerator)
            self.assertEqual(denominator_root**2, squared.denominator)
            return Fraction(numerator_root, denominator_root)

        def audit(count: int) -> tuple[Fraction, Fraction]:
            boundary = union_boundary(count)
            perimeter = sum(
                (
                    exact_edge_length(boundary[index], boundary[(index + 1) % len(boundary)])
                    for index in range(len(boundary))
                ),
                start=Fraction(0),
            )
            twice_area_coefficient = sum(
                (
                    boundary[index][0] * boundary[(index + 1) % len(boundary)][1]
                    - boundary[(index + 1) % len(boundary)][0] * boundary[index][1]
                    for index in range(len(boundary))
                ),
                start=Fraction(0),
            )
            return perimeter, abs(twice_area_coefficient) / 2

        self.assertEqual(audit(1), (Fraction(3), Fraction(1, 4)))
        self.assertEqual(audit(2), (Fraction(9, 2), Fraction(7, 16)))
        self.assertEqual(audit(3), (Fraction(6), Fraction(5, 8)))
        self.assertEqual(audit(112), (Fraction(339, 2), Fraction(337, 16)))

    def test_q11_square_condition_forces_the_interior_angle_signature(self) -> None:
        a = (Fraction(0), Fraction(1))
        b = (Fraction(1), Fraction(1))
        c = (Fraction(1), Fraction(0))

        def vector(
            start: tuple[Fraction, Fraction],
            end: tuple[Fraction, Fraction],
        ) -> tuple[Fraction, Fraction]:
            return end[0] - start[0], end[1] - start[1]

        def dot(
            first: tuple[Fraction, Fraction],
            second: tuple[Fraction, Fraction],
        ) -> Fraction:
            return first[0] * second[0] + first[1] * second[1]

        def determinant(
            first: tuple[Fraction, Fraction],
            second: tuple[Fraction, Fraction],
        ) -> Fraction:
            return first[0] * second[1] - first[1] * second[0]

        def squared_distance(
            first: tuple[Fraction, Fraction],
            second: tuple[Fraction, Fraction],
        ) -> Fraction:
            return dot(vector(first, second), vector(first, second))

        def condition(point: tuple[Fraction, Fraction]) -> bool:
            return 2 * squared_distance(b, point) == (
                squared_distance(c, point) - squared_distance(a, point)
            )

        for ratio in (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5)):
            u = (1 - ratio) / (1 + ratio * ratio)
            v = ratio * u
            point = (1 - u, 1 - v)
            self.assertTrue(0 < point[0] < 1 and 0 < point[1] < 1)
            self.assertTrue(condition(point))
            pa = vector(point, a)
            pb = vector(point, b)
            self.assertLess(dot(pa, pb), 0)
            self.assertEqual(abs(determinant(pa, pb)), -dot(pa, pb))

        outside = (Fraction(0), Fraction(2))
        self.assertTrue(condition(outside))
        outside_pa = vector(outside, a)
        outside_pb = vector(outside, b)
        self.assertGreater(dot(outside_pa, outside_pb), 0)
        self.assertEqual(
            abs(determinant(outside_pa, outside_pb)),
            dot(outside_pa, outside_pb),
        )

    def test_q12_hexagon_overlap_has_its_minimum_at_half_period(self) -> None:
        apothem = math.sqrt(3) / 2

        def overlap_area(angle_degrees: float) -> float:
            constraints = []
            for offset in (0.0, math.radians(angle_degrees)):
                for index in range(6):
                    angle = offset + index * math.pi / 3
                    constraints.append((math.cos(angle), math.sin(angle)))

            vertices: list[tuple[float, float]] = []
            for first, second in combinations(constraints, 2):
                determinant = first[0] * second[1] - first[1] * second[0]
                if abs(determinant) < 1e-10:
                    continue
                x = apothem * (second[1] - first[1]) / determinant
                y = apothem * (first[0] - second[0]) / determinant
                if all(nx * x + ny * y <= apothem + 1e-9 for nx, ny in constraints):
                    vertices.append((x, y))

            unique: list[tuple[float, float]] = []
            for point in vertices:
                if not any(math.dist(point, other) < 1e-8 for other in unique):
                    unique.append(point)
            unique.sort(key=lambda point: math.atan2(point[1], point[0]))
            twice_area = sum(
                unique[index][0] * unique[(index + 1) % len(unique)][1]
                - unique[(index + 1) % len(unique)][0] * unique[index][1]
                for index in range(len(unique))
            )
            return abs(twice_area) / 2

        expected = 18 - 9 * math.sqrt(3)
        self.assertAlmostEqual(overlap_area(30), expected, places=10)
        self.assertAlmostEqual(overlap_area(0), 3 * math.sqrt(3) / 2, places=10)
        for angle in (4, 12, 21, 30):
            analytic = 6 * apothem**2 * (
                math.tan(math.radians(angle / 2))
                + math.tan(math.radians((60 - angle) / 2))
            )
            self.assertAlmostEqual(overlap_area(angle), analytic, places=10)
            self.assertAlmostEqual(overlap_area(angle), overlap_area(60 - angle), places=10)
        sampled = [overlap_area(angle) for angle in range(61)]
        self.assertEqual(sampled.index(min(sampled)), 30)

    def test_q13_recruitment_color_extrema_are_attained(self) -> None:
        founders = set(range(6))
        next_member = 6
        current_recruiter = 0
        parent: dict[int, int] = {}
        outdegree: dict[int, int] = {}

        for _ in range(97):
            self.assertLess(current_recruiter, next_member)
            self.assertNotIn(current_recruiter, outdegree)
            children = list(range(next_member, next_member + 7))
            for child in children:
                parent[child] = current_recruiter
            outdegree[current_recruiter] = 7
            current_recruiter = children[0]
            next_member += 7

        members = set(range(next_member))
        self.assertEqual(len(members), 685)
        self.assertEqual(len(parent), 679)
        self.assertEqual(sum(outdegree.values()), 679)
        self.assertEqual(members - set(parent), founders)
        self.assertTrue(all(degree in {7, 14, 28, 35} for degree in outdegree.values()))

        def inherited_founder(member: int) -> int:
            while member in parent:
                member = parent[member]
            return member

        self.assertEqual({inherited_founder(member) for member in members}, founders)
        self.assertEqual((685 - len(founders)) % 7, 0)

        maximum_founders = set(range(685))
        maximum_edges: dict[int, int] = {}
        self.assertEqual(len(maximum_founders), 685)
        self.assertFalse(maximum_edges)

    def test_part2_q01_triangle_area_transforms(self) -> None:
        self.assertEqual(Fraction(3 * 4, 2), 6)

        base_area = Fraction(7 * 11, 2)
        doubled_area = Fraction((2 * 7) * (2 * 11), 2)
        self.assertEqual(doubled_area / base_area, 4)

        def median_side_squares(
            side_squares: tuple[Fraction, Fraction, Fraction],
        ) -> tuple[Fraction, Fraction, Fraction]:
            a2, b2, c2 = side_squares
            return (
                (2 * b2 + 2 * c2 - a2) / 4,
                (2 * c2 + 2 * a2 - b2) / 4,
                (2 * a2 + 2 * b2 - c2) / 4,
            )

        original_squares = (Fraction(16), Fraction(64), Fraction(80))
        first_medians = median_side_squares(original_squares)
        second_medians = median_side_squares(first_medians)
        self.assertEqual(
            second_medians,
            tuple(Fraction(9, 16) * value for value in original_squares),
        )
        self.assertEqual(Fraction(16) * Fraction(3, 4) ** 2, 9)

        original_area = Fraction(45)
        height_triangle_area = Fraction(30)
        for side in (Fraction(7), Fraction(11), Fraction(13)):
            original_altitude = 2 * original_area / side
            next_altitude = 2 * height_triangle_area / original_altitude
            self.assertEqual(next_altitude, Fraction(2, 3) * side)
        self.assertEqual(original_area * Fraction(2, 3) ** 2, 20)


if __name__ == "__main__":
    unittest.main()
