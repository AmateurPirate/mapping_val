import pandas as pd
import math

class helpers:
    def __init__(self):
        pass

    def euc_dist(self, p1: List[int], p2: List[int]) -> int:
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        euclidian_distance = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
        return euclidian_distance

class parse_csv:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.get_six_points()

    def get_six_points(self):
        self.df['vol'] = pd.rolling_std(self.df, 45)

def main():
    pass

if __name__ == '__main__':
    main.py
