import pandas as pd
import math
from random import randint


class helpers:
    def __init__(self):
        pass

    # euclidian distance between two point in 3d space
    def euc_dist(self, p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        euclidian_distance = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        return euclidian_distance
    

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
            # print(ch+'vol max: ', self.df[ch + 'vol'].max())

    # gets the 6 points used in each calibration video
    def get_six_points(self):
        vol_thresh = 7.5*10e-4
        tmp = self.df[(self.df.xvol < vol_thresh) & (self.df.yvol < vol_thresh) & (self.df.zvol < vol_thresh)]
        for _, row in tmp.head(2).iterrows():
            x, y, z = row.iat[0], row.iat[1], row.iat[2]
            if self.is_different_enough(x, y, z):
                self.points.append([x, y, z])

    # checks to see if this point is different enough from the other points in seen
    # this prevents getting a bunch of consecutive points
    def is_different_enough(self, x, y, z):
        xstd = self.df['x'].std()
        ystd = self.df['y'].std()
        zstd = self.df['z'].std()

        

        


def main():
    csv_path = './calib_ring_5_DLC_3D.csv' 
    pc = parse_csv(csv_path)
    print(pc.points)

if __name__ == '__main__':
    main()
