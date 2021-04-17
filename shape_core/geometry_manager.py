#
import time
import pyclipper as pc
import shapely.geometry as shg
from shapely.ops import cascaded_union

# import matplotlib.pyplot as plt
# from collections import OrderedDict as Od
from .plot_stuff import plot_polygons, plot_shapely
from .pyclipper2shapely import polytree_to_shapely

#
#
#

from OpenGL.GLU import *
# from OpenGL.GL import *
# from pygame.locals import *
# import pygame
# import sys


def merge_polygons_path(poly_set, as_list=False):
    merged = []

    use_shapely = True

    if not use_shapely:
        dark = poly_set
        dark_poly = []
        clear_poly = []
        to_merge = [g.exterior.coords for g in dark]
        if to_merge:
            dark_poly = _merge_polylist(to_merge)
            ito_merge = []
            for g in dark:
                ito_merge += [i.coords for i in g.interiors]
            if ito_merge:
                clear_poly = _merge_polylist(ito_merge)
            if clear_poly:
                geoms = _clip_polylist(clear_poly, dark_poly)
            else:
                geoms = dark_poly

            if geoms:
                tmp = [geoms.pop(0)]
                for l in geoms:
                    if not pc.Orientation(l):
                        # print("trovato FOROOOOO")
                        tmp.append(l)
                    else:
                        g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True).geom
                        #if len(tmp) > 1:
                        #    plot_polygons([g], color='green')
                        merged.append(g)
                        tmp = [l]
                if tmp:
                    g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True).geom
                    merged.append(g)
    else:
        for i, p in enumerate(poly_set):
            #print(list(p.exterior.coords))
            poly_set[i] = p = p.buffer(0)
            if not p.is_valid:
                print(list(p.exterior.coords))
                print(p.is_valid)
                plot_shapely([p])
        merged = cascaded_union(poly_set)
        if merged.geom_type != "MultiPolygon":
            merged = [merged]
        else:
            if as_list:
                merged = list(merged)
    return merged


def fill_holes_sh(poly_sh):
    if poly_sh.geom_type == "MultiPolygon":
        ret = shg.MultiPolygon(shg.Polygon(p.exterior.coords) for p in poly_sh.geoms)
    else:
        ret = shg.Polygon(poly_sh.exterior.coords)
    return ret


def get_poly_diameter(poly_sh):
    pl = [poly_sh]
    if poly_sh.geom_type == "MultiPolygon":
        pl = [p for p in poly_sh.geoms]
    diameters = []
    for p in pl:
        c = p.centroid
        r = get_max_distance(c, p.exterior.coords)
        diameters.append(2.0 * r)
    return diameters


def get_max_distance(c, pl):
    d_max = 0.0
    for p in pl:
        d = c.distance(shg.Point(p))
        d_max = max(d, d_max)
    return d_max


def offset_polygon(polyg, offset, shapely_poly=False):

    use_shapely = True

    if not use_shapely:
        # print("Polygon")
        t0 = time.time()
        if shapely_poly:
            poly = polyg
        else:
            poly = polyg.geom
        # if len(poly) > 1:
        #    print("IN MULTIPOLYGONS")

        ext = poly.exterior.coords
        mmp = [ext]
        for i in poly.interiors:
            g = shg.Polygon(i.coords)
            mmp.append(shg.polygon.orient(g, sign=1.0).exterior.coords)

        geoms = _offset_multiple_polylist(mmp, offset)

        merged = []

        if geoms:
            tmp = [geoms.pop(0)]
            for l in geoms:
                if not pc.Orientation(l):
                    tmp.append(l)
                else:
                    g = shg.Polygon(tmp.pop(0), holes=tmp)
                    merged.append(g)
                    tmp = [l]
            if tmp:
                g = shg.Polygon(tmp.pop(0), holes=tmp)
                merged.append(g)

        if len(merged) == 0:
            opoly = None
        elif len(merged) == 1:
            opoly = merged[0]
        else:
            opoly = shg.MultiPolygon(merged)

    else:
        if shapely_poly:
            opoly = polyg.buffer(offset)
        else:
            opoly = polyg.geom.buffer(offset)

    # print(type(opoly))

    t1 = time.time()
    # print("\t-Time " + str(t1-t0))

    return opoly


def offset_polygon_holes(poly, offset):
    res = []
    g = poly.geom
    for i in g.interiors:
        o = offset_polygon(shg.Polygon(i.coords), offset, shapely_poly=True)
        if o.geom_type == "MultiPolygon":
            res.extend(o.geoms)
        else:
            res.append(o)
    if len(res) > 1:
        return shg.MultiPolygon(res)
    else:
        return res[0]


def offset_polygon_old(polyg, offset, shapely_poly=False):

    use_shapely = True

    if not use_shapely:
        # print("Polygon")
        t0 = time.time()
        if shapely_poly:
            poly = polyg
        else:
            poly = polyg.geom
        ext = poly.exterior.coords
        tmp = _offset_polylist(ext, offset)
        oext = []
        if len(tmp) > 0:
            oext = tmp[0]
        oint = []
        for i in poly.interiors:
            tmp = _offset_polylist(i.coords, -offset)
            if len(tmp) > 0:
                oint.append(tmp[0])

        if oext:
            opoly = shg.Polygon(oext, holes=oint)
            opoly = shg.polygon.orient(opoly, sign=1.0)
            x, y = opoly.exterior.xy
        else:
            opoly = None
            print("[WARNING] OFFSET JUST HOLES")
            print(oint)
    else:
        if shapely_poly:
            opoly = polyg.buffer(offset)
        else:
            opoly = polyg.geom.buffer(offset)

    # print(type(opoly))

    t1 = time.time()
    # print("\t-Time " + str(t1-t0))

    return opoly


def _offset_polylist(mp, offset_in, scale=True):

    t0 = time.time()
    pco = pc.PyclipperOffset()
    polys = mp
    offset = offset_in

    # t1 = time.time()
    # print("Init Time: " + str(t1 - t0))
    if scale:
        polys = pc.scale_to_clipper(mp)
        offset = pc.scale_to_clipper(offset_in)

    # t2 = time.time()
    # print("Scale Time: " + str(t2 - t1))

    pco.AddPath(polys, pc.JT_MITER, pc.ET_CLOSEDPOLYGON)
    opoly = pco.Execute(offset)

    # t3 = time.time()
    # print("Exec Time: " + str(t3 - t2))

    results = []
    if scale:
        opoly = pc.scale_from_clipper(opoly)

    # t4 = time.time()
    # print("Scale Time: " + str(t4 - t3))

    results.extend([cp for cp in opoly])
    pco.Clear()

    # t5 = time.time()
    # print("Result Time: " + str(t5 - t4))

    return results


def _offset_multiple_polylist(mmp, offset_in, scale=True):

    t0 = time.time()
    pco = pc.PyclipperOffset()
    polysl = mmp

    # t1 = time.time()
    # print("Init Time: " + str(t1 - t0))
    offset = offset_in
    if scale:
        offset = pc.scale_to_clipper(offset_in)

    for polys in polysl:
        if scale:
            polys = pc.scale_to_clipper(polys)

        # t2 = time.time()
        # print("Scale Time: " + str(t2 - t1))

        pco.AddPath(polys, pc.JT_MITER, pc.ET_CLOSEDPOLYGON)

    opoly = pco.Execute(offset)

    # t3 = time.time()
    # print("Exec Time: " + str(t3 - t2))

    results = []
    if scale:
        opoly = pc.scale_from_clipper(opoly)

    # t4 = time.time()
    # print("Scale Time: " + str(t4 - t3))

    results.extend([cp for cp in opoly])
    pco.Clear()

    # t5 = time.time()
    # print("Result Time: " + str(t5 - t4))

    return results


def _merge_poly_set(poly_set, pure_merge=False):
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
        dark_poly_sh = _merge_polylist_shapely(to_merge)
        to_merge = [g.geom.exterior.coords for g in clear]

        if to_merge or pure_merge:
            to_merge += init_holes
            # se ci sono immagini clear
            # mi preparo per il clipping
            # ai fori che devo fare aggiungo quelli già calcolati dal merge precedente se ce ne sono
            if dark_poly_sh.geom_type == "MultiPolygon":
                for dk in dark_poly_sh:
                    dark_poly.append(dk.exterior.coords)
                    # aggiungo i fori dei darkpoly alle forme da sotrarre
                    for i in dk.interiors:
                        to_merge.append(i.coords)
            else:
                dark_poly = [dark_poly_sh.exterior.coords]
                # aggiungo i fori dei darkpoly alle forme da sotrarre
                for i in dark_poly_sh.interiors:
                    to_merge.append(i.coords)
            # ora in dark_poly ho solo i poligoni esterni
            # e in to_merge i fori clear + quelli creati nel merge precedente
            if to_merge:
                # print("Son QUI")
                dark_poly_sh = _clip_polylist_sh(to_merge, dark_poly)
            # if dark_poly_sh.geom_type == "MultiPolygon":
            #     plot_shapely(dark_poly_sh, color="green")
            # else:
            #     plot_shapely([dark_poly_sh], color="green")
        else:
            # sono solo immagini dark quindi ho già le geom pronte.
            # genero quindi i miei geom
            # if dark_poly_sh.geom_type == "MultiPolygon":
            #     plot_shapely(dark_poly_sh, color="blue")
            # else:
            #     plot_shapely([dark_poly_sh], color="blue")
            pass

        merged = []
        if dark_poly_sh.geom_type == "MultiPolygon":
            for dk in dark_poly_sh:
                tmp = [dk.exterior.coords]
                # aggiungo i fori dei darkpoly alle forme da sotrarre
                for i in dk.interiors:
                    tmp.append(i.coords)
                g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True)
                merged.append(g)
        else:
            tmp = [dark_poly_sh.exterior.coords]
            # aggiungo i fori dei darkpoly alle forme da sotrarre
            for i in dark_poly_sh.interiors:
                tmp.append(i.coords)
            g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True)
            merged.append(g)
        # tmp = [g.geom for g in merged]
        # plot_shapely(tmp, color="red")

    return merged


def merge_polygons(mp):
    others = []

    to_merge = []
    merged = []

    pre_pol = 'clear'
    poly_set = []

    for p in mp:
        if p.geom:
            # plot_shapely([p.geom])
            # print(p.polarity)
            if p.closed:
                # appendo nella lista tutti i poligoni chiusi fino a quando non ne incontro uno
                # clear, a quel punto faccio l'or dei poligoni dark e sottraggo quello clear
                # metto il risultato nella lista di poligoni trattati
                if p.polarity == 'dark':
                    if pre_pol == 'clear':
                        # generare i poligoni qui
                        # print(poly_set)
                        if poly_set:
                            merged += _merge_poly_set(poly_set)
                        poly_set = [[p], []]
                    else:
                        poly_set[0].append(p)
                elif p.polarity == 'clear':
                    poly_set[1].append(p)
                else:
                    print("[ERROR] Polarity not recognized")
                pre_pol = p.polarity
            else:
                others.append(p)

    print("Geom Collected")
    if poly_set[0]:
        merged += _merge_poly_set(poly_set)
    # tmp_p = [m.geom for m in merged]
    # plot_shapely(tmp_p, color="orange")

    print("Final Merging")

    # merged_final = _merge_poly_set([merged, []], pure_merge=True)

    merged_final = []
    tmp_p = [m.geom for m in merged]
    tmp_final = cascaded_union(tmp_p)
    if tmp_final.geom_type == "MultiPolygon":
        for f in tmp_final:
            tmp = [f.exterior.coords]
            # aggiungo i fori dei darkpoly alle forme da sotrarre
            for i in f.interiors:
                tmp.append(i.coords)
            g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True)
            merged_final.append(g)
    else:
        tmp = [tmp_final.exterior.coords]
        # aggiungo i fori dei darkpoly alle forme da sotrarre
        for i in tmp_final.interiors:
            tmp.append(i.coords)
        g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True)
        merged_final.append(g)

    layer = merged_final
    # tmp_p = [m.geom for m in layer]
    # plot_shapely(tmp_p)

    return layer, others


def _merge_polylist(mp, scale=True):

    pco = pc.Pyclipper()
    polys = mp

    if scale:
        polys = pc.scale_to_clipper(mp)

    results = []
    pco.AddPaths(polys, pc.PT_SUBJECT, True)
    clip_polys = pco.Execute(pc.CT_UNION, pc.PFT_NONZERO, pc.PFT_NONZERO)

    if scale:
        clip_polys = pc.scale_from_clipper(clip_polys)
    results.extend([cp for cp in clip_polys])
    pco.Clear()
    return results


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

    results = []
    pco.AddPaths(clip, pc.PT_CLIP, True)
    pco.AddPaths(subj, pc.PT_SUBJECT, True)
    sol_tree = pco.Execute2(pc.CT_DIFFERENCE, pc.PFT_EVENODD, pc.PFT_EVENODD)
    results = polytree_to_shapely(sol_tree, scale)
    pco.Clear()
    return results


def _clip_polylist(clip_in, subj_in, scale=True):

    pco = pc.Pyclipper()
    clip = clip_in
    if scale:
        clip = pc.scale_to_clipper(clip_in)
    subj = subj_in
    if scale:
        subj = pc.scale_to_clipper(subj_in)

    results = []
    pco.AddPaths(clip, pc.PT_CLIP, True)
    pco.AddPaths(subj, pc.PT_SUBJECT, True)
    sol = pco.Execute(pc.CT_DIFFERENCE, pc.PFT_EVENODD, pc.PFT_EVENODD)

    if scale:
        sol = pc.scale_from_clipper(sol)

    results.extend([cp for cp in sol])
    pco.Clear()
    return results


def get_bbox_area_sh(geom):
    # (minx, miny, maxx, maxy)
    bb = geom.bounds
    a = (bb[2] - bb[0]) * (bb[3] - bb[1])
    return a


class Geom:

    def __init__(self, gdata, complex=False):
        self.points = gdata['points']
        self.closed = gdata['closed']
        self.polarity = gdata['polarity']
        self.complex = complex
        self.geom = self._make_geom()

    def _make_geom(self):
        # print("Make Geometry")
        geom = None
        if self.points:
            if self.closed:
                if self.complex:
                    # print("Complex")
                    pts = self.points[:]
                    ext = pts.pop(0)
                    holes = pts
                    geom = shg.Polygon(ext, holes=holes)
                    geom = shg.polygon.orient(geom, sign=1.0)
                    x, y = geom.exterior.xy
                else:
                    geom = shg.Polygon(self.points)
                    geom = shg.polygon.orient(geom, sign=1.0)
                    x, y = geom.exterior.xy
            else:
                geom = shg.LineString(self.points)
                x, y, = geom.xy
        return geom

