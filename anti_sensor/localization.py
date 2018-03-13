# localization scripts


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.optimize as scopt


def localization(coords, c, g, x0, y0):
	'''
	ldpl function
	'''
	x1, y1 = coords
	return c + g * np.log10(((x1-x0)**2 + (y1-y0)**2)**0.5)


def c_fit(tx, room_len, room_wid):
	popt, pcov = scopt.curve_fit(localization,
	                             (tx.loc_x,tx.loc_y),
	                             tx.RSSI,
	                             maxfev=250000,
	                             bounds=((-100,-5,0,0),(30,5,room_wid,room_len)))
	return popt


def fit(df, mac_addr, room_len, room_wid):
    '''
    checks for mac addr in df and returns estimated coords
    '''
    tx = df[df['Source'].str.contains(mac_addr)]
    time = tx['Time']
    t = max(time)

    tx['side'] = pd.cut(tx['Time'], [-1,10,20,30,40], labels=['side1','side2','side3', 'side4'])

    tx1 = tx[tx['side'] == 'side1']
    tx2 = tx[tx['side'] == 'side2']
    tx3 = tx[tx['side'] == 'side3']
    tx4 = tx[tx['side'] == 'side4']

    xy1 = [(0, room_len*(t/10)) for t in tx1['Time']]
    xy2 = [((t-10)*room_wid/10, room_len) for t in tx2['Time']]
    xy3 = [(room_wid, (room_len - (t-20)*room_len/10)) for t in tx3['Time']]
    xy4 = [((room_wid - (t-30)*room_wid/10), 0) for t in tx4['Time']]

    coords = xy1+xy2+xy3+xy4
    loc_x, loc_y = zip(*coords)

    loc_dict = {'loc_x':loc_x,
    			'loc_y':loc_y,
                'Time':time}
    loc_df = pd.DataFrame(loc_dict)
    tx = tx.merge(loc_df, on='Time', how='left')
    # return tx
    popts = c_fit(tx, room_len, room_wid)
    return popts
