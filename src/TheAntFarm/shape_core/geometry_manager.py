import logging
import time

import pyclipper as pc
import shapely.geometry
import shapely.geometry as shg
from shapely.errors import GEOSException
from shapely.ops import unary_union

from .pyclipper2shapely import polytree_to_shapely

logger = logging.getLogger(__name__)

# Tolerance used when simplifying the offset polygons: it removes the redundant
# vertices produced by the buffer operation (1 um, well below any tool size).
SIMPLIFY_TOLERANCE = 0.001


def merge_polygons_path(poly_set):
    """Merge a set of closed paths into non overlapping polygons.

    Every path is repaired with ``buffer(0)`` before the union, so invalid
    self-intersecting geometries coming from the CAM do not abort the merge.
    The input list is not modified.
    """
    polygons = [p.buffer(0) for p in poly_set]
    merged = unary_union(polygons)
    if merged.geom_type != "MultiPolygon":
        return [merged]
    return list(merged.geoms)


def fill_holes_sh(poly_sh):
    if poly_sh.geom_type == "MultiPolygon":
        ret = shg.MultiPolygon(shg.Polygon(p.exterior.coords) for p in poly_sh.geoms)
    else:
        ret = shg.Polygon(poly_sh.exterior.coords)
    return ret


def get_poly_parts(poly_sh):
    """Return the list of Polygon parts that compose ``poly_sh``.

    The order is stable, so the returned list can be zipped with the list
    returned by :func:`get_poly_diameter`.

    Parameters
    ----------
    poly_sh : shapely.geometry.Polygon | shapely.geometry.MultiPolygon | None

    Returns
    -------
    list of shapely.geometry.Polygon
        One element for a Polygon, one element for each part of a MultiPolygon
        and an empty list for empty or unsupported geometries.
    """
    if poly_sh is None or poly_sh.is_empty:
        return []
    if poly_sh.geom_type == "MultiPolygon":
        return list(poly_sh.geoms)
    if poly_sh.geom_type == "Polygon":
        return [poly_sh]
    return []


def get_poly_diameter(poly_sh):
    """Inscribed diameter of every part of ``poly_sh``, in drawing units.

    The value is computed as ``2 * distance(centroid, boundary)``, i.e. the
    diameter of the biggest round tool that surely fits inside the part: this is
    the correct value to choose a drill bit for the hole.

    It replaces the circumscribed diameter (``2 * max distance from the
    centroid``), which on non circular holes (slots, obrounds, rectangles) is
    larger than the hole width and could select an oversized bit.

    Notes
    -----
    The centroid is used as an approximation of the centre of the inscribed
    circle: the returned diameter is never larger than the circumscribed one and
    for a regular part it matches the real inscribed diameter.

    Parameters
    ----------
    poly_sh : shapely.geometry.Polygon | shapely.geometry.MultiPolygon | None

    Returns
    -------
    list of float
        One diameter for each part, in the same order of :func:`get_poly_parts`.
        Degenerate parts give ``0.0``.
    """
    diameters = []
    for p in get_poly_parts(poly_sh):
        if p.area <= 0.0:
            diameters.append(0.0)
            continue
        diameters.append(2.0 * p.centroid.distance(p.boundary))
    return diameters


def offset_polygon(polyg, offset, shapely_poly=False):
    """Offset a polygon (positive values grow it, negative values shrink it).

    Parameters
    ----------
    polyg : Geom | shapely.geometry.Polygon
        Geometry to offset: a ``Geom`` wrapper unless ``shapely_poly`` is True.
    offset : float
        Offset distance in drawing units.
    shapely_poly : bool
        True when ``polyg`` is already a shapely geometry.

    Returns
    -------
    shapely.geometry.Polygon | shapely.geometry.MultiPolygon
        The offset geometry, simplified at :data:`SIMPLIFY_TOLERANCE`.
    """
    if shapely_poly:
        opoly = polyg.buffer(offset)
    else:
        opoly = polyg.geom.buffer(offset)

    return opoly.simplify(SIMPLIFY_TOLERANCE, preserve_topology=True)


def offset_polygon_holes(poly, offset):
    """Offset the holes of ``poly`` and return them as a single geometry.

    Parameters
    ----------
    poly : Geom
        Geometry whose holes must be offset.
    offset : float
        Offset applied to every hole (negative values shrink the holes).

    Returns
    -------
    shapely.geometry.Polygon | shapely.geometry.MultiPolygon | None
        ``None`` when the polygon has no holes or when every hole disappears
        after the offset (offset larger than the hole itself).
    """
    if poly is None or poly.geom is None:
        return None

    res = []
    for i in poly.geom.interiors:
        o = offset_polygon(shg.Polygon(i.coords), offset, shapely_poly=True)
        if o is None or o.is_empty:
            # the hole disappeared with this offset
            continue
        if o.geom_type == "MultiPolygon":
            res.extend(o.geoms)
        else:
            res.append(o)

    if not res:
        return None
    if len(res) > 1:
        return shg.MultiPolygon(res)
    return res[0]


def _merge_poly_set(poly_set, pure_merge=False):
    """Merge the dark polygons of a layer and subtract the clear ones."""
    merged = []
    dark = poly_set[0]
    clear = poly_set[1]
    dark_poly = []
    to_merge = [g.geom.exterior.coords for g in dark]
    init_holes = []
    for g in dark:
        for i in g.geom.interiors:
            init_holes.append(i.coords)

    if to_merge:
        start_time = time.perf_counter()
        dark_poly_sh = _merge_polylist_shapely(to_merge)
        logger.debug(f"Dark polygons merged in {time.perf_counter() - start_time:.4f} s")
        to_merge = [g.geom.exterior.coords for g in clear]

        if to_merge or pure_merge:
            to_merge += init_holes
            # if there are clear image
            # get ready for clipping
            # of the whole holes
            if dark_poly_sh.geom_type == "MultiPolygon":
                for dk in dark_poly_sh.geoms:
                    dark_poly.append(dk.exterior.coords)
                    # add the holes of the darkpoly to the shapes to be subtracted
                    for i in dk.interiors:
                        to_merge.append(i.coords)
            else:
                dark_poly = [dark_poly_sh.exterior.coords]
                # add the holes of the darkpoly to the shapes to be subtracted
                for i in dark_poly_sh.interiors:
                    to_merge.append(i.coords)
            # now in dark_poly there are external polygon only
            # in to_merge there are clear holes plus the ones from the previous merge
            if to_merge:
                dark_poly_sh = _clip_polylist_sh(to_merge, dark_poly)
        else:
            # just dark images so the geoms are ready, no boolean operation needed
            pass

        merged = []
        if dark_poly_sh.geom_type == "MultiPolygon":
            for dk in dark_poly_sh.geoms:
                tmp = [dk.exterior.coords]
                # add the holes of the darkpoly to the shapes to be subtracted
                for i in dk.interiors:
                    tmp.append(i.coords)
                g = Geom({"points": tmp, "polarity": "dark", "closed": True}, complex=True)
                merged.append(g)
        else:
            tmp = [dark_poly_sh.exterior.coords]
            # add the holes of the darkpoly to the shapes to be subtracted
            for i in dark_poly_sh.interiors:
                tmp.append(i.coords)
            g = Geom({"points": tmp, "polarity": "dark", "closed": True}, complex=True)
            merged.append(g)
    return merged


def merge_polygons(mp):
    """Merge a layer of Geom objects, applying the dark/clear polarity.

    Returns
    -------
    tuple of (list of Geom, list of Geom)
        The merged closed geometries and the open ones, which are not part of
        the filling area.
    """
    start_time = time.perf_counter()
    others = []

    merged = []

    pre_pol = "clear"
    poly_set = []

    for p in mp:
        if p.geom:
            if p.closed:
                # append closed polygon to the list until found a clear one.
                # at this point, merge all the polygons in the list and subtract
                # the clear one, putting the result in the treated polygons list
                if p.polarity == "dark":
                    if pre_pol == "clear":
                        # merge all polygons in the list
                        if poly_set:
                            merged += _merge_poly_set(poly_set)
                        poly_set = [[p], []]
                    else:
                        poly_set[0].append(p)
                elif p.polarity == "clear":
                    poly_set[1].append(p)
                else:
                    logger.error(f"Polarity not recognized: {p.polarity}")

                pre_pol = p.polarity
            else:
                others.append(p)
    logger.debug(f"Geometries collected in {time.perf_counter() - start_time:.4f} s")

    if len(poly_set) > 0:
        if poly_set[0]:
            merged += _merge_poly_set(poly_set)

    logger.debug("Final merging")
    start_time = time.perf_counter()

    merged_final = []
    tmp_p = [m.geom for m in merged]
    tmp_final = unary_union(tmp_p)
    if tmp_final.geom_type == "MultiPolygon":
        for f in tmp_final.geoms:
            tmp = [f.exterior.coords]
            # add the holes of the darkpoly to the shapes to be subtracted
            for i in f.interiors:
                tmp.append(i.coords)
            g = Geom({"points": tmp, "polarity": "dark", "closed": True}, complex=True)
            merged_final.append(g)
    else:
        if tmp_final:
            tmp = [tmp_final.exterior.coords]
            # add the holes of the darkpoly to the shapes to be subtracted
            for i in tmp_final.interiors:
                tmp.append(i.coords)
            g = Geom({"points": tmp, "polarity": "dark", "closed": True}, complex=True)
            merged_final.append(g)

    layer = merged_final
    logger.debug(f"Final merging done in {time.perf_counter() - start_time:.4f} s")

    return layer, others


def _merge_polylist_shapely(mp, scale=True):
    pco = pc.Pyclipper()
    polys = mp

    if scale:
        polys = pc.scale_to_clipper(mp)

    pco.AddPaths(polys, pc.PT_SUBJECT, True)
    sol_tree = pco.Execute2(pc.CT_UNION, pc.PFT_NONZERO, pc.PFT_NONZERO)
    results = polytree_to_shapely(sol_tree, scale)
    pco.Clear()
    return results


def _clip_polylist_sh(clip_in, subj_in, scale=True):

    pco = pc.Pyclipper()
    clip = clip_in
    if scale:
        clip = pc.scale_to_clipper(clip_in)
    subj = subj_in
    if scale:
        subj = pc.scale_to_clipper(subj_in)

    pco.AddPaths(clip, pc.PT_CLIP, True)
    pco.AddPaths(subj, pc.PT_SUBJECT, True)
    sol_tree = pco.Execute2(pc.CT_DIFFERENCE, pc.PFT_EVENODD, pc.PFT_EVENODD)
    results = polytree_to_shapely(sol_tree, scale)
    pco.Clear()
    return results


def get_bbox_area_sh(geom):
    # (x_min, y_min, x_max, y_max)
    bb = geom.bounds
    a = (bb[2] - bb[0]) * (bb[3] - bb[1])
    return a


def is_overlaping_multiple_polygons(polygon, polygon_list, shapely_poly=False):
    # evaluate if polygon overlap one or more polygons in polygon_list

    if shapely_poly:
        diff_polys = polygon_list.difference(polygon)
    else:
        sh_poly = polygon.geom
        sh_poly_list = [p.geom for p in polygon_list]
        sh_mpoly = shapely.geometry.MultiPolygon(sh_poly_list)
        diff_polys = sh_mpoly.difference(sh_poly)

    diff_len = 0
    poly_len = 0

    if diff_polys.geom_type == "MultiPolygon":
        diff_len = len(diff_polys.geoms)
    elif diff_polys.geom_type == "Polygon":
        diff_len = 1
    else:
        logger.warning("Invalid Diff Polygons Type %s" % diff_polys.geom_type)

    if polygon_list.geom_type == "MultiPolygon":
        poly_len = len(polygon_list.geoms)
    elif polygon_list.geom_type == "Polygon":
        poly_len = 1
    else:
        logger.warning("Invalid Polygon List Type %s" % diff_polys.geom_type)

    return diff_len < poly_len - 1


class Geom:
    """A geometry read from a Gerber/Excellon file, with its polarity.

    Parameters
    ----------
    gdata : mapping
        ``{"points": [...], "closed": bool, "polarity": "dark" | "clear"}``.
    complex : bool
        True when ``points`` is a list of rings: the first one is the exterior
        ring, the others are the holes.

    Raises
    ------
    ValueError
        When the points do not describe a valid geometry (a closed path needs
        at least three distinct points). The message reports the shape of the
        data, so that the primitive that produced it can be identified.
    """

    def __init__(self, gdata, complex=False):
        self.points = list(gdata["points"]) if gdata.get("points") else []
        self.closed = gdata["closed"]
        self.polarity = gdata["polarity"]
        self.complex = complex
        self.geom = self._make_geom()

    @classmethod
    def from_shapely(cls, geom, polarity: str = "dark", complex: bool = True) -> "Geom":
        """Build a Geom from an existing shapely geometry, without converting it.

        Used for the geometries produced by the gerbyx parser, which are already
        shapely polygons.
        """
        if geom is None:
            raise ValueError("Cannot build a Geom from a None geometry")
        if geom.geom_type == "Polygon":
            points = [geom.exterior.coords] + [interior.coords for interior in geom.interiors]
        elif geom.geom_type == "LineString":
            points = [list(geom.coords)]
        else:
            raise ValueError(f"Unsupported geometry type: {geom.geom_type} (split a MultiPolygon with get_poly_parts)")

        obj = cls.__new__(cls)
        obj.points = points
        obj.closed = geom.geom_type == "Polygon"
        obj.polarity = polarity
        obj.complex = complex
        obj.geom = geom
        return obj

    def _make_geom(self):
        if not self.points:
            return None
        try:
            if self.closed:
                if self.complex:
                    rings = list(self.points)
                    geom = shg.Polygon(rings[0], holes=rings[1:])
                else:
                    geom = shg.Polygon(self.points)
                return shg.polygon.orient(geom, sign=1.0)
            return shg.LineString(self.points)
        except (ValueError, TypeError, GEOSException) as exc:
            kind = "polygon" if self.closed else "line"
            raise ValueError(
                f"Invalid {kind} geometry: {len(self.points)} points, "
                f"complex={self.complex}, first point={self.points[0]!r}: {exc}"
            ) from exc

    def __repr__(self) -> str:
        kind = "polygon" if self.closed else "line"
        return f"Geom({kind}, polarity={self.polarity!r}, points={len(self.points)})"
