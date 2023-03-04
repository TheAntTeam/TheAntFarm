# FROM: https://www.programcreek.com/python/?code=tilezen%2Fmapbox-vector-tile%2Fmapbox-vector-tile-master%2Fmapbox_vector_tile%2Fpolygon.py
# LICENSE: MIT

import pyclipper as pc
import shapely.geometry as shg
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.validation import explain_validity


def _generate_polys(contours, scale):
    """
    Generator which yields a valid polygon for each contour input.
    """

    for c in contours:
        p = _contour_to_poly(c, scale)
        yield p


def _union_in_blocks(contours, block_size, scale):
    """
    Generator which yields a valid shape for each block_size multiple of
    input contours. This merges together the contours for each block before
    yielding them.
    """

    n_contours = len(contours)
    for i in range(0, n_contours, block_size):
        j = min(i + block_size, n_contours)

        inners = []
        for c in contours[i:j]:
            p = _contour_to_poly(c, scale)
            if p.type == 'Polygon':
                inners.append(p)
            elif p.type == 'MultiPolygon':
                inners.extend(p.geoms)
        holes = unary_union(inners)
        assert holes.is_valid

        yield holes


def _contour_to_poly(contour_in, scale):
    contour = contour_in
    if scale:
        contour = pc.scale_from_clipper(contour_in)
    poly = Polygon(contour)
    if not poly.is_valid:
        poly = poly.buffer(0)
    assert poly.is_valid, \
        "Contour %r did not make valid polygon %s because %s" \
        % (contour, poly.wkt, explain_validity(poly))
    return poly


def _polytree_node_to_shapely(node, scale):
    """
    Recurses down a Clipper PolyTree, extracting the results as Shapely
    objects.

    Returns a tuple of (list of polygons, list of children)
    """

    polygons = []
    children = []
    for ch in node.Childs:
        p, c = _polytree_node_to_shapely(ch, scale)
        polygons.extend(p)
        children.extend(c)

    if node.IsHole:
        # check expectations: a node should be a hole, _or_ return children.
        # this is because children of holes must be outers, and should be on
        # the polygons list.
        assert len(children) == 0
        if node.Contour:
            children = [node.Contour]
        else:
            children = []

    elif node.Contour:
        poly = _contour_to_poly(node.Contour, scale)

        # we add each inner one-by-one so that we can reject them individually
        # if they cause the polygon to become invalid. if the shape has lots
        # of inners, then this can mean a proportional amount of work, and may
        # take 1,000s of seconds. instead, we can group inners together, which
        # reduces the number of times we call the expensive 'difference'
        # method.
        block_size = 200
        if len(children) > block_size:
            inners = _union_in_blocks(children, block_size, scale)
        else:
            inners = _generate_polys(children, scale)

        for inner in inners:
            # the difference of two valid polygons may fail, and in this
            # situation we'd like to be able to display the polygon anyway.
            # so we discard the bad inner and continue.
            #
            # see test_polygon_inners_crossing_outer for a test case.
            try:
                diff = poly.difference(inner)
            except Exception:
                continue

            if not diff.is_valid:
                diff = diff.buffer(0)

            # keep this for when https://trac.osgeo.org/geos/ticket/789 is
            # resolved.
            #
            #  assert diff.is_valid, \
            #      "Difference of %s and %s did not make valid polygon %s " \
            #      " because %s" \
            #      % (poly.wkt, inner.wkt, diff.wkt, explain_validity(diff))
            #
            # NOTE: this throws away the inner ring if we can't produce a
            # valid difference. not ideal, but we'd rather produce something
            # that's valid than nothing.
            if diff.is_valid:
                poly = diff

        assert poly.is_valid
        if poly.type == 'MultiPolygon':
            polygons.extend(poly.geoms)
        else:
            polygons.append(poly)
        children = []

    else:
        # check expectations: this branch gets executed if this node is not a
        # hole, and has no contour. in that situation we'd expect that it has
        # no children, as it would not be possible to subtract children from
        # an empty outer contour.
        assert len(children) == 0

    return (polygons, children)


def _polytree_to_shapely(tree, scale):
    polygons, children = _polytree_node_to_shapely(tree, scale)

    # expect no left over children - should all be incorporated into polygons
    # by the time recursion returns to the root.
    assert len(children) == 0

    union = unary_union(polygons)
    assert union.is_valid
    return union


def polytree_to_shapely(tree, scale):
    res = _polytree_to_shapely(tree, scale)
    # reso = []
    # for p in res:
    #     reso.append(shg.polygon.orient(p, sign=1.0))
    # if len(reso) == 1:
    #     return reso[0]
    # else:
    #     return shg.MultiPolygon(reso)
    return res
