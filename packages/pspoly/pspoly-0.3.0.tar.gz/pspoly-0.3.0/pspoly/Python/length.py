import numpy as _np

from scipy.optimize import curve_fit as _curve_fit

from . import filters as _filters

dl = _np.array([0., 0.70710678, 0.5, 0.5, 0.70710678, 1.41421356, 0.5, 0.5, 0.5, 1.20710678, 1., 1., 0.5, 1.20710678, 1., 1., 0.70710678, 1.41421356, 1.20710678, 1.20710678, 1.41421356, 2.12132034, 1.20710678, 1.20710678, 0.5, 1.20710678, 1., 1., 0.5, 1.20710678, 1., 1., 0.5, 1.20710678, 1., 1., 1.20710678, 1.91421356, 1., 1., 1., 1.70710678, 1.5, 1.5, 1., 1.70710678, 1.5, 1.5, 0.5, 1.20710678, 1., 1., 1.20710678, 1.91421356, 1., 1., 1., 1.70710678, 1.5, 1.5, 1., 1.70710678, 1.5, 1.5, 0.70710678, 1.41421356, 1.20710678, 1.20710678, 1.41421356, 2.12132034, 1.20710678, 1.20710678, 1.20710678, 1.91421356, 1.70710678, 1.70710678, 1.20710678, 1.91421356, 1.70710678, 1.70710678, 1.41421356, 2.12132034, 1.91421356, 1.91421356, 2.12132034, 2.82842712, 1.91421356, 1.91421356, 1.20710678, 1.91421356, 1.70710678, 1.70710678, 1.20710678, 1.91421356, 1.70710678, 1.70710678, 0.5, 1.20710678, 1., 1., 1.20710678, 1.91421356, 1., 1., 1., 1.70710678, 1.5, 1.5, 1., 1.70710678, 1.5, 1.5, 0.5, 1.20710678, 1., 1., 1.20710678, 1.91421356, 1., 1., 1., 1.70710678, 1.5, 1.5, 1., 1.70710678, 1.5, 1.5, 0.5, 0.5, 1., 1., 1.20710678, 1.20710678, 1., 1., 1., 1., 1.5, 1.5, 1., 1., 1.5, 1.5, 1.20710678, 1.20710678, 1.70710678, 1.70710678, 1.91421356, 1.91421356, 1.70710678, 1.70710678, 1., 1., 1.5, 1.5, 1., 1., 1.5, 1.5, 1., 1., 1.5, 1.5, 1.70710678, 1.70710678, 1.5, 1.5, 1.5, 1.5, 2., 2., 1.5, 1.5, 2., 2., 1., 1., 1.5, 1.5, 1.70710678, 1.70710678, 1.5, 1.5, 1.5, 1.5, 2., 2., 1.5, 1.5, 2., 2., 0.5, 0.5, 1., 1., 1.20710678, 1.20710678, 1., 1., 1., 1., 1.5, 1.5, 1., 1., 1.5, 1.5, 1.20710678, 1.20710678, 1.70710678, 1.70710678, 1.91421356, 1.91421356, 1.70710678, 1.70710678, 1., 1., 1.5, 1.5, 1., 1., 1.5, 1.5, 1., 1., 1.5, 1.5, 1.70710678, 1.70710678, 1.5, 1.5, 1.5, 1.5, 2., 2., 1.5, 1.5, 2., 2., 1., 1., 1.5, 1.5, 1.70710678, 1.70710678, 1.5, 1.5, 1.5, 1.5, 2., 2., 1.5, 1.5, 2., 2.])

def contour(dat):
    img = dat.get_img()
    encoded = _filters.encode(img)

    length = 0
    for iy in range(img.shape[0]):
        for ix in range(img.shape[1]):
            length += dl[encoded[iy,ix]]
    return length*dat.get_px_size()

def end_to_end(dat):
    img = dat.get_img()
    encoded = _filters.encode(img)

    endpts = []
    for iy in range(img.shape[0]):
        for ix in range(img.shape[1]):
            if encoded[iy,ix] in _filters.end_patterns: endpts.append([iy,ix])
    if len(endpts) == 2:
        return dat.get_px_size()*((endpts[1][0] - endpts[0][0])**2 + (endpts[1][1] - endpts[0][1])**2)**(1/2)
    elif len(endpts) < 2:
        return 0
    else:
        lengths = [[((pt1[0] - pt0[0])**2 + (pt1[1] - pt0[1])**2)**(1/2) for pt0 in endpts] for pt1 in endpts]
        return dat.get_px_size()*_np.max(lengths)

def wormlike_chain(cl,pl):
    return 4*pl*cl*(1-2*pl/cl*(1-_np.exp(-cl/(2*pl))))

def Lp(data):
    cl = [contour(n) for n in data]
    eel2 = [end_to_end(n)**2 for n in data]
    popt, pcov = _curve_fit(wormlike_chain,cl,eel2)
    return popt[0]

import matplotlib.pyplot as plt

def plot(data):
    cl = [contour(n) for n in data]
    eel2 = [end_to_end(n)**2 for n in data]
    popt, pcov = _curve_fit(wormlike_chain,cl,eel2)

    x = _np.linspace(1,60)
    y2 = wormlike_chain(x,popt[0])

    fig, ax = plt.subplots()
    ax.scatter(cl,_np.sqrt(eel2))
    ax.plot(x,_np.sqrt(y2))

    plt.show()