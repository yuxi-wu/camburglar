import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
import os
import math

'''
Yuxi router: Netgear_7a:52:d
Jess router: 9c:34:26:da:a3:c6, 9d:34:26:da:a3:ca

Ratul phone: cc:08:8d:52:ab:cc
May phone: 40:98:ad:96:74:96
Yuxi phone: 40:4e:36:8b:b0:b3
Jess phone: ec:9b:f3:cc:32:35

Jess computer: a4:5e:60:eb:ec:bf
Ratul computer: e4:ce:8f:42:64:32
May computer: f4:0f:24:10:14:73
Yuxi computer: c4:b3:01:8a:a0:2c

Chromecast: Google_64:38:38
Home?: Google_16:e8:55
Apple_10:14:73

Camera SSID: CH170C5-59842CF8953C-707143
'''

'''
baseline = pd.read_csv('baseline.csv', encoding='ISO-8859-1')
camera = pd.read_csv('camera.csv', encoding='ISO-8859-1')

intersection = {'Apple_52:ab:cc',
                'Apple_52:ab:cc (cc:08:8d:52:ab:cc) (TA)',
                'Apple_eb:ec:3f (a4:5e:60:eb:ec:3f) (TA)',
                'Apple_eb:ec:bf',
                'Apple_eb:ec:bf (a4:5e:60:eb:ec:bf) (BSSID)',
                'Apple_eb:ec:bf (a4:5e:60:eb:ec:bf) (TA)',
                'Apple_eb:ec:bf (a5:5e:60:eb:ec:bf) (TA)',
                'Apple_eb:ec:df (a4:5e:60:eb:ec:df) (TA)',
                'Htc_8b:b0:b3',
                'Htc_8b:b0:b3 (40:4e:36:8b:b0:b3) (TA)',
                'Htc_8b:b0:b3 (41:4e:36:8b:b0:b3) (TA)',
                'SamsungE_cc:32:35',
                'Shenzhen_ca:20:ad'}
'''

devices = {'yuxirouter':'Netgear_7a:52:d',
            'jessrouter':'ArrisGro_da:a3:ca',
            'chromecast':'Google_64:38:38',
            'ratulphone':'Apple_52:ab:cc',
            'mayphone':'Apple_96:74:96',
            'yuxiphone':'Htc_8b:b0:b3',
            'jessmac':'Apple_eb:ec:bf',
            'maymac':'Apple_10:14:73',
            'ratulmac':'Apple_42:64:32',
            'camera':'Shenzhen_ca:20:ad'
            }

def get_packets(outfile, default='en0', duration=10):
    '''
    uses wireshark to capture traffic data and returns df
    '''
    pcap = outfile + '.pcap > '
    csv = outfile + '.csv'
    command = 'tshark -I -i ' + default + ' -a duration:' + str(duration) +' -T fields -E header=y -E separator=, -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Length -e _ws.col.RSSI -w ' + pcap + csv
    os.system(command)
    return pd.read_csv(csv)


def plot_rss(file):
    data = pd.read_csv(file)
    preprocess(data)

    chromecast = data[data['Source'].str.contains('Google_64:38:38')]
    router = data[data['Source'].str.contains('Netgear_7a:52:db')]
    phone = data[data['Source'].str.contains('Htc_8b:b0:b3')]

    plt.plot(phone.RSSI.rolling(window=20, win_type='triang').mean().dropna(), color = 'green')
    plt.plot(router.RSSI.rolling(window=20, win_type='triang').mean().dropna(), color = 'blue')
    plt.plot(chromecast.RSSI.rolling(window=20, win_type='triang').mean().dropna(), color = 'red')

    plt.show()


def preprocess(df):
    '''
    cleans df of packet data and discretises time variable.
    '''
    df.columns = ['Time', 'Source', 'Destination', 'Length', 'RSSI']
    df.dropna(inplace=True)
    df['Second'] = np.ceil(df['Time'])
    df['RSSI'] = df['RSSI'].str.strip(' dBm').astype('float64')


def find_device(data, mac):
    '''
    finds list of all source devices containing a given name in a processed df.
    '''
    return list(set(data[data['Source'].str.contains(mac)]['Source']))


def device_packet_stats(data, device_label, known=False):
    '''
    returns a few summary stats on a given device in a processed df.
    includes packets sent and received per second, average size of packets sent and received, and average RSS (received signal strength) values.
    '''
    device = device_label
    if known:
        device = devices[device_label]

    source, dest = get_device_traffic_counts(data, device)
    s, d = get_device_traffic_counts(data, device, grouped=False)

    num_s, num_d = source.mean(), dest.mean()
    size_s, size_d = s['Length'].mean(), d['Length'].mean()
    rss_s, rss_d = s['RSSI'].mean(), d['RSSI'].mean()

    return {'device':device_label,
            'packets_received':num_d,
            'size_received':size_d,
            'rss_received':rss_d,
            'packets_sent':num_s,
            'size_sent': size_s,
            'rss_sent':rss_s}

def all_device_stats(data, spy_or_facetime=0):
    stats = pd.DataFrame([device_packet_stats(data, device) for device in set(data['Source'])])

    if spy_or_facetime == 0:
        return stats[(stats['packets_received'].isna()) \
            & (stats['size_received'].isna())\
            & (stats['rss_received'].isna())\
            & (stats['packets_sent'] == 2) \
            & (stats['size_sent'].between(150, 200))]['device']
    elif spy_or_facetime == 1:
        return stats[(stats['packets_received']).between(75, 95)) \
            & (stats['size_received'] > 100)\
            & (stats['packets_sent'].between(60, 80)) \
            & (stats['size_sent'] < 200)\
            & (stats['size_sent'] > 150)]['device']



def get_device_traffic_counts(data, device, rolling=False, grouped=True):
    '''
    returns all packets sent and received from a given device in a tup.
    can specify whether the data is aggregated per second and whether the values are rolling means (useful for more interpretable plots).
    '''
    traffic = []

    for call in ['Source', 'Destination']:
        packets = data[data[call].str.contains(device)]

        if grouped:
            packets = packets.groupby('Second').count()['Length']

            if rolling:
                packets = packets.rolling(window=60, win_type='triang').mean().dropna()

        traffic += [packets]

    return tuple(traffic)


def plot_device_traffic(data, device):
    '''
    plots rolling means of sent and received packet counts for a given device in a processed df.
    '''
    source, destination = get_device_traffic_counts(data, device, rolling=True)
    plt.plot(source, color='#2ab74f')
    plt.plot(destination, color='#e05077')
    plt.savefig('actvity-plots/' + device + '.png')
    plt.close('all')


def get_top_devices(data, head):
    '''
    returns a list of top n devices in a processed df by total packet count.
    '''
    return list(data\
            .groupby(['Source'])['Time']\
            .agg({"count": len})\
            .sort_values("count", ascending=False)\
            .head(head)\
            .reset_index()['Source'])
