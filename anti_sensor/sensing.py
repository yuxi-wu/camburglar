import pandas as pd
from anti_sensor.traffic import get_packets, preprocess, all_device_stats
from anti_sensor.localization import fit

def sense(x, y):
    sides = [get_packets('side'+str(s)) for s in range(4)]

    counter = 0
    for s in sides:
        preprocess(s)
        s['Time'] = s['Time'] + counter
        s['Second'] = s['Second'] + counter
        counter += 10

    df = pd.concat(sides)
    devices = all_device_stats(df, spy_or_facetime=1)

    locs = pd.DataFrame([(d, fit(df, d, x, y)) for d in devices])

    with open('locs.html', 'w') as html:
        html.write(locs.to_html())

    return len(devices)
