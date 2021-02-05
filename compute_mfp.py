from math import floor
HEIGHT = 169
AGE = 20
def compute(weight):
    bmr = (10*weight + 6.25*HEIGHT - 5*AGE + 5)*1.25
    ded = round(bmr-500, -1)
    carbs = (ded*0.5)/4
    protein = ded*0.4/4
    fat = ded*0.1/8
    fiber = 38
    return {"calories":ded, "carbs":carbs, "protein": protein, "fat":fat, "fiber": fiber}

def get_diff(totals, ded):
    exercise = totals.pop("exercise")
    ded1 = ded.copy()
    ded1["calories"] = ded1["calories"]+exercise
    for k in ded1.keys():
        ded1[k] = ded1[k] - totals[k]
    return ded1