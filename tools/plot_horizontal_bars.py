import argparse

import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

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

to_merge = ['Car', 'Wheel', 'Van', 'Land vehicle', 'Person', 'Motorcycle', 'Tire', 'Train', 'Bicycle',
            'Vehicle registration plate', 'Man', 'Bicycle wheel', 'Footwear', 'Truck', 'Woman', 'Bicycle helmet', 'Clothing']

for i in object_data.intervals_for_list(to_merge):
    plot_data = plot_data.append({
        'key': 'Merged',
        'start': i[0],
        'end': i[1]
    }, ignore_index=True)

fig_merged = figure(y_range=['Merged'], height=200, width=1600)
fig_merged.hbar(y="key", left='start', right='end', height=0.5,
                source=plot_data)

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
    color = colorpicker.for_title(k)
    color = (color[0]/2, color[1]/2, color[2]/3)
    fig.hbar(y="key", left='start', right='end', height=0.5,
             source=plot_data[plot_data['key'] == k],
             fill_color=color, line_color=color)

show(column(fig_merged, fig))

print("Intervals not containing bad keys",
      object_data.intervals_not_containing(to_merge))
