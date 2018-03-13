import pandas as pd
from anti_sensor.traffic import get_packets, preprocess, all_device_stats
from anti_sensor.localization import fit

def sense(x, y, sof=1):
    sides = [get_packets('side'+str(s)) for s in range(4)]

    counter = 0
    for s in sides:
        preprocess(s)
        s['Time'] = s['Time'] + counter
        s['Second'] = s['Second'] + counter
        counter += 10

    df = pd.concat(sides)
    devices = all_device_stats(df, spy_or_facetime=sof)

    locs = pd.DataFrame([{'device':d, 'coords':(fit(df, d, x, y)[2], fit(df, d, x, y)[3])} for d in devices])
    locs = locs.to_html().replace('\n','')

    with open('locs.html', 'w') as html:
        html.write(locs)

    return len(devices)
