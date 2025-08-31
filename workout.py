def calories_from_macros(protein_g, carbs_g, fat_g, alcohol_g=0.0):
    if protein_g < 0 or carbs_g < 0 or fat_g < 0 or alcohol_g < 0:
        raise ValueError("macros cannot be negative")
    return 4 * protein_g + 4 * carbs_g + 9 * fat_g + 7 * alcohol_g


def macros_from_calories(calories, p_frac, c_frac, f_frac, a_frac=0.0):
    if calories < 0:
        raise ValueError("calories cannot be negative")
    if p_frac < 0 or c_frac < 0 or f_frac < 0 or a_frac < 0:
        raise ValueError("fractions cannot be negative")
    if abs((p_frac + c_frac + f_frac + a_frac) - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1.0")

    if calories == 0:
        return (0, 0, 0, 0)

    protein_g = (calories * p_frac) / 4
    carbs_g   = (calories * c_frac) / 4
    fat_g     = (calories * f_frac) / 9
    alcohol_g = (calories * a_frac) / 7
    return (protein_g, carbs_g, fat_g, alcohol_g)


def bmi(weight_lb, height_in):
    if weight_lb <= 0 or height_in <= 0:
        raise ValueError("weight and height must be positive")
    return 703.0 * weight_lb / (height_in ** 2)


def bmr_mifflin(sex, weight_lb, height_in, age_years):
    if weight_lb <= 0 or height_in <= 0 or age_years <= 0:
        raise ValueError("weight, height, and age must be positive")
    s = sex.lower()
    if s not in ("male", "female"):
        raise ValueError("sex must be 'male' or 'female'")

    weight_kg = weight_lb * 0.45359237
    height_cm = height_in * 2.54

    base = 10 * weight_kg + 6.25 * height_cm - 5 * age_years
    return base + (5 if s == "male" else -161)


def tdee(bmr, activity):
    if bmr <= 0:
        raise ValueError("bmr must be positive")
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    key = activity.lower()
    if key not in multipliers:
        raise ValueError("invalid activity level")
    return bmr * multipliers[key]


def protein_target_per_lb(weight_lb, goal="maintain"):
    if weight_lb <= 0:
        raise ValueError("weight must be positive")
    goal = goal.lower()
    if goal == "cut":
        return 1.0 * weight_lb
    elif goal == "maintain":
        return 0.73 * weight_lb
    elif goal == "bulk":
        return 0.82 * weight_lb
    else:
        raise ValueError("invalid goal")


def weekly_weight_change(start_lb, end_lb, days):
    if days <= 0:
        raise ValueError("days must be > 0")
    return (end_lb - start_lb) * (7 / days)


class WorkoutTracker:
    def __init__(self):
        self.data = {}

    def add_set(self, exercise, reps, weight):
        if not exercise or not isinstance(exercise, str):
            raise ValueError("exercise must be a non-empty string")
        if reps <= 0:
            raise ValueError("reps must be positive")
        if weight < 0:
            raise ValueError("weight cannot be negative")
        self.data.setdefault(exercise, []).append((reps, weight))

    def total_volume(self, exercise=None):
        def volume(sets):
            return sum(r * w for r, w in sets)
        if exercise is None:
            return sum(volume(sets) for sets in self.data.values())
        return volume(self.data.get(exercise, []))

    def best_1rm(self, exercise):
        sets = self.data.get(exercise, [])
        if not sets:
            return 0.0
        return max(w * (1 + r / 30) for r, w in sets)

    def exercises(self):
        return list(self.data.keys())

    def reset(self):
        self.data.clear()