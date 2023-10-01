from .main import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.transforms import offset_copy

import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import pandas as pd
import numpy as np

import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade

from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def visual_check():
    s = LEOSS()
    return s

def attitudeTrack(recorder: Recorder, sample: int = 0, saveas: str = "mp4", dpi: int = 300):

    df = pd.DataFrame.from_dict(recorder.dataDict)

    spacecraft = recorder.attachedTo
    system = spacecraft.system

    xs =spacecraft.size.x/min(spacecraft.size)
    ys =spacecraft.size.y/min(spacecraft.size)
    zs =spacecraft.size.z/min(spacecraft.size)

    ratio = max(spacecraft.size)/min(spacecraft.size)

    if sample > 0:
        df = df.iloc[::sample,:]   

    States      = [ item for item in df['State'].values.tolist()[1:] ]
    Positions   = [ item.position for item in df['State'].values.tolist()[1:] ]
    Quaternions = [ item.quaternion for item in df['State'].values.tolist()[1:] ]
    Bodyrates   = [ item.bodyrate*R2D for item in df['State'].values.tolist()[1:] ]
    Datetimes   = [ item for item in df['Datetime'] ][1:]
    Times       = [ (item - system.datetime0).total_seconds() for item in df['Datetime'][1:] ]

    fig = plt.figure(figsize=(18,9))
    fig.tight_layout()
    ax1 = fig.add_subplot(3,2,2)
    ax2 = fig.add_subplot(3,2,4)
    ax3 = fig.add_subplot(2,4,1, projection='3d')
    ax4 = fig.add_subplot(3,2,6)
    ax5 = fig.add_subplot(2,4,2, projection='3d')
    ax6 = fig.add_subplot(2,4,5, projection='3d')
    ax7 = fig.add_subplot(2,4,6, projection='3d')

    QuatW = [ q.w for q in Quaternions ]
    QuatX = [ q.x for q in Quaternions ]
    QuatY = [ q.y for q in Quaternions ]
    QuatZ = [ q.z for q in Quaternions ]
    RateX = [ r.x for r in Bodyrates ]
    RateY = [ r.y for r in Bodyrates ]
    RateZ = [ r.z for r in Bodyrates ]

    Eulers = [ q.YPR_toRPY_vector() for q in Quaternions ]
    Roll  = [ item.x*R2D for item in Eulers ]
    Pitch = [ item.y*R2D for item in Eulers ]
    Yaw   = [ item.z*R2D for item in Eulers ]

    Matrices = [ q.toMatrix().transpose() for q in Quaternions ]

    ln1, = ax1.plot([],[], label='q0')
    ln2, = ax1.plot([],[], label='q1')
    ln3, = ax1.plot([],[], label='q2')
    ln4, = ax1.plot([],[], label='q3')
    ln5, = ax2.plot([],[], label='X')
    ln6, = ax2.plot([],[], label='Y')
    ln7, = ax2.plot([],[], label='Z')
    ln8, = ax3.plot([],[],[])
    ln9, = ax3.plot([],[],[])
    ln10, = ax3.plot([],[],[])
    ln11, = ax3.plot([],[],[])
    ln12, = ax4.plot([],[], label='roll')
    ln13, = ax4.plot([],[], label='pitch')
    ln14, = ax4.plot([],[], label='yaw')

    ln15, = ax5.plot([],[],[])
    ln16, = ax5.plot([],[],[])
    ln17, = ax5.plot([],[],[])

    ln18, = ax6.plot([],[],[])
    ln19, = ax6.plot([],[],[])
    ln20, = ax6.plot([],[],[])

    ln21, = ax6.plot([],[],[])
    ln22, = ax6.plot([],[],[])
    ln23, = ax6.plot([],[],[])
    

    ax1.grid()
    ax2.grid()
    ax3.view_init(30,20)
    ax5.view_init(0,0)
    ax6.view_init(0,90)
    ax7.view_init(90,0)
    ax4.grid()

    ax1.title.set_text(f'Quaternion')
    ax2.title.set_text(f'Body Rates (deg/s)')
    ax4.title.set_text(f'Euler Angles (deg)')

    plt.style.use("Solarize_Light2")


    def init():
        ax1.set_ylim(-1.1,1.1)
        ax4.set_ylim(-190,190)

        for axis in ax5.xaxis, ax6.yaxis, ax7.zaxis:
            axis.set_label_position('none')
            axis.set_ticks_position('none')

        ax6.zaxis.set_label_position('upper')
        ax6.zaxis.set_ticks_position('upper')    

        plt.subplots_adjust(wspace=0, hspace=0.3, left=0)   

        return ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9, ln10, ln11, ln12, ln13, ln14, \
                ln15, ln16, ln17, ln18, ln19, ln20, ln21, ln22, ln23,

    def update(frame):
        plt.suptitle(f'{spacecraft.name}\n{Datetimes[frame]}', fontname='monospace')

        ln1.set_data(Times[0: frame], QuatW[0: frame])
        ln2.set_data(Times[0: frame], QuatX[0: frame])
        ln3.set_data(Times[0: frame], QuatY[0: frame])
        ln4.set_data(Times[0: frame], QuatZ[0: frame])
        ln5.set_data(Times[0: frame], RateX[0: frame])
        ln6.set_data(Times[0: frame], RateY[0: frame])
        ln7.set_data(Times[0: frame], RateZ[0: frame])
        ln12.set_data(Times[0: frame], Roll[0: frame])
        ln13.set_data(Times[0: frame], Pitch[0: frame])
        ln14.set_data(Times[0: frame], Yaw[0: frame])        

        xaxis = Vector(1,0,0)
        yaxis = Vector(0,1,0)
        zaxis = Vector(0,0,1)
        maxis = Matrices[frame] * spacecraft.inertia*Bodyrates[frame]

        maxisZ = maxis.normalize()
        maxisX = maxisZ.cross(zaxis).normalize()
        maxisY = maxisZ.cross(maxisX).normalize()
        MomentumRotation = Matrix(maxisX, maxisY,maxisZ)

        Rotation = Matrices[frame]
        Rotation = MomentumRotation.transpose() * Matrices[frame]
        maxisLine = MomentumRotation.transpose() * maxis * ratio * 2

        xaxis = Rotation * xaxis * xs * 2
        yaxis = Rotation * yaxis * ys * 2
        zaxis = Rotation * zaxis * zs * 2

        xFaceP1 = Rotation * Vector( xs,-ys, zs)
        xFaceP2 = Rotation * Vector( xs, ys, zs)
        xFaceP3 = Rotation * Vector( xs, ys,-zs)
        xFaceP4 = Rotation * Vector( xs,-ys,-zs)

        nxFaceP1 = Rotation * Vector(-xs, ys, zs)
        nxFaceP2 = Rotation * Vector(-xs,-ys, zs)
        nxFaceP3 = Rotation * Vector(-xs,-ys,-zs)
        nxFaceP4 = Rotation * Vector(-xs, ys,-zs)

        yFaceP1 = Rotation * Vector( xs, ys, zs)
        yFaceP2 = Rotation * Vector(-xs, ys, zs)
        yFaceP3 = Rotation * Vector(-xs, ys,-zs)
        yFaceP4 = Rotation * Vector( xs, ys,-zs)

        nyFaceP1 = Rotation * Vector(-xs,-ys, zs)
        nyFaceP2 = Rotation * Vector( xs,-ys, zs)
        nyFaceP3 = Rotation * Vector( xs,-ys,-zs)
        nyFaceP4 = Rotation * Vector(-xs,-ys,-zs)

        zFaceP1 = Rotation * Vector(-xs,-ys, zs)
        zFaceP2 = Rotation * Vector(-xs, ys, zs)
        zFaceP3 = Rotation * Vector( xs, ys, zs)
        zFaceP4 = Rotation * Vector( xs,-ys, zs)

        nzFaceP1 = Rotation * Vector(-xs,-ys,-zs)
        nzFaceP2 = Rotation * Vector(-xs, ys,-zs)
        nzFaceP3 = Rotation * Vector( xs, ys,-zs)
        nzFaceP4 = Rotation * Vector( xs,-ys,-zs)

        xFaceX = np.array([xFaceP1.x, xFaceP2.x, xFaceP3.x, xFaceP4.x])
        xFaceY = np.array([xFaceP1.y, xFaceP2.y, xFaceP3.y, xFaceP4.y])
        xFaceZ = np.array([xFaceP1.z, xFaceP2.z, xFaceP3.z, xFaceP4.z])

        nxFaceX = np.array([nxFaceP1.x, nxFaceP2.x, nxFaceP3.x, nxFaceP4.x])
        nxFaceY = np.array([nxFaceP1.y, nxFaceP2.y, nxFaceP3.y, nxFaceP4.y])
        nxFaceZ = np.array([nxFaceP1.z, nxFaceP2.z, nxFaceP3.z, nxFaceP4.z])

        yFaceX = np.array([yFaceP1.x, yFaceP2.x, yFaceP3.x, yFaceP4.x])
        yFaceY = np.array([yFaceP1.y, yFaceP2.y, yFaceP3.y, yFaceP4.y])
        yFaceZ = np.array([yFaceP1.z, yFaceP2.z, yFaceP3.z, yFaceP4.z])

        nyFaceX = np.array([nyFaceP1.x, nyFaceP2.x, nyFaceP3.x, nyFaceP4.x])
        nyFaceY = np.array([nyFaceP1.y, nyFaceP2.y, nyFaceP3.y, nyFaceP4.y])
        nyFaceZ = np.array([nyFaceP1.z, nyFaceP2.z, nyFaceP3.z, nyFaceP4.z])

        zFaceX = np.array([zFaceP1.x, zFaceP2.x, zFaceP3.x, zFaceP4.x])
        zFaceY = np.array([zFaceP1.y, zFaceP2.y, zFaceP3.y, zFaceP4.y])
        zFaceZ = np.array([zFaceP1.z, zFaceP2.z, zFaceP3.z, zFaceP4.z])

        nzFaceX = np.array([nzFaceP1.x, nzFaceP2.x, nzFaceP3.x, nzFaceP4.x])
        nzFaceY = np.array([nzFaceP1.y, nzFaceP2.y, nzFaceP3.y, nzFaceP4.y])
        nzFaceZ = np.array([nzFaceP1.z, nzFaceP2.z, nzFaceP3.z, nzFaceP4.z])

        xFace = np.zeros([4,3])
        xFace[:,0] = xFaceX
        xFace[:,1] = xFaceY
        xFace[:,2] = xFaceZ

        nxFace = np.zeros([4,3])
        nxFace[:,0] = nxFaceX
        nxFace[:,1] = nxFaceY
        nxFace[:,2] = nxFaceZ

        yFace = np.zeros([4,3])
        yFace[:,0] = yFaceX
        yFace[:,1] = yFaceY
        yFace[:,2] = yFaceZ

        nyFace = np.zeros([4,3])
        nyFace[:,0] = nyFaceX
        nyFace[:,1] = nyFaceY
        nyFace[:,2] = nyFaceZ

        zFace = np.zeros([4,3])
        zFace[:,0] = zFaceX
        zFace[:,1] = zFaceY
        zFace[:,2] = zFaceZ

        nzFace = np.zeros([4,3])
        nzFace[:,0] = nzFaceX
        nzFace[:,1] = nzFaceY
        nzFace[:,2] = nzFaceZ

        ax3.clear()
        ax3.set_xlim(-ratio,ratio)
        ax3.set_ylim(-ratio,ratio)
        ax3.set_zlim(-ratio,ratio)
        ax3.grid(False)
        ln8,  = ax3.plot([0,xaxis.x],[0,xaxis.y],[0,xaxis.z],c='red',   linewidth=1.0, zorder=5, linestyle='--')
        ln9,  = ax3.plot([0,yaxis.x],[0,yaxis.y],[0,yaxis.z],c='green', linewidth=1.0, zorder=5, linestyle='--')
        ln10, = ax3.plot([0,zaxis.x],[0,zaxis.y],[0,zaxis.z],c='blue',  linewidth=1.0, zorder=5, linestyle='--')
        ln11, = ax3.plot([0,maxisLine.x],[0,maxisLine.y],[0,maxisLine.z],c='orange',linewidth=1.0, zorder=5, linestyle='-')
        ax3.add_collection(Poly3DCollection([xFace, yFace, zFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))
        ax3.add_collection(Poly3DCollection([nxFace, nyFace, nzFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))

        scale = 2.0
        ax5.clear()
        ax5.set_xlim(-ratio*scale,ratio*scale)
        ax5.set_ylim(-ratio*scale,ratio*scale)
        ax5.set_zlim(-ratio*scale,ratio*scale)
        ax5.grid(False)
        ln15,  = ax5.plot([0,xaxis.x],[0,xaxis.y],[0,xaxis.z],c='red',   linewidth=1.0, zorder=5, linestyle='--')
        ln16,  = ax5.plot([0,yaxis.x],[0,yaxis.y],[0,yaxis.z],c='green', linewidth=1.0, zorder=5, linestyle='--')
        ln17, = ax5.plot([0,zaxis.x],[0,zaxis.y],[0,zaxis.z],c='blue',  linewidth=1.0, zorder=5, linestyle='--')
        ax5.add_collection(Poly3DCollection([xFace, yFace, zFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))
        ax5.add_collection(Poly3DCollection([nxFace, nyFace, nzFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))

        ax6.clear()
        ax6.set_xlim(-ratio*scale,ratio*scale)
        ax6.set_ylim(-ratio*scale,ratio*scale)
        ax6.set_zlim(-ratio*scale,ratio*scale)
        ax6.grid(False)
        ln18,  = ax6.plot([0,xaxis.x],[0,xaxis.y],[0,xaxis.z],c='red',   linewidth=1.0, zorder=5, linestyle='--')
        ln19,  = ax6.plot([0,yaxis.x],[0,yaxis.y],[0,yaxis.z],c='green', linewidth=1.0, zorder=5, linestyle='--')
        ln20, = ax6.plot([0,zaxis.x],[0,zaxis.y],[0,zaxis.z],c='blue',  linewidth=1.0, zorder=5, linestyle='--')
        ax6.add_collection(Poly3DCollection([xFace, yFace, zFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))
        ax6.add_collection(Poly3DCollection([nxFace, nyFace, nzFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))

        ax7.clear()
        ax7.set_xlim(-ratio*scale,ratio*scale)
        ax7.set_ylim(-ratio*scale,ratio*scale)
        ax7.set_zlim(-ratio*scale,ratio*scale)
        ax7.grid(False)
        ln21,  = ax7.plot([0,xaxis.x],[0,xaxis.y],[0,xaxis.z],c='red',   linewidth=1.0, zorder=5, linestyle='--')
        ln22,  = ax7.plot([0,yaxis.x],[0,yaxis.y],[0,yaxis.z],c='green', linewidth=1.0, zorder=5, linestyle='--')
        ln23, = ax7.plot([0,zaxis.x],[0,zaxis.y],[0,zaxis.z],c='blue',  linewidth=1.0, zorder=5, linestyle='--')
        ax7.add_collection(Poly3DCollection([xFace, yFace, zFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))
        ax7.add_collection(Poly3DCollection([nxFace, nyFace, nzFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))

        ax3.set_title(f'3D View\nFrame = Angular Momentum Vector', fontsize=10, fontname='monospace')
        ax5.set_title(f'Perspective Along X', fontsize=10, fontname='monospace', y=-0.01)
        ax6.set_title(f'Perspective Along Y', fontsize=10, fontname='monospace', y=-0.01)
        ax7.set_title(f'Perspective Along Z', fontsize=10, fontname='monospace', y=-0.01)

        if frame > 0:
            ax1.set_xlim(Times[0]-1, Times[frame]+10)
            ax2.set_xlim(Times[0]-1, Times[frame]+10)
            ax4.set_xlim(Times[0]-1, Times[frame]+10)
            maxV = 0
            for rate in Bodyrates[0: frame]:
                lis = abs(np.array([rate.x, rate.y, rate.z]))
                if max(lis) > maxV:
                    maxV = max(lis)

            ax2.set_ylim(-1.5*maxV,1.5*maxV)
            
            ax1.legend(loc='center left', bbox_to_anchor=(1,0.5))
            ax2.legend(loc='center left', bbox_to_anchor=(1,0.5))
            ax4.legend(loc='center left', bbox_to_anchor=(1,0.5))

        return ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9, ln10, ln11, ln12, ln13, ln14, \
                ln15, ln16, ln17, ln18, ln19, ln20, ln21, ln22, ln23,

    print("\nRun Animation (from "+str(Times[0])+" to "+str(Times[-1])+")")
    anim = FuncAnimation(
        fig,
        update,
        frames = tqdm(np.arange(0, len(Times), 1), position=0, desc='Animating Attitude Track', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}'),
        interval = 30,
        init_func = init,
        blit = True
    )

    if saveas == "mp4":
        anim.save("Attitudetrack.mp4", fps=30, dpi=dpi)
    if saveas == "gif":
        anim.save("Attitudetrack.gif", writer='pillow', fps=30, dpi=dpi)

    plt.close()


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
    # ax.coastlines(resolution='110m')
    
    # gl = ax.gridlines(draw_labels=True)
    # gl.top_labels = False
    # gl.right_labels = False

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='white', alpha = 0.25,
                  linestyle='--')

    # labels on bottom and left axes
    gl.top_labels = False
    gl.right_labels = False

    # define the label style
    gl.xlabel_style = {'size': 10, 'color': 'black'}
    gl.ylabel_style = {'size': 10, 'color': 'black'}

    # now we define exactly which ones to label and spruce up the labels
    gl.xlocator = mticker.FixedLocator([-180, -135, -90, -45, 0, 45, 90, 135, 180])
    gl.ylocator = mticker.FixedLocator([-80, -60, -40, -20, 0, 20, 40, 60, 80])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

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

    plt.suptitle(f'{spacecraft.name}\n{dateTime}')
    plot.set_alpha([ item<=currentTime for item in Times])
    ax.add_feature(Nightshade(dateTime, alpha=0.3))

    index = Times.index(currentTime)
    spot, = ax.plot(Longitudes[index], Latitudes[index] , marker='o', color='white', markersize=12,
            alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)
    
    lat = str('%.2F'% Latitudes[index]+"°")
    lon = str('%.2F'% Longitudes[index]+"°")
    alt = str('%.2F'% Altitudes[index]+"km")
    txt = "lat: "+lat+"\nlon: "+lon+"\nalt: "+alt
    geodetic_transform = ccrs.PlateCarree()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=+15, y=+0)

    label = ax.text(Longitudes[index], Latitudes[index], txt,
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform, fontsize=8,
        bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'), fontdict={'family':'monospace'})
    
    # import matplotlib
    # print(matplotlib.artist.getp(spot))
    # spot.set_data([0,0])
    # label.set(position=[0,0])
    # label.set(text="AA")

    plt.show()

class animatedGroundTrack(object):

    def __init__(self, recorder: Recorder, sample: int = 0, saveas: str = "mp4", dpi: int = 300):

        df = pd.DataFrame.from_dict(recorder.dataDict)

        if sample > 0:
            df = df.iloc[::sample,:]   

        spacecraft = recorder.attachedTo
        self.name = spacecraft.name
        self.system = spacecraft.system

        self.lat = [ item[0] for item in df['Location'].values.tolist()[1:] ]
        self.lon = [ item[1] for item in df['Location'].values.tolist()[1:] ]
        self.alt = [ item[2] for item in df['Location'].values.tolist()[1:] ]
        self.datetimes = [ item for item in df['Datetime'] ][1:]
        self.time = [ (item - self.system.datetime0).total_seconds() for item in df['Datetime'][1:] ]

        self.fig = plt.figure(figsize=(10, 5))

        self.ax = plt.axes(projection=ccrs.PlateCarree())

        self.ax.stock_img()
        # self.ax.coastlines(resolution='110m')
        self.NS = self.ax.add_feature(Nightshade(self.system.datetime0, alpha=0.3))


        gl = self.ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                    linewidth=1, color='white', alpha = 0.25,
                    linestyle='--')

        # labels on bottom and left axes
        gl.top_labels = False
        gl.right_labels = False

        # define the label style
        gl.xlabel_style = {'size': 10, 'color': 'black'}
        gl.ylabel_style = {'size': 10, 'color': 'black'}

        # now we define exactly which ones to label and spruce up the labels
        gl.xlocator = mticker.FixedLocator([-180, -135, -90, -45, 0, 45, 90, 135, 180])
        gl.ylocator = mticker.FixedLocator([-80, -60, -40, -20, 0, 20, 40, 60, 80])
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        # gl = self.ax.gridlines(draw_labels=True)
        # gl.top_labels = False
        # gl.right_labels = False

        self.plot = plt.scatter(self.lon, self.lat,
            color='red', s=0.2, zorder=2.5,
            transform=ccrs.PlateCarree(),
            )
        
        self.spot, = self.ax.plot(self.lon[0], self.lat[0] , marker='o', color='white', markersize=12,
                alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)
        
        geodetic_transform = ccrs.PlateCarree()._as_mpl_transform(self.ax)
        text_transform = offset_copy(geodetic_transform, units='dots', x=+15, y=+0)

        lat = str('%.2F'% self.lat[0]+"°")
        lon = str('%.2F'% self.lon[0]+"°")
        alt = str('%.2F'% self.alt[0]+"km")
        txt = "lat: "+lat+"\nlon: "+lon+"\nlat: "+alt
        self.text = self.ax.text(self.lon[0], self.lat[0], txt,
            verticalalignment='center', horizontalalignment='left',
            transform=text_transform, fontsize=8,
            bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'), fontdict={'family':'monospace'})
        
        length = (len(self.time)//10)

        plt.suptitle(f'{spacecraft.name}\n{self.system.datetime0}')

        print("\nRun Animation (from "+str(self.time[0])+" to "+str(self.time[-1])+")")
        anim = FuncAnimation(
            self.fig,
            self.update,
            frames = tqdm(np.linspace(self.time[0], self.time[-1], length),  position=0, desc='Animating Ground Track', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}'),
            interval = 1
        )

        if saveas == "mp4":
            anim.save("Groundtrack.mp4", fps=30, dpi=dpi)
        if saveas == "gif":
            anim.save("Groundtrack.gif", writer='pillow', fps=30, dpi=dpi)

        plt.close()

    def update(self, t_current):

        dt_current = self.system.datetime0 + datetime.timedelta(seconds=t_current)
        self.NS.set_visible(False)
        self.NS = self.ax.add_feature(Nightshade(dt_current, alpha=0.3))

        plt.suptitle(f'{self.name}\n{dt_current}')
        self.plot.set_alpha(self.time<=t_current)

        index = len([ item for item in self.time if item <= t_current ]) - 1
   
        self.spot.set_data([self.lon[index], self.lat[index]])

        lat = str('%.2F'% self.lat[index]+"°")
        lon = str('%.2F'% self.lon[index]+"°")
        alt = str('%.2F'% self.alt[index]+"km")
        txt = "lat: "+lat+"\nlon: "+lon+"\nalt: "+alt
        self.text.set(position=[self.lon[index], self.lat[index]], text=txt)

        return self.plot

