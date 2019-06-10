import argparse
import os

import pandas as pd

from lib.object_data import ObjectData

parser = argparse.ArgumentParser(description='Adds to csv file with information about interesting parts in video')
parser.add_argument('--input', help='json file with object information')
parser.add_argument('--output', help='csv file with interesting segments', default='interesting_video_parts.csv')

args = parser.parse_args()

to_merge = ['Car', 'Wheel', 'Van', 'Land vehicle', 'Person', 'Motorcycle', 'Tire', 'Train', 'Bicycle', 'Vehicle registration plate', 'Man', 'Bicycle wheel', 'Footwear', 'Truck', 'Woman', 'Bicycle helmet', 'Clothing']

object_data = ObjectData()
object_data.load(args.input)

if os.path.isfile(args.output):
    df = pd.read_csv(args.output)
else:
    df = pd.DataFrame(columns = ['filename', 'start', 'end', 'status'])

filename = os.path.split(args.input)[1]

for interval in object_data.intervals_not_containing(to_merge):
    df = df.append({
        'filename': filename,
        'start': interval[0],
        'end': interval[1],
        'status': 'unseen'
        }, ignore_index=True)

df.to_csv(args.output, index=False)
