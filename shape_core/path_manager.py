#
import time
from .geometry_manager import merge_polygons_path, offset_polygon, offset_polygon_holes, get_bbox_area_sh, fill_holes_sh, get_poly_diameter
from .plot_stuff import plot_paths, plot_shapely
from shapely.geometry import Polygon, LinearRing, LineString
from collections import OrderedDict


class MachinePath:

    MIN_AREA = 0.1e-1

    def __init__(self, machining_type='gerber'):
        # machining type
        # gerber, profile

        self.geom_list = []
        if machining_type == 'gerber':
            self.cfg = {'tool_diameter': 0.2, 'passages': 3, 'overlap': 0.5}
            if self.cfg['passages'] < 1:
                print("[WARNING] At Least One Pass")
                self.cfg['passages'] = 1
        elif machining_type == 'profile':
            self.cfg = {'tool_diameter': 1.0, 'margin': 0.1, 'taps_number': 4, 'taps_length': 1.0}
        elif machining_type == 'pocketing':
            self.cfg = {'tool_diameter': 1.0}
        elif machining_type == 'drill':
            self.cfg = {'tool_diameter': 1.0, 'bits_diameter': [1.0, 0.8, 0.6, 0.4]}
        else:
            self.cfg = {}
        self.type = machining_type
        self.path = None

    def get_path(self):
        return self.path

    def load_geom(self, geom_list):
        self.geom_list = geom_list

    def load_cfg(self, cfg):
        self.cfg = cfg

    def execute(self):
        elabs = None
        if self.type == 'gerber':
            self.execute_gerber()
        elif self.type == 'profile':
            self.execute_profile()
        elif self.type == 'pocketing':
            elabs = self.execute_pocketing()
        elif self.type == 'drill':
            # se e' impostato un tool di pocketing
            # eseguo la lavorazione
            # altrimenti risolvo tutto con i fori
            elabs_p = None
            if self.cfg['tool_diameter'] is not None:
                elabs_p = self.execute_pocketing()

            # se è stata effettuata una lavorazione di pocketing
            # elabs conterrà una lista di bool che identifica i fori
            # gia' elaborati e che quindi dovranno essere scartati
            # dalla lavorazione di drilling
            elabs_d = self.execute_drill(not_to_drill=elabs_p)

            # controllando elabs ora si potranno individurare
            # quali sono i fori che non sono stati elaborati
            # ed eventualmente indicarli all'utente
            elabs = []

            if elabs_p is not None:
                for i in range(len(elabs_d)):
                    elabs.append(elabs_p[i] or elabs_d[i])

            if elabs is not None:
                if not all(elabs):
                    print("Not all holes are computed, please add bits with correct diameter")

        return elabs

    def execute_gerber(self):
        # creo il primo passaggio di lavorazione, quello più vicino alle piste.
        t0 = time.time()
        og_list = []
        prev_poly = []
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, self.cfg['tool_diameter']/2.0)
            if og is not None:
                og_list.append(og)

        # per i sucessivi si parte dal path precedente, lo si ingrandisce del raggio del tool
        # se ne fa l'or e poi lo si riduce del raggio del tool
        # a quel punto lo si ingrandisce del diametro del tool*(1-perc_di_overlap) [qui è da rivedere la formula]
        for i in range(self.cfg['passages']-1):
            sub_og_list = self._subpath_execute(og_list)
            og_list += sub_og_list

        # plot_shapely(og_list + prev_poly)
        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")

        og_list = self.check_min_area(og_list)

        plot_paths(prev_poly, [og_list], grb_color='green', path_color='black')

        # plot_shapely(og_list)
        # print(og_list)

        # estraggo le linestring dai poligoni path
        path = []
        for g in og_list:
            ex_path = g.exterior
            print(ex_path.type)
            if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                path.append(ex_path)
            for i in g.interiors:
                if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                    path.append(i)
        self.path = path

    def check_min_area(self, og_list):
        big_poly = []
        old_poly = 0
        new_poly = 0
        for p in og_list:
            old_poly += 1
            new_inners = []
            for inner in p.interiors:
                old_poly += 1
                # need to make a polygon of the linearring to get the _filled_ area of
                # the closed ring.
                if abs(Polygon(inner).area) >= self.MIN_AREA:
                    new_inners.append(inner)
            if abs(Polygon(p.exterior).area) >= self.MIN_AREA:
                p = Polygon(p.exterior, new_inners)
                new_poly += 1 + len(p.interiors)
                big_poly.append(p)

        print("REMOVED: " + str(old_poly - new_poly))

        return big_poly

    def execute_pocketing(self):
        print("Pocketing")
        # creo il primo passaggio di lavorazione, quello più vicino al profilo del foro
        t0 = time.time()
        og_list = []
        prev_poly = []
        milled_list = []
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, -self.cfg['tool_diameter']/2.0)
            if og is not None:
                if not og.is_empty:
                    og_list.append(og)
                    milled_list.append(True)
                else:
                    milled_list.append(False)
            else:
                milled_list.append(False)

        # per i sucessivi si parte dal path precedente, lo si ingrandisce del raggio del tool
        # se ne fa l'or e poi lo si riduce del raggio del tool
        # a quel punto lo si ingrandisce del diametro del tool*(1-perc_di_overlap) [qui è da rivedere la formula]
        # for i in range(self.cfg['passages']-1):
        #     sub_og_list = self._subpath_execute(og_list)
        #     og_list += sub_og_list

        # plot_shapely(og_list + prev_poly)
        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")
        plot_paths(prev_poly, [og_list], grb_color='grey', path_color='black')
        # plot_shapely(og_list)
        # print(og_list)

        # estraggo le linestring dai poligoni path
        path = []
        for g in og_list:
            ex_path = g.exterior
            print(ex_path.type)
            if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                path.append(ex_path)
            for i in g.interiors:
                if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                    path.append(i)
        self.path = path

        return milled_list

    def execute_drill(self, not_to_drill=None):
        print("Drilling")
        bd = self.cfg['bits_diameter'][:]
        bd.sort(reverse=True)
        # print(bd)

        #print(not_to_drill)
        to_drill = [True] * len(self.geom_list)
        if not_to_drill is not None:
            to_drill = [not elem for elem in not_to_drill]
        # creo il primo passaggio di lavorazione, quello più vicino al profilo del foro
        drilled_list = []
        drills = []
        for i, g in enumerate(self.geom_list):
            if to_drill[i]:
                drilled_list.append(True)
                c = g.geom.centroid
                ds = get_poly_diameter(g.geom)
                # ho il diametro del foro
                # ora posso selezionare tra i disponibili
                # la punta corretta per effettuare il foro.
                # tra quelle disponibili selezione quella piu' vicina
                # col diametro inferiore
                # print(ds)
                for j, d in enumerate(ds):
                    drills.append([i, c.coords[j], d])
            else:
                drilled_list.append(False)

        drills.sort(key=lambda x: x[2], reverse=True)
        # print(drills)

        drill_per_bit = OrderedDict()
        b = bd[0]
        c = 1
        for dd in drills:
            d = dd[2]
            while b > d and c < len(bd):
                b = bd[c]
                c += 1
            if b not in drill_per_bit.keys():
                drill_per_bit[b] = []
            drill_per_bit[b].append(dd[1])

        print(drill_per_bit)

        return drilled_list

    def execute_profile(self):
        # per eseguire la lavorazione di profilo, va prima individuata la geometria
        # esterna, ci sarà un check che indicherà se le altre geom saranno interne
        # Se la geometria esterna è l'unica, verranno elaborati anche i suoi fori
        # se invece sono presenti altre geometrie saranno considerate dei contorni
        # a dei fori che andranno lavorati.

        t0 = time.time()
        og_list = []
        prev_poly = [g.geom for g in self.geom_list]

        # check di singolarità del profilo
        if len(self.geom_list) == 1:
            # profilo mono polygono con eventuali fori
            ext_path = offset_polygon(fill_holes_sh(self.geom_list[0].geom),
                                      self.cfg['tool_diameter'] / 2.0 + self.cfg['margin'], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)
            og = offset_polygon_holes(self.geom_list[0], -self.cfg['tool_diameter'] / 2.0 + self.cfg['margin'])
            if og is not None:
                og_list.append(og)
        else:
            # profilo composto da più poligoni
            # per individuare il profilo esterno calcolo le aree delle bbox di ogni poligono
            # il poligono con la bbox più grande sarà quello esterno.
            geoms = [g.geom for g in self.geom_list]
            bba = get_bbox_area_sh(geoms.pop(0))
            id = 0

            for i, p in enumerate(geoms):
                a = get_bbox_area_sh(p)
                # print("Area: " + str(a) + " " + str(i+1))
                if a > bba:
                    bba = a
                    id = i + 1

            # print(id)

            # id contiene ora l'indice della geom con bbox maggiore.
            # todo: fare il check che tutte le altre geom siano contenute in essa

            # print("GEOM POLY")
            # print(self.geom_list)
            # print(len(self.geom_list))

            ext_p = self.geom_list[id]
            ext_path = offset_polygon(fill_holes_sh(ext_p.geom),
                                      self.cfg['tool_diameter'] / 2.0 + self.cfg['margin'], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)

            for i, g in enumerate(self.geom_list):
                if i != id:
                    og = offset_polygon_holes(g, -self.cfg['tool_diameter'] / 2.0 + self.cfg['margin'])
                    if og is not None:
                        og_list.append(og)

        # plot_shapely(og_list + prev_poly)
        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")
        plot_paths(prev_poly, [og_list], grb_color='green', path_color='black')
        # plot_shapely(og_list)
        # print(og_list)

        # estraggo le linestring dai poligoni path
        path = []
        for g in og_list:
            ex_path = g.exterior
            # print(ex_path.type)
            if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                path.append(ex_path)
            for i in g.interiors:
                if ex_path.type == "LinearRing" or ex_path.type == "LineString":
                    path.append(i)
        self.path = path

    def _subpath_execute(self, ppg_list):

        #
        ov = self.cfg['overlap']

        # ppg_list pre path list

        pre_offset = self.cfg['tool_diameter']/2.0 * (1 + 0.5 - ov)
        og_list = []

        # print("ORIG")
        # plot_shapely(ppg_list)

        for g in ppg_list:
            og = offset_polygon(g, pre_offset, shapely_poly=True)
            if og is not None:
                if og.geom_type == 'MultiPolygon':
                    for sog in og:
                        og_list.append(sog)
                else:
                    og_list.append(og)

        # print("OFFSET")
        # plot_shapely(og_list)

        mg_list = merge_polygons_path(og_list)

        # print("MERGED")
        # plot_shapely(mg_list)

        mog_list = []
        for g in mg_list:
            mog = offset_polygon(g, -pre_offset, shapely_poly=True)
            if mog is not None:
                if mog.geom_type == 'MultiPolygon':
                    for smog in mog:
                        mog_list.append(smog)
                else:
                    mog_list.append(mog)

        # definisco l'ultima operzione in base al diametro del tool ed il valore dell'overlap

        ng_list = []
        for g in mog_list:
            ng = offset_polygon(g, self.cfg['tool_diameter'] / 2.0 * (1 + 0.5 - ov), shapely_poly=True)
            if ng is not None:
                # ng_list.append(ng)
                if ng.geom_type == 'MultiPolygon':
                    for sng in ng:
                        ng_list.append(sng)
                else:
                    ng_list.append(ng)

        fmg_list = merge_polygons_path(ng_list)

        return fmg_list
