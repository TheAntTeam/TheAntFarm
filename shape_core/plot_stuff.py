from matplotlib import pyplot
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from numpy import asarray, concatenate, ones
from shapely.geometry import *


def ring_coding(ob):
    # The codes will be all "LINETO" commands, except for "MOVETO"s at the
    # beginning of each subpath
    n = len(ob.coords)
    codes = ones(n, dtype=Path.code_type) * Path.LINETO
    codes[0] = Path.MOVETO
    return codes


def pathify(polygon):
    # Convert coordinates to path vertices. Objects produced by Shapely's
    # analytic methods have the proper coordinate order, no need to sort.
    vertices = concatenate(
                    [asarray(polygon.exterior)]
                    + [asarray(r) for r in polygon.interiors])
    codes = concatenate(
                [ring_coding(polygon.exterior)]
                + [ring_coding(r) for r in polygon.interiors])
    return Path(vertices, codes)


def plot_vertices(vertices):
    fig, ax = pyplot.subplots(1, 1)
    ax.plot(vertices)
    pyplot.show()


def plot_lines(ll1, ll2=None):
    # plotta line strings
    fig, ax = pyplot.subplots(1, 1)
    for l in ll1:
        x, y = l.xy
        ax.plot(x, y, 'k')
    if ll2 is not None:
        for l in ll2:
            x, y = l.xy
            ax.plot(x, y, 'w')
    ax.set_aspect('equal')
    pyplot.show()


def plot_polygons(poly_list, color=None):

    fig, ax = pyplot.subplots(1, 1)

    xl = []
    yl = []

    for polygon in poly_list:
        if polygon.geom is not None:
            x, y = polygon.geom.exterior.xy

            xl += x
            yl += y

            path = pathify(polygon.geom)
            if color is not None:
                patch = PathPatch(path, facecolor=color, edgecolor=color)
            else:
                patch = PathPatch(path, facecolor='#cccccc', edgecolor='#999999')
            ax.add_patch(patch)
        else:
            print("[WARNING] poly with None geom")

    xmin = min(xl)
    xmax = max(xl)
    ymin = min(yl)
    ymax = max(yl)

    deltax = xmax - xmin
    deltay = ymax - ymin

    ax.set_xlim(xmin - abs(deltax*0.1), xmax + abs(deltax*0.1))
    ax.set_ylim(ymin - abs(deltay*0.1), ymax + abs(deltay*0.1))
    ax.set_aspect('equal', 'box')
    fig.tight_layout()

    pyplot.show()


def plot_shapely(poly_list, color=None):

    fig, ax = pyplot.subplots(1, 1)

    xl = []
    yl = []

    try:
        print(poly_list.geom_type)
    except:
        print("polyList")

    for poly in poly_list:
        if poly is not None:
            # print("Sub Polygon Type")
            # print(poly.geom_type)
            x, y = poly.exterior.xy

            xl += x
            yl += y

            path = pathify(poly)
            if color is not None:
                patch = PathPatch(path, facecolor=color, edgecolor='#999999')
            else:
                patch = PathPatch(path, facecolor='#cccccc', edgecolor='#999999')
            ax.add_patch(patch)
        else:
            print("[WARNING] poly with None geom")

    # print(xl)
    # print(len(xl))
    # print(yl)
    # print(len(yl))

    xmin = min(xl)
    xmax = max(xl)
    ymin = min(yl)
    ymax = max(yl)

    # print("X " + str(xmax) + " - " + str(xmin))
    # print("Y " + str(ymax) + " - " + str(ymin))

    deltax = xmax - xmin
    deltay = ymax - ymin

    # ax.set_xlim(xmin - abs(deltax*0.1), xmax + abs(deltax*0.1))
    # ax.set_ylim(ymin - abs(deltay*0.1), ymax + abs(deltay*0.1))
    ax.set_aspect('equal', 'box')
    ax.autoscale()
    # fig.tight_layout()

    pyplot.show()


def plot_paths(grb_list, path_lists, grb_color=None, path_color=None):
    # poly_list types
    fig, ax = pyplot.subplots(1, 1)

    xl = []
    yl = []

    for polygon in grb_list:
        if polygon is not None:
            x, y = polygon.exterior.xy

            xl += x
            yl += y

            path = pathify(polygon)
            if grb_color is not None:
                patch = PathPatch(path, facecolor=grb_color, edgecolor=grb_color)
            else:
                patch = PathPatch(path, facecolor='#cccccc', edgecolor='#999999')
            ax.add_patch(patch)
        else:
            print("[WARNING] poly with None geom")

    for path_list in path_lists:
        for polygon in path_list:
            if polygon is not None:

                x, y = polygon.exterior.xy

                xl += x
                yl += y

                path = pathify(polygon)
                if path_color is not None:
                    patch = PathPatch(path, facecolor='none', edgecolor=path_color)
                else:
                    patch = PathPatch(path, facecolor='none', edgecolor='#999999')
                patch.set_linewidth(0.5)
                ax.add_patch(patch)
            else:
                print("[WARNING] poly with None geom")

    xmin = min(xl)
    xmax = max(xl)
    ymin = min(yl)
    ymax = max(yl)

    deltax = xmax - xmin
    deltay = ymax - ymin

    ax.set_xlim(xmin - abs(deltax*0.1), xmax + abs(deltax*0.1))
    ax.set_ylim(ymin - abs(deltay*0.1), ymax + abs(deltay*0.1))
    ax.set_aspect('equal', 'box')
    fig.tight_layout()

    pyplot.show()