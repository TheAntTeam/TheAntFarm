#
import time
from shapely.geometry import Polygon, LinearRing, LineString, MultiLineString, Point
from collections import OrderedDict
from .geometry_manager import merge_polygons_path, offset_polygon, offset_polygon_holes, get_bbox_area_sh, fill_holes_sh, get_poly_diameter
from .plot_stuff import plot_paths, plot_shapely
from .path_optimizer import Optimizer
from .plot_stuff import plot_lines


class Gapper:

    def __init__(self, path, cfg):
        self.cfg = cfg
        self.in_path = path
        self.gap_dim = self.cfg['taps_length'] + self.cfg['tool_diameter']

    @staticmethod
    def rotate(l, n):
        return l[n:] + l[:n]

    def add_taps_on_external_path(self, strategy='4p'):
        ex_path = self.in_path
        b = ex_path.bounds
        # print("Bounds")
        # print(b)

        xm = (b[2] + b[0]) / 2.0
        ym = (b[3] + b[1]) / 2.0

        # croce dritta
        vl = LineString(((xm, b[1]), (xm, b[3])))
        hl = LineString(((b[0], ym), (b[2], ym)))

        # croce rotata di 45
        # vl = LineString(((b[0], b[1]), (b[2], b[3])))
        # hl = LineString(((b[2], b[1]), (b[0], b[3])))

        # print(vl)
        # print(hl)

        taps = None

        if strategy == '4p':
            # Trovo i punti di intersezione tra
            # la croce vl hl e il perimetro esterno
            # identifico gli indici dei segmenti
            # attraversati, da li seguendo il linestring
            # e creo il segmento da rimuovere lungo taps_length
            vpts = ex_path.intersection(vl)
            points = list(ex_path.coords)
            vtaps = self.get_tap(points, vpts)

            hpts = ex_path.intersection(hl)
            points = list(ex_path.coords)
            htaps = self.get_tap(points, hpts)

            taps = MultiLineString(vtaps + htaps)
            # plot_lines([ex_path], taps)

        if strategy == '2h':
            # Trovo i punti di intersezione tra
            # la croce vl hl e il perimetro esterno
            # identifico gli indici dei segmenti
            # attraversati, da li seguendo il linestring
            # e creo il segmento da rimuovere lungo taps_length

            hpts = ex_path.intersection(hl)
            points = list(ex_path.coords)
            htaps = self.get_tap(points, hpts)

            taps = MultiLineString(htaps)
            # plot_lines([ex_path], taps)

        if strategy == '2v':
            # Trovo i punti di intersezione tra
            # la croce vl hl e il perimetro esterno
            # identifico gli indici dei segmenti
            # attraversati, da li seguendo il linestring
            # e creo il segmento da rimuovere lungo taps_length
            vpts = ex_path.intersection(vl)
            points = list(ex_path.coords)
            vtaps = self.get_tap(points, vpts)

            taps = MultiLineString(vtaps)
            # plot_lines([ex_path], taps)

        if taps is not None:
            npaths = ex_path.difference(taps)
            plot_lines(npaths)
            print("N tap part: " + str(npaths.type))
            if npaths.type == "MultiLineString":
                return list(npaths.geoms)
            else:
                return [npaths]
        else:
            return [ex_path]

    def get_tap(self, points, vpts):
        taps = []
        for pt in vpts.geoms:
            start_id = 0
            c = 0
            prev_len = [(tuple(pt.coords[0]), 0)]
            post_len = [(tuple(pt.coords[0]), 0)]
            for i, j in zip(points, points[1:]):
                if LineString((i, j)).distance(pt) < 1e-8:
                    start_id = c
                    prev_len.append((i, Point(i).distance(pt)))
                    post_len.append((j, Point(j).distance(pt)))
                c += 1
            htl = self.gap_dim / 2.0

            # segmento destro
            # la dimensione del segmento non è
            # sufficiente quindi scorro i segmenti precedenti
            pts = self.rotate(points, start_id)
            # ora il punto di partenza sta alla fine
            flag = post_len[1][1] <= htl
            c = 1
            d = post_len[-1][1]
            while flag and c < len(pts):
                di = Point(post_len[-1][0]).distance(Point(pts[c]))
                post_len.append((pts[c], di))
                if d + di > htl:
                    flag = False
                else:
                    d += di
                c += 1
            if not flag:
                # ho trovato il numero di segmenti
                # necessari a ricostruire metà
                if post_len[-1][1] != htl:
                    # la lunghezza e' superiore
                    p1 = post_len[-2][0]
                    p2 = post_len[-1][0]
                    l = LineString((p1, p2))
                    r = htl - post_len[-2][1]
                    ps = l.intersection(Point(p1).buffer(r))
                    post_len.pop()
                    post_len.append((ps.coords[1], htl))

            # segmento sinistro
            # la dimensione del segmento non è
            # sufficiente quindi scorro i segmenti precedenti
            pts = self.rotate(points, start_id)
            # ora il punto di partenza sta alla fine
            flag = prev_len[1][1] <= htl
            c = -1
            d = prev_len[-1][1]
            while flag and c > - (len(pts)-1):
                di = Point(prev_len[-1][0]).distance(Point(pts[c]))
                prev_len.append((pts[c], di))
                if d + di > htl:
                    flag = False
                else:
                    d += di
                c -= 1
            if not flag:
                # ho trovato il numero di segmenti
                # necessari a ricostruire metà
                if prev_len[-1][1] != htl:
                    # la lunghezza e' superiore
                    p1 = prev_len[-2][0]
                    p2 = prev_len[-1][0]
                    l = LineString((p1, p2))
                    r = htl - prev_len[-2][1]
                    ps = l.intersection(Point(p1).buffer(r))
                    prev_len.pop()
                    prev_len.append((ps.coords[1], htl))

            pre_pts = [p[0] for p in prev_len]
            pre_pts.reverse()
            pre_pts.pop()
            post_pts = [p[0] for p in post_len]
            tap_pts = pre_pts + post_pts
            # print("Tap")
            # print(tap_pts)
            taps.append(LineString(tap_pts))
        return taps


class MachinePath:

    MIN_AREA = 0.1e-1
    TD_COEFF = 0.999

    def __init__(self, tag, machining_type='gerber'):
        # machining type
        # gerber, profile

        self.tag = tag

        self.geom_list = []
        if machining_type == 'gerber':
            self.cfg = {'tool_diameter': 0.2, 'passages': 3, 'overlap': 0.3}
            if self.cfg['passages'] < 1:
                print("[WARNING] At Least One Pass")
                self.cfg['passages'] = 1
        elif machining_type == 'profile':
            self.cfg = {'tool_diameter': 1.0, 'margin': 0.1, 'taps_type': '2h', 'taps_length': 1.0}
        elif machining_type == 'pocketing':
            self.cfg = {'tool_diameter': 1.0}
        elif machining_type == 'drill':
            # self.cfg = {'tool_diameter': 1.0, 'bits_diameter': [1.0, 0.8, 0.6, 0.4]}
            self.cfg = {'tool_diameter': None, 'bits_diameter': [0.8], 'optimize': False}
        else:
            self.cfg = {}
        self.type = machining_type
        self.path = None

    def load_cfg(self, cfg):
        self.cfg = cfg

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
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, td/2.0)
            if og is not None:
                og_list.append(og)

        #print(og_list)

        og_list = merge_polygons_path(og_list, as_list=True)

        #print(og_list)

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

        # plot_paths(prev_poly, [og_list], grb_color='green', path_color='black')

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
        t_d = self.cfg['tool_diameter']
        self.path = [(t_d, path)]

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
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        for g in self.geom_list:
            prev_poly.append(g.geom)
            og = offset_polygon(g, - td / 2.0)
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
        # plot_paths(prev_poly, [og_list], grb_color='grey', path_color='black')
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
        t_d = self.cfg['tool_diameter']
        self.path = [(t_d, path)]

        return milled_list

    def execute_drill(self, not_to_drill=None):
        print("Drilling")
        bd = self.cfg['bits_diameter'][:]
        bd.sort(reverse=True)
        # print(bd)

        # print(not_to_drill)
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

        # print("drill list per bit")
        # print(drill_per_bit)

        for bit_k in drill_per_bit.keys():
            bit_points = drill_per_bit[bit_k]
            if self.cfg['optimize']:
                opt = Optimizer(bit_points)
                optimized_bit_points = opt.get_optimized_path()
                drill_per_bit[bit_k] = optimized_bit_points
                print("Bit " + str(bit_k) + " " + str(optimized_bit_points))
            else:
                print("Bit " + str(bit_k) + " " + str(bit_points))

        paths = []
        for k in drill_per_bit:
            paths.append((k, LineString(drill_per_bit[k])))
        self.path = paths

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
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        # check di singolarità del profilo
        if len(self.geom_list) == 1:
            # profilo mono polygono con eventuali fori
            ext_path = offset_polygon(fill_holes_sh(self.geom_list[0].geom),
                                      td / 2.0 + self.cfg['margin'], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)
            og = offset_polygon_holes(self.geom_list[0], - td / 2.0 + self.cfg['margin'])
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
                                      td / 2.0 + self.cfg['margin'], shapely_poly=True)
            if ext_path is not None:
                og_list.append(ext_path)

            for i, g in enumerate(self.geom_list):
                if i != id:
                    og = offset_polygon_holes(g, - td / 2.0 + self.cfg['margin'])
                    if og is not None:
                        og_list.append(og)

        # plot_shapely(og_list + prev_poly)
        t1 = time.time()
        print("Path Generation Done in " + str(t1-t0) + " sec")
        # plot_paths(prev_poly, [og_list], grb_color='green', path_color='black')
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

        # inserrisco i taps
        # in base alla strategia scelta
        t = Gapper(path[0], self.cfg)
        new_ext = t.add_taps_on_external_path()
        # path[0] = new_ext
        path.pop(0)
        path = new_ext + path

        # todo: aggiungere l'opzione per i gap dei fori
        # pensavo a qualcosa che mettesse almeno 2 gap
        # nel caso in cui il foro avesse un perimetro
        # maggiore di un parametro fissato tipo 20mm
        # il parametro potrebbe essere fissato da GUI

        t_d = self.cfg['tool_diameter']
        self.path = [(t_d, path)]

    def _subpath_execute(self, ppg_list):

        #
        ov = self.cfg['overlap']

        # ppg_list pre path list
        td = self.cfg['tool_diameter'] * self.TD_COEFF
        pre_offset = td/2.0 * (1 + 0.5 - ov)
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
            ng = offset_polygon(g, td / 2.0 * (1 + 0.5 - ov), shapely_poly=True)
            if ng is not None:
                # ng_list.append(ng)
                if ng.geom_type == 'MultiPolygon':
                    for sng in ng:
                        ng_list.append(sng)
                else:
                    ng_list.append(ng)

        fmg_list = merge_polygons_path(ng_list)

        return fmg_list
