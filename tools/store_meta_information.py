import argparse

from datetime import date

from lib import Strava
from lib.data import MetaInformation

parser = argparse.ArgumentParser(
    description='Stores meta information')
parser.add_argument('--input', help='mp4 file')
parser.add_argument('--output', help='csv file with meta information',
                    default='meta_information.csv')

args = parser.parse_args()

mi = MetaInformation(filename=args.output)
strava = Strava()

mi.append_entry(args.input, 'strava_activity',
                strava.retrieve_last_activity_id())
mi.append_entry(args.input, 'date',
                str(date.today()))

mi.save()
