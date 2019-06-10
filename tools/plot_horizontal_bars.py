import argparse
import json

import pandas as pd
import numpy as np

from bokeh.plotting import figure, output_file, show

from lib.colorpicker import Colorpicker
from lib.object_data import ObjectData

output_file('output/hbar.html')

parser = argparse.ArgumentParser(description='Creates a horizontal plot')
parser.add_argument('--input', help='json file')

args = parser.parse_args()

object_data = ObjectData()
object_data.load(args.input)

plot_data = pd.DataFrame(columns=['key', 'start', 'end'])

labels = object_data.get_keys()

object_data.data.head()

for k in labels:
    intervals = object_data.compute_intervals(k)
    
    for i in intervals:
        plot_data = plot_data.append({
            'key': k,
            'start': i[0],
            'end': i[1]
        }, ignore_index=True)
        
labels.reverse()

colorpicker = Colorpicker()

fig = figure(y_range=labels, width=1600)
for k in labels:
    color=colorpicker.for_title(k)
    color = (color[0]/2, color[1]/2, color[2]/3)
    fig.hbar(y="key", left='start', right='end', height=0.5,
             source=plot_data[plot_data['key'] == k],
             fill_color=color, line_color=color)
show(fig)
