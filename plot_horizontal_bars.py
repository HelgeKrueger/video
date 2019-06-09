import argparse
import json
from tqdm import tqdm

import pandas as pd
import numpy as np

from bokeh.plotting import figure, output_file, show

from lib.colorpicker import Colorpicker

output_file('output/hbar.html')

parser = argparse.ArgumentParser(description='Creates a horizontal plot')
parser.add_argument('--input', help='json file')

args = parser.parse_args()

data = json.load(open(args.input))

df = pd.DataFrame()
df['s'] = range(int(len(data) / 30))
# df['s'] = df['s'] / 30

df.head()

def safe_entities(d):
    if d is None:
        return []
    else: 
        return d['entities']

entities = [safe_entities(d) for d in data]
for idx, ent in tqdm(enumerate(entities)):
    names, counts = np.unique(ent, return_counts=True)
    for name, count in zip(names, counts):
        if name not in df:
            df[name] = 0
        df.at[int(idx / 30), name] += count

def compute_intervals(df, key):
    last_seen = None
    intervals = []

    for idx, count in  df[key].items():
        if count > 0 and last_seen is None:
            last_seen = idx

        if count == 0 and last_seen is not None:
            intervals.append([last_seen, idx])
            last_seen = None
            
    if last_seen is not None:
        intervals.append([last_seen, len(df)])
            
    return intervals

plot_data = pd.DataFrame(columns=['key', 'start', 'end'])

labels = [k for k in df.keys() if k != 's']

for k in labels:
    intervals = compute_intervals(df, k)
    
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
