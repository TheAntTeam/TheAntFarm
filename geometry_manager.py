#
import pyclipper as pc
import shapely.geometry as shg
# import matplotlib.pyplot as plt
# from collections import OrderedDict as Od
# from plot_stuff import plot_polygons

#
#
#

from OpenGL.GLU import *
# from OpenGL.GL import *
# from pygame.locals import *
# import pygame
# import sys


def _merge_poly_set(poly_set):
    merged = []
    dark = poly_set[0]
    clear = poly_set[1]
    dark_poly = []
    clear_poly = []
    to_merge = [g.geom.exterior.coords for g in dark]
    if to_merge:
        dark_poly = _merge_polylist(to_merge)
        to_merge = [g.geom.exterior.coords for g in clear]
        if to_merge:
            clear_poly = _merge_polylist(to_merge)
        if clear_poly:
            geoms = _clip_polylist(clear_poly, dark_poly)
        else:
            geoms = dark_poly

        if geoms:
            tmp = [geoms.pop(0)]
            for l in geoms:
                if not pc.Orientation(l):
                    tmp.append(l)
                else:
                    g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True)
                    #if len(tmp) > 1:
                    #    plot_polygons([g], color='green')
                    merged.append(g)
                    tmp = [l]
            if tmp:
                g = Geom({'points': tmp, 'polarity': 'dark', 'closed': True}, complex=True)
                merged.append(g)
    return merged


def merge_polygons(mp):
    others = []

    to_merge = []
    merged = []

    pre_pol = 'clear'
    poly_set = []

    for p in mp:
        if p.geom:
            if p.closed:
                # appendo nella lista tutti i poligoni chiusi fino a quando non ne incontro uno
                # clear, a quel punto faccio l'or dei poligoni dark e sottraggo quello clear
                # metto il risultato nella lista di poligoni trattati
                if p.polarity == 'dark':
                    if pre_pol == 'clear':
                        # generare i poligoni qui
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

    layer = merged
    # if layer:
    #     plot_polygons(layer, color='green')
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

