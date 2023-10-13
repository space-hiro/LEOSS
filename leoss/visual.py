from .main import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.transforms import offset_copy
from matplotlib import gridspec

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

def attitudeTrack(recorder: Recorder, sample: int = 0, saveas: str = "mp4", dpi: int = 300, frameRef: str = 'Inertial'):

    df = pd.DataFrame.from_dict(recorder.dataDict)

    spacecraft = recorder.attachedTo
    system = spacecraft.system

    xs =spacecraft.size.x/min(spacecraft.size)
    ys =spacecraft.size.y/min(spacecraft.size)
    zs =spacecraft.size.z/min(spacecraft.size)

    ratio = max(spacecraft.size)/min(spacecraft.size)

    if sample > 0:
        df1 = df.iloc[::sample,:]   
        df2 = df.iloc[df.index[-1]:,:]
        df1 = pd.concat([df1, df2], ignore_index=True, axis=0)
    
    elif sample == 0:
        df1 = df

    States      = [ item for item in df1['State'].values.tolist()[:] ]
    Positions   = [ item.position for item in df1['State'].values.tolist()[:] ]
    Quaternions = [ item.quaternion for item in df1['State'].values.tolist()[:] ]
    Bodyrates   = [ item.bodyrate*R2D for item in df1['State'].values.tolist()[:] ]
    Datetimes   = [ item for item in df1['Datetime'] ][:]
    Times       = [ (item - system.datetime0).total_seconds() for item in df1['Datetime'][:] ]

    # plt.style.use("seaborn-v0_8")
    fig = plt.figure(figsize=(18,9))
    fig.tight_layout()
    ax1 = fig.add_subplot(3,2,2)
    ax2 = fig.add_subplot(3,2,4)
    ax3 = fig.add_subplot(3,2,6)
    ax4 = fig.add_subplot(2,4,1, projection='3d')
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

    ln8, = ax3.plot([],[], label='roll')
    ln9, = ax3.plot([],[], label='pitch')
    ln10, = ax3.plot([],[], label='yaw')

    ln11, = ax4.plot([],[],[])
    ln12, = ax4.plot([],[],[])
    ln13, = ax4.plot([],[],[])
    ln14, = ax4.plot([],[],[])

    ln15, = ax5.plot([],[],[])
    ln16, = ax5.plot([],[],[])
    ln17, = ax5.plot([],[],[])

    ln18, = ax6.plot([],[],[])
    ln19, = ax6.plot([],[],[])
    ln20, = ax6.plot([],[],[])

    ln21, = ax7.plot([],[],[])
    ln22, = ax7.plot([],[],[])
    ln23, = ax7.plot([],[],[])
    
    ax1.grid(visible=True)
    ax2.grid(visible=True)
    ax3.grid(visible=True)

    ax4.view_init(30,20)
    ax5.view_init(0,0)
    ax6.view_init(0,90)
    ax7.view_init(90,0)

    ax1.title.set_text(f'Quaternion')
    ax2.title.set_text(f'Body Rates (deg/s)')
    ax3.title.set_text(f'Euler Angles (deg)')

    def init():
        ax1.set_ylim(-1.1,1.1)
        ax3.set_ylim(-190,190)

        for axis in ax5.xaxis, ax6.yaxis, ax7.zaxis:
            axis.set_label_position('none')
            axis.set_ticks_position('none')

        ax6.zaxis.set_label_position('upper')
        ax6.zaxis.set_ticks_position('upper')    

        plt.subplots_adjust(wspace=0.1, hspace=0.3, left=None, right=None)   

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
        ln8.set_data(Times[0: frame], Roll[0: frame])
        ln9.set_data(Times[0: frame], Pitch[0: frame])
        ln10.set_data(Times[0: frame], Yaw[0: frame])    

        ln1.set_label("q0 = "+str('%+.4F' % QuatW[frame]))
        ln2.set_label("q1 = "+str('%+.4F' % QuatX[frame]))
        ln3.set_label('q2 = '+str('%+.4F' % QuatY[frame]))
        ln4.set_label('q3 = '+str('%+.4F' % QuatZ[frame]))
        ax1.legend(loc='lower left', prop={'family':'monospace'}, ncol=4)    

        ln5.set_label("X = "+str('%+.4F' % RateX[frame]))
        ln6.set_label("Y = "+str('%+.4F' % RateY[frame]))
        ln7.set_label('Z = '+str('%+.4F' % RateZ[frame]))
        ax2.legend(loc='lower left', prop={'family':'monospace'}, ncol=3)   

        ln8.set_label("Roll = "+str('%+.4F' % Roll[frame]))
        ln9.set_label("Pith = "+str('%+.4F' % Pitch[frame]))
        ln10.set_label('Yaw = '+str('%+.4F' % Yaw[frame]))
        ax3.legend(loc='lower left', prop={'family':'monospace'}, ncol=3)  

        xaxis = Vector(1,0,0)
        yaxis = Vector(0,1,0)
        zaxis = Vector(0,0,1)
        maxis = Matrices[frame] * spacecraft.inertia*Bodyrates[frame]

        maxisZ = maxis.normalize()
        if maxisZ.cross(zaxis).magnitude() == 0:
            maxisX = maxisZ.cross(xaxis).normalize()
        else:
            maxisX = maxisZ.cross(zaxis).normalize()
        maxisY = maxisZ.cross(maxisX).normalize()
        MomentumRotation = Matrix(maxisX, maxisY,maxisZ)

        Rotation = Matrices[frame]
        maxisLine = maxis.normalize() * ratio * 2

        if frameRef == 'Momentum':
            Rotation = MomentumRotation.transpose() * Matrices[frame]
            maxisLine = MomentumRotation.transpose() * maxis.normalize() * ratio * 2


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

        ax4.clear()
        ax4.set_xlim(-ratio,ratio)
        ax4.set_ylim(-ratio,ratio)
        ax4.set_zlim(-ratio,ratio)
        ax4.grid(False)
        ln11,  = ax4.plot([0,xaxis.x],[0,xaxis.y],[0,xaxis.z],c='red',   linewidth=1.0, zorder=5, linestyle='--')
        ln12,  = ax4.plot([0,yaxis.x],[0,yaxis.y],[0,yaxis.z],c='green', linewidth=1.0, zorder=5, linestyle='--')
        ln13, = ax4.plot([0,zaxis.x],[0,zaxis.y],[0,zaxis.z],c='blue',  linewidth=1.0, zorder=5, linestyle='--')
        ln14, = ax4.plot([0,maxisLine.x],[0,maxisLine.y],[0,maxisLine.z],c='orange',linewidth=1.0, zorder=5, linestyle='-')
        ax4.add_collection(Poly3DCollection([xFace, yFace, zFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))
        ax4.add_collection(Poly3DCollection([nxFace, nyFace, nzFace], facecolors='cyan', linewidths=1, edgecolors='k', alpha=.50))

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

        frameText = ''
        if frameRef == 'Inertial':
            frameText = 'ECIF'
        if frameRef == 'Momentum':
            frameText = 'Angular Momentum Vector'

        ax4.set_title(f'3D View\nFrame = {frameText}', fontsize=10, fontname='monospace')
        ax5.set_title(f'Perspective Along X', fontsize=10, fontname='monospace', y=-0.01)
        ax6.set_title(f'Perspective Along Y', fontsize=10, fontname='monospace', y=-0.01)
        ax7.set_title(f'Perspective Along Z', fontsize=10, fontname='monospace', y=-0.01)

        if frame > 0:
            ax1.set_xlim(Times[0]-1, Times[frame]+10)
            ax2.set_xlim(Times[0]-1, Times[frame]+10)
            ax3.set_xlim(Times[0]-1, Times[frame]+10)
            maxV = 0
            for rate in Bodyrates[0: frame]:
                lis = abs(np.array([rate.x, rate.y, rate.z]))
                if max(lis) > maxV:
                    maxV = max(lis)

            ax2.set_ylim(-1.5*maxV,1.5*maxV)

        return ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9, ln10, ln11, ln12, ln13, ln14, \
                ln15, ln16, ln17, ln18, ln19, ln20, ln21, ln22, ln23,

    print("\nRun Animation (from "+str(Times[0])+" to "+str(Times[-1])+", step="+str(Times[1]-Times[0])+")")
    anim = FuncAnimation(
        fig,
        update,
        frames = tqdm(np.arange(0, len(Times), 1), total=len(Times)-1, position=0, desc='Animating Attitude Track', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}'),
        interval = 30,
        init_func = init,
        blit = True
    )

    if saveas == "mp4":
        anim.save("Attitudetrack.mp4", fps=30, dpi=dpi)
    if saveas == "gif":
        anim.save("Attitudetrack.gif", writer='pillow', fps=30)

    plt.close()


def groundTrack(recorder: Recorder, dateTime = -1):

    # get datadict from recorder as dataframe
    df = pd.DataFrame.from_dict(recorder.dataDict)

    # variable for spacecraft and system
    spacecraft = recorder.attachedTo
    system     = spacecraft.system

    # split data columns from recorder into components
    Latitudes  = [ item[0] for item in df['Location'].values.tolist()[:] ]
    Longitudes = [ item[1] for item in df['Location'].values.tolist()[:] ]
    Altitudes  = [ item[2] for item in df['Location'].values.tolist()[:] ]
    Datetimes  = [ item for item in df['Datetime'] ][:]
    Times      = [ (item - system.datetime0).total_seconds() for item in df['Datetime'][:] ]

    # initialize figure and projection 
    fig = plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # add the default global map
    ax.stock_img()

    # create gridlines
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

    # plot the scatter points for longitude and latitude track
    plot = plt.scatter(Longitudes, Latitudes,
        color='red', s=0.2, zorder=2.5,
        transform=ccrs.PlateCarree(),
        )
    
    # if datetime input is -1 then set the datetime as current datetime (plot all from Start to End)
    if dateTime == -1:
        dateTime = system.datenow()

    # replace datetime input as a datetime object, from int or float
    currentTime = 0
    if isinstance(dateTime, datetime.datetime):
        currentTime = (dateTime - system.datetime0).total_seconds()
    elif isinstance(dateTime, int) or isinstance(dateTime, float):
        if dateTime > Times[0] and dateTime <= Times[-1]:
            currentTime = dateTime
            dateTime = (system.datetime0+datetime.timedelta(seconds=currentTime))
        else:
            raise ValueError("Datetime input should valid time")
    else:
        raise TypeError("Datetime input should be int, float or datettime type")
    
    # create a super title with name of spacecraft and datetime
    plt.suptitle(f'{spacecraft.name}\n{dateTime}')

    # set the visibility of the track to only show the track from start time to the input time
    plot.set_alpha([ item<=currentTime for item in Times])

    # show the nightshade transition on the global map
    ax.add_feature(Nightshade(dateTime, alpha=0.3))

    # create a spot on the current location given the time
    index = Times.index(currentTime)
    spot, = ax.plot(Longitudes[index], Latitudes[index] , marker='o', color='white', markersize=12,
            alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)
    
    # create a legend on the current location with details on lat,lon and lat
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

    plt.show()

def animateGroundTrack(recorder: Recorder, sample: int = 0, saveas: str = 'mp4', dpi: int = 300):

    # get datadict from recorder as dataframe
    df = pd.DataFrame.from_dict(recorder.dataDict)

    # variable for spacecraft and system
    spacecraft = recorder.attachedTo
    system     = spacecraft.system

    if sample > 0:
        df1 = df.iloc[::sample,:]   
        df2 = df.iloc[df.index[-1]:,:]
        df1 = pd.concat([df1, df2], ignore_index=True, axis=0)
        
    elif sample == 0:
        df1 = df

    # split data columns from recorder into components
    Latitudes  = [ item[0] for item in df1['Location'].values.tolist()[:] ]
    Longitudes = [ item[1] for item in df1['Location'].values.tolist()[:] ]
    Altitudes  = [ item[2] for item in df1['Location'].values.tolist()[:] ]
    Datetimes  = [ item for item in df1['Datetime'] ][1:]
    Times      = [ (item - system.datetime0).total_seconds() for item in df1['Datetime'][:] ]

    # initialize figure and projection 
    fig = plt.figure(figsize=(12, 6))
    ax  = plt.axes(projection=ccrs.PlateCarree())

    # globe projection image
    ax.stock_img()

    # nighshade 
    animateGroundTrack.ns = ax.add_feature(Nightshade(system.datetime0, alpha=0.3))
    
    # gridlines
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

    # create scatter plot of the ground track
    plot = plt.scatter(Longitudes, Latitudes,
        color='red', s=0.2, zorder=2.5,
        transform=ccrs.PlateCarree(),
        )
    
    # create a spot for the current track position
    spot, = ax.plot(Longitudes[0], Latitudes[0] , marker='o', color='white', markersize=12,
            alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)

    # create legend / label on the current track position    
    geodetic_transform = ccrs.PlateCarree()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=+15, y=+0)

    lat = str('%.2F'% Latitudes[0]+"°")
    lon = str('%.2F'% Longitudes[0]+"°")
    alt = str('%.2F'% Altitudes[0]+"km")
    txt = "lat: "+lat+"\nlon: "+lon+"\nlat: "+alt
    text = ax.text(Longitudes[0], Latitudes[0], txt,
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform, fontsize=8,
        bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'), fontdict={'family':'monospace'})

    plt.suptitle(f'{spacecraft.name}\n{system.datetime0}')

    def init():
        return plot, spot, text,

    def update(frame):
        plt.suptitle(f'{spacecraft.name}\n{Datetimes[frame]}', fontname='monospace')

        animateGroundTrack.ns.set_visible(False)
        animateGroundTrack.ns = ax.add_feature(Nightshade(Datetimes[frame], alpha=0.3))
        current_time = (Datetimes[frame] - system.datetime0).total_seconds()
        plot.set_alpha( [item <= current_time for item in Times ])

        index = len([ item for item in Times if item <= current_time ]) - 1
   
        spot.set_data([Longitudes[index], Latitudes[index]])

        lat = str('%.2F'% Latitudes[index]+"°")
        lon = str('%.2F'% Longitudes[index]+"°")
        alt = str('%.2F'% Altitudes[index]+"km")
        txt = "lat: "+lat+"\nlon: "+lon+"\nalt: "+alt
        text.set(position=[Longitudes[index], Latitudes[index]], text=txt)       

        return plot, spot, text,

    print("\nRun Animation (from "+str(Times[0])+" to "+str(Times[-1])+", step="+str(Times[1]-Times[0])+")")
    anim = FuncAnimation(
        fig,
        update,
        frames = tqdm(np.arange(0, len(Times), 1), total=len(Times)-1,  position=0, desc='Animating Ground Track', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}'),
        interval = 30
    )

    if saveas == "mp4":
        anim.save("Groundtrack.mp4", fps=30, dpi=dpi)
    if saveas == "gif":
        anim.save("Groundtrack.gif", writer='pillow', fps=30)

    plt.close()

def sensorTrack(recorder: Recorder, sensor: str, sample: int = 0, saveas: str = 'mp4', dpi: int = 300):

    # get datadict from recorder as dataframe
    df = pd.DataFrame.from_dict(recorder.dataDict)

    # variable for spacecraft and system
    spacecraft = recorder.attachedTo
    system     = spacecraft.system

    if sample > 0:
        df1 = df.iloc[::sample,:]   
        df2 = df.iloc[df.index[-1]:,:]
        df1 = pd.concat([df1, df2], ignore_index=True, axis=0)

    elif sample == 0:
        df1 = df

    # split data columns from recorder into components
    SensorData = [ item for item in df1[sensor].values.tolist()[:] ]
    Latitudes  = [ item[0] for item in df1['Location'].values.tolist()[:] ]
    Longitudes = [ item[1] for item in df1['Location'].values.tolist()[:] ]
    Altitudes  = [ item[2] for item in df1['Location'].values.tolist()[:] ]
    Datetimes  = [ item for item in df1['Datetime'] ][:]
    Times      = [ (item - system.datetime0).total_seconds() for item in df1['Datetime'][:] ]

    SensorX = [ item.x for item in SensorData ]
    SensorY = [ item.y for item in SensorData ]
    SensorZ = [ item.z for item in SensorData ]

    # initialize figure and projection 
    # plt.style.use("seaborn-v0_8")
    fig = plt.figure(figsize=(12, 9))
    fig.tight_layout()
    gs = gridspec.GridSpec(2,1, height_ratios=[2, 1])
    ax1 = plt.subplot(gs[0], projection=ccrs.PlateCarree())
    ax2 = plt.subplot(gs[1])
    # ax1 = fig.add_subplot(3,1,1, height_ratio = 2, projection=ccrs.PlateCarree())
    # ax2 = fig.add_subplot(3,1,3)

    # globe projection image
    ax1.stock_img()

    # nighshade 
    animateGroundTrack.ns = ax1.add_feature(Nightshade(system.datetime0, alpha=0.3))
    
    # gridlines
    gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
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

    # create scatter plot of the ground track
    plot = ax1.scatter(Longitudes, Latitudes,
        color='red', s=0.2, zorder=2.5,
        transform=ccrs.PlateCarree(),
        )
    
    ln1, = ax2.plot([],[], label="X")
    ln2, = ax2.plot([],[], label="Y")
    ln3, = ax2.plot([],[], label="Z")

    # create a spot for the current track position
    spot, = ax1.plot(Longitudes[0], Latitudes[0] , marker='o', color='white', markersize=12,
            alpha=0.5, transform=ccrs.PlateCarree(), zorder=3.0)

    # create legend / label on the current track position    
    geodetic_transform = ccrs.PlateCarree()._as_mpl_transform(ax1)
    text_transform = offset_copy(geodetic_transform, units='dots', x=+15, y=+0)

    lat = str('%.2F'% Latitudes[0]+"°")
    lon = str('%.2F'% Longitudes[0]+"°")
    alt = str('%.2F'% Altitudes[0]+"km")
    txt = "lat: "+lat+"\nlon: "+lon+"\nlat: "+alt
    text = ax1.text(Longitudes[0], Latitudes[0], txt,
        verticalalignment='center', horizontalalignment='left',
        transform=text_transform, fontsize=8,
        bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'), fontdict={'family':'monospace'})

    plt.suptitle(f'{spacecraft.name}\n{system.datetime0}')

    ax2.title.set_text(f'{sensor} output')
    ax2.grid(visible=True)

    def init():

        plt.subplots_adjust(wspace=0, right=0, left=0)   

        return plot, spot, text, ln1, ln2, ln3,

    def update(frame):
        plt.suptitle(f'{spacecraft.name}\n{Datetimes[frame]}', fontname='monospace')

        animateGroundTrack.ns.set_visible(False)
        animateGroundTrack.ns = ax1.add_feature(Nightshade(Datetimes[frame], alpha=0.3))
        current_time = (Datetimes[frame] - system.datetime0).total_seconds()
        plot.set_alpha( [item <= current_time for item in Times ])

        ln1.set_data(Times[0: frame], SensorX[0: frame])
        ln2.set_data(Times[0: frame], SensorY[0: frame])
        ln3.set_data(Times[0: frame], SensorZ[0: frame])

        ln1.set_label("X = "+str('%+.3E' % SensorX[frame]))
        ln2.set_label("Y = "+str('%+.3E' % SensorY[frame]))
        ln3.set_label('Z = '+str('%+.3E' % SensorZ[frame]))
        ax2.legend(loc='lower left', prop={'family':'monospace'}, ncol=3)

        index = len([ item for item in Times if item <= current_time ]) - 1
   
        spot.set_data([Longitudes[index], Latitudes[index]])

        lat = str('%.2F'% Latitudes[index]+"°")
        lon = str('%.2F'% Longitudes[index]+"°")
        alt = str('%.2F'% Altitudes[index]+"km")
        txt = "lat: "+lat+"\nlon: "+lon+"\nalt: "+alt
        text.set(position=[Longitudes[index], Latitudes[index]], text=txt)   

        if frame > 0:
            maxV = 0
            for rate in SensorData[0: frame]:
                lis = abs(np.array([rate.x, rate.y, rate.z]))
                if max(lis) > maxV:
                    maxV = max(lis)
            if maxV != 0:
                ax2.set_ylim(-1.5*maxV,1.5*maxV)

        ax2.set_xlim(Times[0]-1, Times[frame]+10)    

        return plot, spot, text, ln1, ln2, ln3

    print("\nRun Animation (from "+str(Times[0])+" to "+str(Times[-1])+", step="+str(Times[1]-Times[0])+")")
    anim = FuncAnimation(
        fig,
        update,
        frames = tqdm(np.arange(0, len(Times), 1), total=len(Times)-1,  position=0, desc='Animating Sensor Track', bar_format='{l_bar}{bar:25}{r_bar}{bar:-25b}'),
        interval = 30
    )

    if saveas == "mp4":
        anim.save("Sensortrack.mp4", fps=30, dpi=dpi)
    if saveas == "gif":
        anim.save("Sensortrack.gif", writer='pillow', fps=30)

    plt.close()
