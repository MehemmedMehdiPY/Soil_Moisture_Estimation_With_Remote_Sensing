import numpy as np

def get_wavenumber(wave_length: float):
    return 2 * np.pi / wave_length

def get_surface_roughness(bs_coef_diff: float, A: float = 4.27, B: float = .22):
    """
    bs_coef:      Backscattering coefficient difference. VH - VV
    """
    sr = A + B * bs_coef_diff
    
    # Replacing negative outliers
    sr_min = sr[sr >= 0].min()
    sr[sr < sr_min] = sr_min
    
    return sr
    
def retrieve_sm(sp: float):
    """
    Retrieve sm (soil moisture) from sp (soil permittivity)
    Based on Equation - 4
    """
    sm = -5.3 * 10 ** -2 + 2.92 * 10 ** -2 * sp - 5.5 * 10 ** -4 * sp ** 2 + 4.3 * 10 ** -6 * sp ** 3
    return sm

def Dubois(vv, vh, angle, wave_length=5.625, eps=1e-16):

    # Converting into decibels
    vv_decibel = 10 * np.log10(vv + .001)
    vh_decibel = 10 * np.log10(vh + .001)
    sr = get_surface_roughness(vh_decibel - vv_decibel)
    
    k = get_wavenumber(wave_length)
    denominator = (wave_length ** .7 \
                * (k * sr * np.sin(angle) ** 3) ** 1.1 \
                * 10 ** -2.35 \
                * (np.cos(angle) ** 3) / np.sin(angle)
                )
    ratio = np.log((vv / denominator) + eps) / np.log(10)

    # Soil Permittivity
    sp = ratio / 0.046 / np.tan(angle)
    
    # Soil Moisture
    sm = retrieve_sm(sp)
    
    return sm
