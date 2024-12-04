import numpy as np

def transform2rgb(sm: np.ndarray):
    if sm.ndim == 3:
        # Assuming the array has one channel
        sm = sm[0]

    sm = sm[:, :, None].repeat(3, axis=-1)
    sm_map = sm.copy()

    # Red
    indexes_0, indexes_1, _ = np.where(sm <= .3)
    sm_map[indexes_0, indexes_1] = (255, 0, 0)

    # Yellow
    indexes_0, indexes_1, _ = np.where((sm > .3) & (sm <= .5))
    sm_map[indexes_0, indexes_1] = (255, 255, 0)

    # Green
    indexes_0, indexes_1, _ = np.where((sm > .5) & (sm <= .8))
    sm_map[indexes_0, indexes_1] = (0, 255, 0)

    # Blue
    indexes_0, indexes_1, _ = np.where(sm > .8)
    sm_map[indexes_0, indexes_1] = (0, 0, 255)
    
    return sm_map
