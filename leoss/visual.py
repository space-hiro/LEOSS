from .main import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.transforms import offset_copy

import pandas as pd
import numpy as np

import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade

def visual_check():
    s = LEOSS()
    return s

def groundTrack(recorder: Recorder, dateTime = 0):

    df = pd.DataFrame.from_dict(recorder.dataDict)

    spacecraft = recorder.attachedTo
    system = spacecraft.system

    Latitudes  = [ item[0] for item in df['Location'].values.tolist()[1:] ]
    Longitudes = [ item[1] for item in df['Location'].values.tolist()[1:] ]
    Altitudes  = [ item[2] for item in df['Location'].values.tolist()[1:] ]
    Datetimes  = [ item for item in df['Datetime'] ][1:]
    Times      = [ (item - system.datetime0).total_seconds() for item in df['Datetime'][1:] ]

    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.stock_img()
    ax.coastlines(resolution='110m')
    
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    plot = plt.scatter(Longitudes, Latitudes,
        color='red', s=0.2, zorder=2.5,
        transform=ccrs.PlateCarree(),
        )
    if dateTime == 0:
        dateTime = system.datenow()
    currentTime = 0
    if isinstance(dateTime, datetime.datetime):
        currentTime = (dateTime - system.datetime0).total_seconds()
    elif isinstance(dateTime, int) or isinstance(dateTime, float):
        if dateTime > Times[0] and dateTime < Times[-1]:
            currentTime = dateTime
            dateTime = (system.datetime0+datetime.timedelta(seconds=currentTime))
        else:
            raise ValueError("Datetime input should valid time")
    else:
        raise TypeError("Datetime input should be int, float or datettime type")

    ax.set_title(f'Datetime: {dateTime}', horizontalalignment='left', loc='Left')
    plt.title(f'{spacecraft.name}', loc='Right')
    plot.set_alpha([ item<=currentTime for item in Times])
    ax.add_feature(Nightshade(dateTime, alpha=0.3))

    index = Times.index(currentTime)
    ax.plot(Longitudes[index], Latitudes[index] , marker='o', color='white', markersize=12,
            alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)
    
    lat = str('%.2F'% Latitudes[index]+"°")
    lon = str('%.2F'% Longitudes[index]+"°")
    alt = str('%.0F'% Altitudes[index]+"km")
    txt = "lat: "+lat+"\nlon: "+lon+"\nalt: "+alt
    geodetic_transform = ccrs.PlateCarree()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=+15, y=+0)

    ax.text(Longitudes[index], Latitudes[index], txt,
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform, fontsize=8,
        bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'))

    plt.show()

class animatedGroundTrack(object):

    def __init__(self, recorder: Recorder):

        df = pd.DataFrame.from_dict(recorder.dataDict)

        spacecraft = recorder.attachedTo
        self.system = spacecraft.system

        self.lat = [ item[0] for item in df['Location'].values.tolist()[1:] ]
        self.lon = [ item[1] for item in df['Location'].values.tolist()[1:] ]
        self.alt = [ item[2] for item in df['Location'].values.tolist()[1:] ]
        self.datetimes = [ item for item in df['Datetime'] ][1:]
        self.time = [ (item - self.system.datetime0).total_seconds() for item in df['Datetime'][1:] ]

        self.fig = plt.figure(figsize=(10, 5))

        self.ax = plt.axes(projection=ccrs.PlateCarree())

        self.ax.stock_img()
        self.ax.coastlines(resolution='110m')
        self.NS = self.ax.add_feature(Nightshade(self.system.datetime0, alpha=0.3))
        
        gl = self.ax.gridlines(draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False

        self.plot = plt.scatter(self.lon, self.lat,
            color='red', s=0.2, zorder=2.5,
            transform=ccrs.PlateCarree(),
            )
        
        length = int(self.time[-1]/10)

        plt.title(f'{spacecraft.name}', loc='Right')

        print("\nRun Animation (from "+str(self.time[0])+" to "+str(self.time[-1])+")")
        anim = FuncAnimation(
            self.fig,
            self.update,
            frames = tqdm(np.linspace(self.time[0], self.time[-1], length), total=length,  position=0, desc='Animating Ground Track', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}'),
            interval = 1
        )

        anim.save("Groundtrack.mp4", fps=30)

    def update(self, t_current):

        dt_current = self.system.datetime0 + datetime.timedelta(seconds=t_current)
        self.NS.set_visible(False)
        self.NS = self.ax.add_feature(Nightshade(dt_current, alpha=0.3))
        self.ax.set_title(f'Datetime: {dt_current}', horizontalalignment='left', loc='Left')
        self.plot.set_alpha(self.time<=t_current)

        # index = len([ item for item in self.time if item <= t_current ]) - 1
        # self.ax.plot(self.lon[index], self.lat[index] , marker='o', color='white', markersize=12,
        #         alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)
        
        # lat = str('%.2F'% self.lat[index]+"°")
        # lon = str('%.2F'% self.lon[index]+"°")
        # txt = "lat: "+lat+"\nlon: "+lon
        # geodetic_transform = ccrs.PlateCarree()._as_mpl_transform(self.ax)
        # text_transform = offset_copy(geodetic_transform, units='dots', x=+80, y=+0)

        # self.ax.text(self.lon[index], self.lat[index], txt,
        #     verticalalignment='center', horizontalalignment='right',
        #     transform=text_transform, fontsize=8,
        #     bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'))

        return self.plot

