import csv

import numpy as np

import matplotlib.pyplot as plt

from icecream import ic

def write_waypoints(x, y, sl, numtrees, nvx,nvy):

    filename = 'waypoints.csv'
    cordsx = []
    cordsy = []

    for bx in range(0, len(x)):
        x_start = x[bx][0]
        x_end = x[bx][1]
        num_points = abs(int(((x_start - x_end) / 0.1))) + 1
        x_pb = np.linspace(start=x_start, stop=x_end, num=num_points)

        for by in y[bx]:
            
            if sl == 0:
                y_pb = np.repeat([by], num_points, axis=0)
                coordinates = [list(x_pb), list(y_pb)]
            else:
                if x_end<0:
                    y_pb = np.linspace(by,by-sl*(numtrees[bx]-1), num_points, axis=0)+2.5
                    coordinates = [list(x_pb), list(y_pb)]
                    ic(y_pb)
                else:
                    y_pb = np.linspace(by,by+sl*(numtrees[bx]-1), num_points, axis=0)
                    coordinates = [list(x_pb), list(y_pb)]
                    ic(y_pb)

            with open(filename, 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)

                # writing the data rows
                csvwriter.writerows(coordinates)

            cordsx.append(list(x_pb))
            cordsy.append(list(y_pb))

    plt.scatter(cordsx, cordsy)
    plt.scatter(nvx, nvy)
    plt.show()
