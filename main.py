import pandas as pd
import math

class helpers:
    def __init__(self):
        pass

    def euc_dist(self, p1, p2):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        euclidian_distance = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        return euclidian_distance

class parse_csv:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.add_vol()
        self.get_six_points()

    def add_vol(self):
        for ch in 'xyz':
            self.df[ch + 'vol'] = self.df['DLC_3D']['one'][ch].rolling(45).std()

    def get_six_points(self):
        pass

def main():
    csv_path = './calib_ring_5_DLC_3D.csv' 
    pc = parse_csv(csv_path)
    print(pc.df.head())
    pass

if __name__ == '__main__':
    main()
