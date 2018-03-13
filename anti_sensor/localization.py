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


def c_fit(tx):
	popt, pcov = scopt.curve_fit(localization,
	                             (tx.loc_x,tx.loc_y),
	                             tx.RSSI,
	                             maxfev=250000,
	                             bounds=((-100,-5,0,0),(30,5,40,40)))
	return popt


def fit(df, mac_addr, room_len, room_wid):
    '''
    checks for mac addr in df and returns estimated coords
    '''

    time = list(df['Time'])
    t = max(time)
    tx = df[df['Source'].str.contains(mac_addr)]

    y_loc1 = [(0, y*room_len/t) for y in df['Time']]
    x_loc1 = [(x*room_wid/(t+10), room_len) for x in df['Time']]

    y_loc2 = y_loc1[::-1]
    x_loc2 = x_loc1[::-1]

    x1 = [x for x,y in x_loc1]
    x2 = [x for x,y in x_loc2]
    y1 = [y for x,y in y_loc1]
    y2 = [y for x,y in y_loc2]
    
    x_coords = x1+x2
    y_coords = y1+y2

    loc_dict = {'loc_x':x_coords,
    			'loc_y':y_coords,
    			'Time':time}

    loc_df = pd.DataFrame(loc_dict, columns=['loc_x','loc_y','Time'])
    tx = tx.merge(loc_df, on='Time', how='left')
    popts = c_fit(tx)
    return popts
