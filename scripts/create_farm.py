import argparse

from itertools import zip_longest

import random

from get_plane_model import get_plane_model

from get_tree_model import get_tree_model

import numpy as np

# SET THESE VARIABLES

FT_TO_M = 0.3048
row_width_spacing = 5 * FT_TO_M
row_length_spacing = 5 * FT_TO_M
block_to_block_spacing = 15 * FT_TO_M

mean = 0  # Gaussian noise
sigma = 0.0  # Gaussian noise (ideal = 0.2, 0 to disable noise addition)
slope = 0  # To make rows slant (ideal = 0.2, 0 for straight rows)
block_offset = (
    0
)  # Distance in meters (ideal = 3) to add block offset, by default odd no. of blocks are staggered
staggered = 0  # Make zero to disable staggered rows, 1 to enable
mud = 0

# ----- -------------- -----------

tree_strings = []
plane_strings = []

# Gazebo coordinates are offset; everything needs to be shifted left
gazebo_left_offset = 0

# Gather user inputs
parser = argparse.ArgumentParser(description='Gazebo Farm World Creator')
parser.add_argument('--num_blocks', '-nb', type=int, default=1)

parser.add_argument(
    '--num_rows',
    '-nr',
    nargs='+',
    default=3,
    help='list of number of rows to use, 1 val per block. Default: 3',
)

parser.add_argument(
    '--num_trees_row',
    '-ntr',
    nargs='+',
    default=5,
    help='list of number of trees in each row to use, 1 val per block. Default: 5',
)

parser.add_argument(
    '--filename',
    '-f',
    type=str,
    default='../worlds/spraybot.world',
    help='full path to save the file in',
)

args = parser.parse_args()

args.num_blocks = int(args.num_blocks)

if args.num_rows is not None:
    # Argparse reads strings, so we need to convert to float
    args.num_rows = [int(i) for i in args.num_rows]
    args.num_rows = np.array(args.num_rows)
    if len(args.num_rows) != 1 and len(args.num_rows) != args.num_blocks:
        raise ValueError(
            'Length of number of rows should be 1 or same as number of blocks'
        )
    elif len(args.num_rows) == 1:
        args.num_rows = np.repeat(args.num_rows, args.num_blocks)

if args.num_trees_row is not None:
    # Argparse reads strings, so we need to convert to float
    args.num_trees_row = [int(i) for i in args.num_trees_row]
    if len(args.num_trees_row) != 1 and len(args.num_trees_row) != args.num_blocks:
        raise ValueError(
            'Length of num of trees in a row should be 1 or same as number of blocks'
        )
    elif len(args.num_trees_row) == 1:
        args.num_trees_row = np.repeat(args.num_trees_row, args.num_blocks)


# Finding First co-ordinate


def compute_grid_one(blocks):
    n = 1
    while True:
        sq = n * n
        if blocks <= sq:
            x = n
            break
        else:
            n = n + 1
    return x


# Second co-ordinate
def compute_grid_two(x_max, blocks):
    count = 0
    x = 1
    cord = []
    row_l = []
    while count < blocks:
        cord_m = []
        row_l_i = []
        while x <= x_max and count < blocks:
            cord_m.append(1)
            row_l_i.append(
                ((args.num_trees_row[count]) - 1) * row_width_spacing
            )  # length of row
            count = count + 1
            x = x + 1
        x = 1

        row_l.append(row_l_i)
        cord.append(cord_m)
    return cord, row_l


x_g = compute_grid_one(args.num_blocks)
b_cords, rl = compute_grid_two(x_g, args.num_blocks)

for r in range(1, len(rl)):  # Row lengths
    rl[r] = [
        sum(n) for n in zip_longest(rl[r - 1], rl[r], fillvalue=0)
    ]  # Cummulative row length

# Computing shift in x
shift_x = (max(rl[-1]) + (len(b_cords) - 1) * block_to_block_spacing) / 2

# Finding y co-ordinates of trees
y_a = []
bl = 0
for br in b_cords:
    y_pos = 0
    y_positions = []
    for bc in br:
        for row in range(args.num_rows[bl]):
            y_positions.append(y_pos)
            y_pos += row_width_spacing
        y_pos = y_pos - row_width_spacing + block_to_block_spacing
        bl = bl + 1
    y_a.append(y_positions)

# print(y_a)

# Shifting to keep origin at center of farm
for rows in range(len(y_a)):
    shift = (y_a[rows][-1] + y_a[rows][0]) / 2
    shifted_y_positions = [round(yy - shift, 2) for yy in y_a[rows]]
    y_a[rows] = shifted_y_positions


# Tree Strings
def make_row(rid, cid, tree_r, idx, x_pos, y_pos):
    name = 'tree_{}_{}_{}_{}'.format(rid, cid, tree_r, idx)
    tree_str = get_tree_model(name=name, x=x_pos, y=y_pos - gazebo_left_offset, z=0)
    tree_strings.append(tree_str)


# Plane Strings
def make_plane(rid, cid, xo, yo, xt, yt):
    model_name = 'gp_{}_{}'.format(rid, cid)
    link_name = 'gp_{}_{}'.format(rid, cid)
    visual_name = 'gp_{}_{}'.format(rid, cid)

    exmud = row_width_spacing / 2

    if staggered == 1:
        if xt < 0:
            xo = xo - row_width_spacing / 2
        else:
            xt = xt + row_width_spacing / 2

    plane_str = get_plane_model(
        model_name,
        link_name,
        visual_name,
        (xo + xt) / 2,
        (yo + yt) / 2,
        abs(xo - xt) + exmud / 2,
        abs(yo - yt) + exmud,
    )
    plane_strings.append(plane_str)


# Finding x co-ordinates of trees
for rows in range(len(y_a)):
    ind = 0

    while ind < len(b_cords[rows]):

        for tr in range(0, args.num_trees_row[rows * len(b_cords[rows]) + ind]):

            start = ind * args.num_rows[rows * len(b_cords[rows]) + ind - 1]
            end = start + args.num_rows[rows * len(b_cords[rows]) + ind]

            y_pos = y_a[rows][start:end]
            y_pos_m = [
                (tr * slope) + (rows * block_offset + element) for element in y_pos
            ]

            x_pos = [
                (tr * row_width_spacing) + abs(random.gauss(mean, sigma))
                for y_pos in y_pos_m
            ]

            # Centering around origin
            if rows != 0:
                x_pos_m = [
                    -shift_x
                    + element
                    + (rows * block_to_block_spacing)
                    + rl[rows - 1][ind]
                    for element in x_pos
                ]
            else:
                x_pos_m = [-shift_x + element for element in x_pos]

            # Staggering
            # x_pos_m = [
            #     (x_pos[i] - row_width_spacing / 2 * staggered)
            #     if i % 2 != 0
            #     else x_pos[i]
            #     for i in range(len(x_pos))
            # ]
            for i in range(len(x_pos_m)):
                if i % 2 != 0:
                    if x_pos_m[i] < 0:
                        x_pos_m[i] = x_pos_m[i] - row_width_spacing / 2 * staggered
                    else:
                        x_pos_m[i] = x_pos_m[i] + row_width_spacing / 2 * staggered

            # For Mud Plane Co-ordinates

            if tr == 0:
                x1, y1 = x_pos_m[0], y_pos_m[0]
            elif tr == ((args.num_trees_row[rows * len(b_cords[rows]) + ind]) - 1):
                x2, y2 = x_pos_m[-1], y_pos_m[-1]

            # print(rows,ind,tr)
            # print(x_pos_m)
            # print(y_pos_m)

            for i in range(0, len(x_pos_m)):
                make_row(
                    rid=rows,
                    cid=ind,
                    tree_r=tr,
                    idx=i,
                    x_pos=x_pos_m[i],
                    y_pos=y_pos_m[i],
                )

        if mud == 1:
            make_plane(rows, ind, x1, y1, x2, y2)

        ind = ind + 1


pre_gen_info = open('../data/pre_gen_info.txt', 'r')
post_gen_info = open('../data/post_gen_info.txt', 'r')
output_file = open(args.filename, 'w')

# Write the text needed before the tree strings
output_file.write(pre_gen_info.read())
pre_gen_info.close()

for plane in plane_strings:
    output_file.write(plane)

# Write the tree strings
for tree in tree_strings:
    output_file.write(tree)

# Write the text needed at the end
output_file.write(post_gen_info.read())
post_gen_info.close()
output_file.close()

print('DONE')
