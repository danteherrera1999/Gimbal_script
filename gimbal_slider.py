import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.widgets import Slider
d2r = np.pi / 180
R_cyl = 1
L_cyl = -12
R_base = 3
s = 9
points = np.array([[R_cyl*np.cos(i * 2 * np.pi / s),R_cyl*np.sin(i * 2 * np.pi / s),L_cyl] for i in range(s+1)]+[[R_cyl*np.cos(i * 2 * np.pi / s),R_cyl*np.sin(i * 2 * np.pi / s),0] for i in range(s+1)]).T
fixpoints_base = np.array([R_base * np.cos(np.arange(3) * 2 * np.pi / 3),R_base * np.sin(np.arange(3) * 2 * np.pi / 3),np.arange(3)*0])
fixpoints = fixpoints_base.copy()*R_cyl/R_base
fixpoints[2] += L_cyl/3
T2 = lambda phi: np.array([[1,0,0],
                           [0,np.cos(phi),-np.sin(phi)],
                           [0,np.sin(phi),np.cos(phi)]])
T1 = lambda theta: np.array([[np.cos(theta),0,-np.sin(theta)],
                             [0,1,0],
                             [np.sin(theta),0,np.cos(theta)]])
T_G_2_I = lambda theta, phi: np.matmul(T1(theta),T2(phi))
transform = lambda theta,phi: np.matmul(T_G_2_I(theta,phi),points)
transform_fp = lambda theta,phi: np.matmul(T_G_2_I(theta,phi),fixpoints)
surface_data = lambda theta,phi: np.array([[axis[:s+1],axis[s+1:]] for axis in transform(theta,phi)])
fig = plt.figure()
ax = plt.axes(projection = '3d')
cyl = ax.plot_surface(*surface_data(0,0),color='mediumpurple',alpha=.75)
#Create Axis
ax_t = plt.axes([.25,.07,.65,.03])
ax_p = plt.axes([.25,.02,.65,.03])
#Create Sliders
t = Slider(ax_t,'Theta',-90,90,0)
p = Slider(ax_p,'Phi',-90,90,0)
mag = lambda vec: round(100*np.sqrt(np.dot(vec,vec)))/100
def condition():
    ax.set_ylim3d(-5,5)
    ax.set_xlim3d(-5,5)
    ax.set_zlim3d(-12,1)
    ax.plot_surface(*np.array([[[5, 5], [-5, -5]], [[5, -5], [5, -5]], [[0, 0], [0, 0]]]),alpha=.25)
    ax.scatter(*fixpoints_base,color='black')
def members(theta,phi):
    x,y,z = fixpoints_base
    xp,yp,zp = transform_fp(theta,phi)
    fp_dat = np.array([np.array([x,xp]).T,np.array([y,yp]).T,np.array([z,zp]).T])
    ax.scatter(xp,yp,zp,color='black')
    [ax.plot3D(*fp_dat[:,i],linewidth=3,label=f"L{1+i}: {mag(fp_dat.T[1][i]-fp_dat.T[0][i])}") for i in range(3)]
    ax.legend()
condition()
members(0,0)
ax.set_title(r"Gimbal | $\theta$: " + str(round(0 / d2r * 100) / 100) + r" | $\phi$: " + str(round(0 / d2r * 100) / 100))
def update(val):
    ax.clear()
    condition()
    theta, phi = t.val * d2r,p.val * d2r
    members(theta,phi)
    ax.set_title(r"Gimbal | $\theta$: "+ str(round(theta/d2r*100)/100) + r" | $\phi$: " + str(round(phi/d2r*100)/100))
    ax.plot_surface(*surface_data(theta,phi),color='mediumpurple',alpha=.75)
#Update Call
t.on_changed(update)
p.on_changed(update)
plt.show()