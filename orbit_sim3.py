import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

#Set axes aspect to equal as orbits are almost circular; hence square is needed
ax = plt.figure(0).add_subplot(111, aspect='equal')

#Setting the title, axis labels, axis values and introducing a grid underlay
#Variable used so title can indicate user inputed date
plt.title('Inner Planetary Orbits at[user input date]')
plt.ylabel('x10^6 km')
plt.xlabel('x10^6 km')
ax.set_xlim(-300, 300)
ax.set_ylim(-300, 300)
plt.grid()

#Creating the point to represent the sun at the origin (not to scale), 
ax.scatter(0,0,s=200,color='y')
plt.annotate('Sun', xy=(0,-30))

#Implementing ellipse equations to generate the values needed to plot an ellipse
#Using only the planet's min (m) and max (M) distances from the sun
#Equations return '2a' (the ellipses width) and '2b' (the ellipses height)
def OrbitLength(M, m):
    a=(M+m)/2
    c=a-m
    e=c/a
    b=a*(1-e**2)**0.5
    print(a)
    print(b)
    return 2*a, 2*b

#This function uses the returned 2a and 2b for the ellipse function's variables
#Also generating the orbit offset (putting the sun at a focal point) using M and m
def PlanetOrbit(Name, M, m):
    w, h = OrbitLength(M, m)
    Xoffset= ((M+m)/2)-m
    Name = Ellipse(xy=((Xoffset),0), width=w, height=h, angle=0, linewidth=1, fill=False)
    ax.add_artist(Name)



from math import *

EPSILON = 1e-12
def solve_bisection(fn, xmin,xmax,epsilon = EPSILON):
  while True:
      xmid = (xmin + xmax) * 0.5
      if (xmax-xmin < epsilon):
        return xmid
      fn_mid = fn(xmid)
      fn_min = fn(xmin)
      if fn_min*fn_mid < 0:
          xmax = xmid
      else:
          xmin = xmid

'''
Found something similar at this gamedev question:
http://gamedev.stackexchange.com/questions/11116/kepler-orbit-get-position-on-the-orbit-over-time?newreg=e895c2a71651407d8e18915c38024d50

Equations taken from:
https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion#Position_as_a_function_of_time
'''
def SolveOrbit(rmax, rmin, t):
  # calculation precision
  epsilon = EPSILON
  # mass of the sun [kg]
  Msun = 1.9891e30
  # Newton's gravitational constant [N*m**2/kg**2]
  G = 6.6740831e-11
  # standard gravitational parameter
  mu = G*Msun
  # eccentricity
  eps = (rmax - rmin) / (rmax + rmin)
  # semi-latus rectum
  p = rmin * (1 + eps)
  # semi/half major axis
  a = p / (1 - eps**2)
  # period
  P = sqrt(a**3 / mu)
  # mean anomaly
  M = (t / P) % (2*pi)
  # eccentric anomaly
  def fn_E(E):
    return M - (E-eps*sin(E))
  E = solve_bisection(fn_E, 0, 2*pi)
  # true anomaly
  # TODO: what if E == pi?
  def fn_theta(theta):
    return (1-eps)*tan(theta/2)**2 - ((1+eps)*tan(E/2)**2)
  theta = solve_bisection(fn_theta, 0, pi)
  # if we are at the second half of the orbit
  if (E > pi):
    theta = 2*pi - theta
  # heliocentric distance
  r = a * (1 - eps * cos(E))
  return theta, r

def DrawPlanet(name, rmax, rmin, t):
  SCALE = 1e9
  theta, r = SolveOrbit(rmax * SCALE, rmin * SCALE, t)
  x = -r * cos(theta) / SCALE
  y = r * sin(theta) / SCALE
  planet = Circle((x, y), 8)
  ax.add_artist(planet)

#These are the arguments taken from hyperphysics.phy-astr.gsu.edu/hbase/solar/soldata2.html
#They are the planet names, max and min distances, and their longitudinal angle
#Also included is Halley's Comet, used to show different scale  and eccentricity
PlanetOrbit('Mercury', 69.8, 46.0)
PlanetOrbit('Venus', 108.9, 107.5)
PlanetOrbit('Earth', 152.1, 147.1)
PlanetOrbit('Mars', 249.1, 206.7)
PlanetOrbit("Halley's Comet",45900,88)
for i in range(0, 52):
  DrawPlanet('Earth', 152.1, 147.1, i/52 * 365.25 *60*60*24)
for i in range(-2, 3):
  DrawPlanet("Halley's Comet",45900,88, 7*i *60*60*24)
print(60*60*24*365)

plt.show()
