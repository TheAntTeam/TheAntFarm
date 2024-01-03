
import numpy as np
import numpy.linalg as nl
from scipy.spatial.distance import pdist, cdist, squareform


class TpsCoefficients:

    def __init__(self, sampled_points):
        """
        Parameters
        ----------
        sampled_points : list of couples of a pair of coordinates
            The list of sampled points with corresponding control point. i.e.:
            [
              ((control_p0_x, control_p0_y), (sampled_p0_x, sampled_p0_y)),
              ((control_p1_x, control_p1_y), (sampled_p1_x, sampled_p1_y)),
              ((control_p2_x, control_p2_y), (sampled_p2_x, sampled_p2_y)),
              ...
            ]
        """

        self.sampled_points = sampled_points
        self.cx, self.cy = self.compute_tps_coeff()

    def get_control_points_stack(self):
        return self.get_points_stack(0)

    def get_sampled_points_stack(self):
        return self.get_points_stack(1)

    def get_points_stack(self, index):
        xs, ys = zip(*list(zip(*self.sampled_points))[index])  # get the coords of all points (control or sampled [0,1])
        return np.vstack([xs, ys]).T

    def compute_tps_coeff(self):

        cx = cy = None
        if self.sampled_points is not []:
            cps = self.get_control_points_stack()
            sps = self.get_sampled_points_stack()

            # construct T Matrix
            tm = self.compute_t_matrix(cps)

            # solve cx, cy (coefficients for x and y)
            xt_aug = np.concatenate([sps[:, 0], np.zeros(3)])
            yt_aug = np.concatenate([sps[:, 1], np.zeros(3)])
            cx = nl.solve(tm, xt_aug)  # [K+3]
            cy = nl.solve(tm, yt_aug)
        return cx, cy

    @staticmethod
    def compute_t_matrix(cp):
        # cp: [K x 2] control points
        # tm: [(K+3) x (K+3)]
        k = cp.shape[0]
        tm = np.zeros((k + 3, k + 3))
        tm[:k, 0] = 1
        tm[:k, 1:3] = cp
        tm[k, 3:] = 1
        tm[k + 1:, 3:] = cp.T
        r = squareform(pdist(cp, metric='euclidean'))
        r = r * r
        r[r == 0] = 1  # a trick to make R ln(R) 0
        r = r * np.log(r)
        np.fill_diagonal(r, 0)
        tm[:k, 3:] = r
        return tm

    @staticmethod
    def lift_points(p, cp):
        # p: [n x 2], input points
        # cp: [k x 2], control points
        # p_lift: [n x (3+k)], lifted input points
        n, k = p.shape[0], cp.shape[0]
        p_lift = np.zeros((n, k+3))
        p_lift[:, 0] = 1
        p_lift[:, 1:3] = p
        r = cdist(p, cp, 'euclidean')
        r = r * r
        r[r == 0] = 1
        r = r * np.log(r)
        p_lift[:, 3:] = r
        return p_lift

    def compute_points_transform(self, gps):

        cps = self.get_control_points_stack()

        # transform
        pg_lift = self.lift_points(gps, cps)  # [N x (K+3)]
        xgt = np.dot(pg_lift, self.cx.T)
        ygt = np.dot(pg_lift, self.cy.T)
        return xgt, ygt


class AlignManager:

    def __init__(self):
        self.sampled_points = []
        self.tps_coeff = None

    def load_sampled_points(self, sampled_points):
        self.sampled_points = sampled_points
        self.update_tps_coefficients()

    def is_sampled_point_loaded(self):
        return self.sampled_points != []

    def update_tps_coefficients(self):
        self.tps_coeff = TpsCoefficients(self.sampled_points)

    def compute_points_transform(self, points):
        if self.tps_coeff is not None and len(points) > 0:
            zgs = None
            if len(points[0]) == 3:
                xgs, ygs, zgs = list(zip(*points))
            else:
                xgs, ygs = list(zip(*points))

            gps = np.vstack([xgs, ygs]).T
            nxgs, nygs = self.tps_coeff.compute_points_transform(gps)

            if len(points[0]) == 3:
                new_points_coord = list(zip(nxgs, nygs, zgs))
            else:
                new_points_coord = list(zip(nxgs, nygs))
            return new_points_coord
        else:
            return None


