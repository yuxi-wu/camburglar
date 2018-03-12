import pandas as pd
from traffic import get_packets, preprocess, all_device_stats
from localization import fit

def sense(x, y):
    sides = [get_packets('side%'+str(s)) for s in range(4)]

    counter = 0
    for s in sides:
        preprocess(s)
        s['Time'] = s['Time'] + counter
        s['Second'] = s['Second'] + counter
        print(s.head(5))
        counter += 10

    df = pd.concat(sides)
    devices = all_device_stats(df)

    return pd.DataFrame([(d, fit(d, x, y)) for d in devices])
