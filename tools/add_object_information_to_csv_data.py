from lib.data import VideoFileSegments
from lib.object_data import ObjectData
import argparse
import os

import logging

# get TF logger
log = logging.getLogger('tensorflow')
log.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
fh = logging.FileHandler('tensorflow.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)


parser = argparse.ArgumentParser(
    description='Adds to csv file with information about interesting parts in video')
parser.add_argument('--input', help='json file with object information')
parser.add_argument('--output', help='csv file with interesting segments',
                    default='interesting_video_parts.csv')

args = parser.parse_args()

to_merge = ['Car', 'Wheel', 'Van', 'Land vehicle', 'Person', 'Motorcycle', 'Tire', 'Train', 'Bicycle',
            'Vehicle registration plate', 'Man', 'Bicycle wheel', 'Footwear', 'Truck', 'Woman', 'Bicycle helmet', 'Clothing']

object_data = ObjectData()
object_data.load(args.input)

filename = os.path.split(args.input)[1]

segments = VideoFileSegments(filename=args.output)

for interval in object_data.intervals_not_containing(to_merge):
    segments.append_entry(filename, interval)

segments.save()
