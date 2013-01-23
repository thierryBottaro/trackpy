import numpy as np
from scipy import special
import lmfit

def setup_params(angle):
    """The fit parameters' bounds depend on the range of the angle data.
    
    Parameters
    ----------
    angle -- an array-like sequence of angle values

    Returns
    -------
    params -- Parameters object with correct bounds
    """
    pi = np.pi
    params = lmfit.Parameters()
    params.add('m', value=1.5, min=0)
    params.add('C', value=1.0, min=0)
    params.add('offset', -0.05) # specify bounds below 
    params.add('theta0_plus_offset', 0.1, min=0, max=0.2) # bounding utility 
    params.add('theta0', expr='theta0_plus_offset - offset')

    offset = params['offset']
    angle_min, angle_max = angle.min(), angle.max()
    assert angle_min.size == 1, "argument must be a 1D sequence"
    offset.min, offset.max = -pi/2 - angle_min, pi/2 - angle_max
    return params

def power_fluid(angle, params):
    m = params['m'].value
    C = params['C'].value
    theta0 = params['theta0'].value
    offset = params['offset'].value
    _validate(angle, m, C, theta0, offset)
    term1 = 1/(m-1)*C**m*\
        np.cos(angle + offset)**(1-m)*_F(angle + offset, m)
    term2 = 1/(m-1)*C**m*\
        np.cos(theta0 + offset)**(1-m)*_F(theta0 + offset, m)
    return term1 + term2

def _validate(angle, m, C, theta0, offset):
    assert C >= 0, (
        "C = {} < 0 is not physical.").format(C)
    assert m >= 0, (
        "m < 0 is not physical.").format(m)
    assert m != 1, (
        """m == 1 means that the flow index n is also 1.
           This model diverges, but a purely viscous one should work.""")
    assert np.all(np.cos(angle + offset) >= 0), "cos(angle + offset) < 0"
    assert np.all(np.cos(angle + offset) >= 0), "cos(angle + offset) < 0"
    assert np.all(np.cos(theta0 + offset) >= 0), "cos(theta0 + offset) < 0"

def _F(angle, m):
    "Convenience function"
    # _2F_1(1/2, (1-m)/2; (3-m)/2, cos^2(theta))
    result = special.hyp2f1(0.5, (1-m)/2, (3-m)/2, np.cos(angle)**2)
    assert np.isfinite(result).all(), (
        """Hypergeometric function returned a result that is not finite.
        m={}
        result={}""".format(m, result))
    return result
