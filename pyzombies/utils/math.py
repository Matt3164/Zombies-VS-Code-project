from math import sqrt # needed

def l2_distance(x1: float, y1: float, x2:float, y2:float):
    return sqrt(
        (x2-x1)**2 + (y2-y1)**2
    )