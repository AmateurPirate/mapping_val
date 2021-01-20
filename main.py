import pandas as pd
import math
from random import randint
import warnings
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import networkx as nx


class helpers:
    def __init__(self):
        pass

    # euclidian distance between two point in 3d space
    def euc_dist(self, p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        euclidian_distance = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        return euclidian_distance

    def return_euc_dists(self, points):
        N = len(points)

        if N != 6:
            msg = f'you have {N} points'
            warnings.warn(msg)

        dists = []

        for i in range(1, N):
            dists.append(self.euc_dist(points[i-1], points[i]))
    
        # dists.append(self.euc_dist(points[-1], points[0]))

        # dists = self.min_max_scaler(dists)

        return dists

    def min_max_scaler(self, dists):
        dists = np.array(dists)
        scaler = MinMaxScaler(tuple([5, 6]))
        dists = scaler.fit_transform(dists.reshape(-1, 1))

        return dists



class parse_csv:
    def __init__(self, csv_path):
        # someone tried to multiindex the input csv, but somewhere along the line the formatting got broken
        self.df = pd.read_csv(csv_path, header=2, index_col=0)
        self.points = []
        self.add_vol()
        self.get_six_points()

    # adds cols to df with rolling std so we can detect when the tracked object is stationary
    def add_vol(self):
        for ch in 'xyz':
            self.df[ch + 'vol'] = self.df[ch].rolling(45).std()

    # gets the 6 points used in each calibration video
    def get_six_points(self):
        vol_thresh = 7.5*10e-4
        tmp = self.df[(self.df.xvol < vol_thresh) & (self.df.yvol < vol_thresh) & (self.df.zvol < vol_thresh)]

        x, y, z = tmp.iloc[0][0], tmp.iloc[0][1], tmp.iloc[0][2]
        self.points.append([x, y, z])

        for _, row in tmp.iterrows():
            x, y, z = row.iat[0], row.iat[1], row.iat[2]
            if self.is_different_enough(x, y, z):
                self.points.append([x, y, z])

    # checks to see if this point is different enough from the other points in seen
    # this prevents getting a bunch of consecutive points
    def is_different_enough(self, cx, cy, cz):
        INF = float('inf')
        zscore_thresh = 1

        xstd = self.df['x'].std()
        ystd = self.df['y'].std()
        zstd = self.df['z'].std()

        min_cum_zscore = INF

        for x, y, z in self.points:
            min_cum_zscore = min(min_cum_zscore, abs(cx - x)/xstd + abs(cy - y)/ystd + abs(cz - z)/zstd)

        return min_cum_zscore > zscore_thresh

class visualize_graph(helpers):
    def __init__(self, point_cloud):
        self.point_cloud = point_cloud
        self.adj_list = []
        self.get_adj_list()
        print(self.adj_list)

    def get_adj_list(self):
        node_names = 'abcdef'
        for i in range(N):
            for j in range(i):
                self.adj_list.append([node_names[i], node_names[j], self.euc_dist(self.point_cloud[i], self.point_cloud[j])])

    
        



# validate accuracy with points taken out of video...
# did this and it works perfectly...

# manually selected points from calib_ring_5_DLC_3D.csv
points = [[-43.53, 5.35, 38.22], [-45.45, 5.37, 39.46], [-45.44, 2.56, 39.53], [-45.44, -0.4, 39.6], [-43.53, -0.57, 38.37], [-43.58, 2.38, 38.26]]
# calib_ring_6_DLC_3D.csv
# points = [[-44.4, 5.09, 36.93], [-46.21, 5.05, 38.12], [-46.25, 2.56, 38.11], [-46.21, -0.3, 38.22], [-44.45, -0.5, 37.02], [-44.5, 2.5, 36.94]]

# calib_ring_7_DLC_3D.csv
# points = [[-45.51, 4.66, 35.1], [-47, 4.62, 36.1], [-47.11, 2.43, 36.11], [-47.14, -0.52, 36.22]]
def main():
    DEBUG = False

    if not DEBUG:
        vg = visualize_graph(points)

    else:
        csv_path = './calib_ring_6_DLC_3D.csv' 
        pc = parse_csv(csv_path)
        h = helpers()
        ans = h.return_euc_dists(points)
        print(ans)

if __name__ == '__main__':
    main()
