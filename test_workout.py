import unittest
from workout import (calories_from_macros, macros_from_calories, bmi, bmr_mifflin, tdee, protein_target_per_lb, weekly_weight_change, WorkoutTracker)

class TestCaloriesAndMacros(unittest.TestCase):
    def test_calories_basic(self):
        self.assertEqual(calories_from_macros(100, 200, 70), 1830)

    def test_calories_with_alcohol(self):
        self.assertEqual(calories_from_macros(0, 0, 0, 10), 70)

    def test_calories_all_zero(self):
        self.assertEqual(calories_from_macros(0, 0, 0, 0), 0)

    def test_calories_negative_protein_raises(self):
        with self.assertRaises(ValueError):
            calories_from_macros(-1, 0, 0, 0)

    def test_calories_negative_alcohol_raises(self):
        with self.assertRaises(ValueError):
            calories_from_macros(0, 0, 0, -0.1)

    def test_macros_happy_path(self):
        # 2000 kcal, P30/C40/F30
        p, c, f, a = macros_from_calories(2000, 0.30, 0.40, 0.30, 0.0)
        self.assertAlmostEqual(p, 2000 * 0.30 / 4, places=6)
        self.assertAlmostEqual(c, 2000 * 0.40 / 4, places=6)
        self.assertAlmostEqual(f, 2000 * 0.30 / 9, places=6)
        self.assertAlmostEqual(a, 0.0, places=6)

    def test_macros_with_alcohol(self):
        p, c, f, a = macros_from_calories(2100, 0.25, 0.45, 0.20, 0.10)
        self.assertAlmostEqual(p, 2100 * 0.25 / 4, places=6)
        self.assertAlmostEqual(c, 2100 * 0.45 / 4, places=6)
        self.assertAlmostEqual(f, 2100 * 0.20 / 9, places=6)
        self.assertAlmostEqual(a, 2100 * 0.10 / 7, places=6)

    def test_macros_zero_calories_returns_zeros(self):
        self.assertEqual(macros_from_calories(0, 1.0, 0.0, 0.0, 0.0), (0, 0, 0, 0))

    def test_macros_negative_calories_raises(self):
        with self.assertRaises(ValueError):
            macros_from_calories(-1, 0.3, 0.4, 0.3, 0.0)

    def test_macros_fractions_must_sum_to_one(self):
        with self.assertRaises(ValueError):
            macros_from_calories(2000, 0.3, 0.3, 0.3, 0.2)
        with self.assertRaises(ValueError):
            macros_from_calories(2000, 0.3, 0.3, 0.39, 0.00)

    def test_macros_negative_fraction_raises(self):
        with self.assertRaises(ValueError):
            macros_from_calories(2000, -0.1, 0.4, 0.7, 0.0)


class TestBodyCalculators(unittest.TestCase):
    def test_bmi_known_example(self):
        self.assertAlmostEqual(bmi(176, 70), 703 * 176 / (70 ** 2), places=6)

    def test_bmi_requires_positive_inputs(self):
        with self.assertRaises(ValueError):
            bmi(0, 70)
        with self.assertRaises(ValueError):
            bmi(150, 0)
        with self.assertRaises(ValueError):
            bmi(-150, 70)

    def test_bmr_mifflin_male(self):
        weight_lb, height_in, age = 180, 70, 30
        weight_kg = weight_lb * 0.45359237
        height_cm = height_in * 2.54
        expected = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        self.assertAlmostEqual(bmr_mifflin("male", weight_lb, height_in, age), expected, places=6)

    def test_bmr_mifflin_female(self):
        weight_lb, height_in, age = 132, 65, 28
        weight_kg = weight_lb * 0.45359237
        height_cm = height_in * 2.54
        expected = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        self.assertAlmostEqual(bmr_mifflin("female", weight_lb, height_in, age), expected, places=6)

    def test_bmr_mifflin_invalid_inputs(self):
        with self.assertRaises(ValueError):
            bmr_mifflin("male", -1, 70, 30)
        with self.assertRaises(ValueError):
            bmr_mifflin("male", 180, 0, 30)
        with self.assertRaises(ValueError):
            bmr_mifflin("unknown", 180, 70, 30)


    def test_tdee_valid_levels(self):
        self.assertAlmostEqual(tdee(1700, "sedentary"), 1700 * 1.2, places=6)
        self.assertAlmostEqual(tdee(1700, "light"), 1700 * 1.375, places=6)
        self.assertAlmostEqual(tdee(1700, "moderate"), 1700 * 1.55, places=6)
        self.assertAlmostEqual(tdee(1700, "active"), 1700 * 1.725, places=6)
        self.assertAlmostEqual(tdee(1700, "very_active"), 1700 * 1.9, places=6)

    def test_tdee_invalid_level_or_bmr(self):
        with self.assertRaises(ValueError):
            tdee(0, "sedentary")
        with self.assertRaises(ValueError):
            tdee(2000, "super_active")


class TestProteinAndWeightChange(unittest.TestCase):

    def test_protein_targets_by_goal(self):
        self.assertAlmostEqual(protein_target_per_lb(200, "cut"), 1.0 * 200, places=6)
        self.assertAlmostEqual(protein_target_per_lb(200, "maintain"), 0.73 * 200, places=6)
        self.assertAlmostEqual(protein_target_per_lb(200, "bulk"), 0.82 * 200, places=6)

    def test_protein_invalid_goal_or_weight(self):
        with self.assertRaises(ValueError):
            protein_target_per_lb(0, "cut")
        with self.assertRaises(ValueError):
            protein_target_per_lb(180, "recomp")


    def test_weekly_weight_change_gain(self):
        self.assertAlmostEqual(weekly_weight_change(200, 201, 7), 1.0, places=6)

    def test_weekly_weight_change_loss(self):
        self.assertAlmostEqual(weekly_weight_change(201, 200, 7), -1.0, places=6)

    def test_weekly_weight_change_requires_positive_days(self):
        with self.assertRaises(ValueError):
            weekly_weight_change(200, 202, 0)


class TestWorkoutTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = WorkoutTracker()

    def test_add_set_and_list_exercises(self):
        self.tracker.add_set("Squat", 5, 225)
        self.tracker.add_set("Bench", 8, 155)
        self.assertEqual(self.tracker.exercises(), ["Squat", "Bench"])

    def test_add_set_validates_inputs(self):
        with self.assertRaises(ValueError):
            self.tracker.add_set("", 5, 100)
        with self.assertRaises(ValueError):
            self.tracker.add_set("Squat", 0, 100)
        with self.assertRaises(ValueError):
            self.tracker.add_set("Squat", 5, -1)

    def test_total_volume_specific_and_overall(self):
        self.tracker.add_set("Deadlift", 5, 315)
        self.tracker.add_set("Deadlift", 3, 335)
        self.tracker.add_set("Row", 10, 95)
        self.assertEqual(self.tracker.total_volume("Deadlift"), 2580)
        self.assertEqual(self.tracker.total_volume("Row"), 950)
        self.assertEqual(self.tracker.total_volume(), 3530)

    def test_total_volume_missing_exercise_is_zero(self):
        self.assertEqual(self.tracker.total_volume("Press"), 0)

    def test_best_1rm_epley(self):
        self.tracker.add_set("Bench", 5, 185)
        self.tracker.add_set("Bench", 3, 195)
        expected = max(185 * (1 + 5/30), 195 * (1 + 3/30))
        self.assertAlmostEqual(self.tracker.best_1rm("Bench"), expected, places=4)

    def test_best_1rm_no_sets_returns_zero(self):
        self.assertEqual(self.tracker.best_1rm("Squat"), 0.0)

    def test_reset_clears_everything(self):
        self.tracker.add_set("Squat", 5, 225)
        self.tracker.reset()
        self.assertEqual(self.tracker.exercises(), [])
        self.assertEqual(self.tracker.total_volume(), 0)
        self.assertEqual(self.tracker.best_1rm("Squat"), 0.0)


if __name__ == "__main__":
    unittest.main()