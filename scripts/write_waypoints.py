import csv

import numpy as np


def write_waypoints(x, y):

    filename = 'waypoints.csv'

    for bx in range(0, len(x)):
        x_start = x[bx][0]
        x_end = x[bx][1]
        num_points = abs(int(((x_start - x_end) / 0.1))) + 1
        x_pb = np.linspace(start=x_start, stop=x_end, num=num_points)

        for by in y[bx]:
            y_pb = np.repeat([by], num_points, axis=0)
            coordinates = [list(x_pb), list(y_pb)]

            with open(filename, 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)

                # writing the data rows
                csvwriter.writerows(coordinates)
