import numpy as np

def generate_lane_points(lane, x_start=-10.0, x_end=130.0, step=0.25,):

    x = np.arange(
        x_start,
        x_end,
        step,
    )

    y = (
        lane.a
        + lane.b * x
        + lane.c * x**2
        + lane.d1 * x**3
    )

    return x, y