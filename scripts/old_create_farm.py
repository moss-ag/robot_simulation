import argparse

from get_tree_model import get_tree_model

import numpy as np

FT_TO_M = 0.3048
row_width_spacing = 5 * FT_TO_M
row_length_spacing = 5 * FT_TO_M
block_to_block_spacing = 15 * FT_TO_M

tree_strings = []
# Gazebo coordinates are offset; everything needs to be shifted left
gazebo_left_offset = 1

# Gather user inputs
parser = argparse.ArgumentParser(description='Gazebo Farm World Creator')
parser.add_argument(
    '--num_blocks',
    '-nb',
    type=int,
    default=1,
)
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


def make_row(y_ind, y_pos, num_trees_row):
    """
    Generate the string sections for all of the trees in a row.

    Args:
    ----
        y_ind (int): the index of the row
        y_pos (float): the y position of the row
        num_trees_row (int): the num of trees in the row

    """
    row_length = (num_trees_row - 1) * row_length_spacing
    for index, x_pos in enumerate(
        np.linspace(-row_length / 2, row_length / 2, num_trees_row)
    ):
        name = 'tree_{}_{}'.format(y_ind, index)
        tree_str = get_tree_model(name=name, x=x_pos, y=y_pos - gazebo_left_offset, z=0)
        tree_strings.append(tree_str)


# create list of y positions from widths
y_positions = []
y_pos = 0
while y_pos <= np.sum(args.num_rows):
    for rows in args.num_rows:
        for max_row in range(rows):
            y_positions.append(y_pos)
            if rows - 1 == max_row:
                diff = block_to_block_spacing
            else:
                diff = row_width_spacing
            y_pos += diff

shift = (y_positions[-1] + y_positions[0]) / 2
shifted_y_positions = [round(y_pos - shift, 2) for y_pos in y_positions]

# generate tree strings
ind = 0
for i, y_pos in enumerate(shifted_y_positions):
    if i == args.num_rows[ind]:
        ind += 1
    make_row(y_ind=i, y_pos=y_pos, num_trees_row=args.num_trees_row[ind])


# Open the text files needed for the output file
pre_gen_info = open('../data/pre_gen_info.txt', 'r')
post_gen_info = open('../data/post_gen_info.txt', 'r')

output_file = open(args.filename, 'w')

# Write the text needed before the tree strings
output_file.write(pre_gen_info.read())
pre_gen_info.close()

# Write the tree strings
for tree in tree_strings:
    output_file.write(tree)

# Write the text needed at the end
output_file.write(post_gen_info.read())
post_gen_info.close()
output_file.close()
