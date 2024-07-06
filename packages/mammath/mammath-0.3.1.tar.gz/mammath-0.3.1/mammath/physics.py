from .constants import *
from .operations import *
import numpy as np
from .geometry import *
from tabulate import tabulate


"""
PHYSICS
"""

#Force, Mass, Acceleration - F=ma
def Force(m, a):
    return m*a
def Mass(f, a):
    return f/a
def Acceleration(f, m):
    return f/m

#Speed, Distance, Time - S=d/t
def Speed(d, t):
    return d/t
def Distance(s, t):
    return s*t
def Time(s, d):
    return s*d

class Planet:
    def __init__(self, name, mass, radius, semi_major_axis, orbital_period, eccentricity):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.semi_major_axis = semi_major_axis
        self.orbital_period = orbital_period
        self.eccentricity = eccentricity

    def as_dict(self):
        return {
            'Name': self.name,
            'Mass (kg)': self.mass,
            'Radius (km)': self.radius,
            'Semi-major Axis (km)': self.semi_major_axis,
            'Orbital Period (Earth days)': self.orbital_period,
            'Eccentricity': self.eccentricity
        }

class SolarSystem:
    def __init__(self):
        self.planets = [
            Planet('Mercury', 3.3011e23, 2439.7, 57_909_227, 87.9691, 0.2056),
            Planet('Venus', 4.8675e24, 6051.8, 108_209_475, 224.70069, 0.0067),
            Planet('Earth', 5.97237e24, 6371, 149_598_262, 365.25641, 0.0167),
            Planet('Mars', 6.4171e23, 3389.5, 227_943_824, 687.0, 0.0934),
            Planet('Jupiter', 1.8982e27, 69_911, 778_340_821, 4_332.59, 0.0489),
            Planet('Saturn', 5.6834e26, 58_232, 1_426_666_422, 10_759.22, 0.0565),
            Planet('Uranus', 8.6810e25, 25_362, 2_870_658_186, 30_688.5, 0.0463),
            Planet('Neptune', 1.02413e26, 24_622, 4_498_396_441, 60_182, 0.0095),
        ]

    def display_planet(self, name):
        """
        Displays all the information of a given planet in a table
        """
        planet = self.get_planet(name)
        if planet:
            table = tabulate([planet.as_dict()], headers='keys', tablefmt='pretty')
            print(table)
        else:
            print("Planet not found.")

    def get_planet(self, name):
        """
        Displays all of the information of a given planet
        """
        for planet in self.planets:
            if planet.name.lower() == name.lower():
                return planet
        return None
            
solar_system = SolarSystem()

def grav_f(m1, m2, distance):
    """
    Uses F = (G*M1*M2)/(r**2)
    """
    return (G*m1*m2)/(distance**2)

def grav_field(m, distance):
    """
   Gravitational field strength of the mass at the given distance.
    """
    return grav_f(m, 1, distance)

def temperature_pressure(pressure, mass, density):
    """
    Calculates the temperature of a body given the pressure, mass, and density of the body using the rearranged version of the ideal gas law - T(p) = (pm)/(dk)
    """
    return (pressure*mass)/(density*boltzmanns_constant)

def force_acceleration(m, v, u, t):
    """
    Uses the alternative equation to solve for force by subsitution acceleration = (v-u)/t into f = ma to get f = (m*(v-u))/t
    """
    return (m*(v-u))/t

def event_horizon(mass):
    """
    Computes the schwarzschild radius of a schwarzschild black hole given the mass of the black hole
    """
    return (2*G*mass)/speed_of_light**2

def separate_vectors(vector, theta, deg=True):
    if not deg:
        theta = 180 * theta / pi
    return (vector * cos(theta), vector * sin(theta))

def electric_field(q, r):
    """
    Calculates the acceleration from a point on an electromagnetic field
    """
    return q * coulomb_constant / r ** 2

def centripetal_acceleration(v, r):
    """
    Returns the centripetal acceleration for the given velocity and radius.
    """
    return v**2 / r

def centripetal_force(m, v, r):
    """
    Calculates the centripetal force of an object in a circular motion
    """
    return m * v ** 2 / r

def get_hookes(F, dx):
    """
    Returns the Hookes constant for the spring
    """
    return F / dx

def newtonian_gravity(m1, m2, d):
    """
    Returns the gravtitational force on two given objects of defined mass and centers d meters apart
    """
    return (m1*m2)/(d**2) * G

def suvat_solve(solve_for, s=None, u=None, v=None, a=None, t=None):
    """
    Uses the SUVAT equations to solve for s, u, v, a, t
    """
    equations = {
        's': lambda u, v, a, t: (u + v) * t / 2 if u and v and t else u * t + 0.5 * a * t**2,
        'u': lambda s, v, a, t: (s - 0.5 * a * t ** 2) / t if s else v - a * t,
        'v': lambda s, u, a, t: u + a * t,
        'a': lambda s, u, v, t: 2 * (s - (u + v) * t / 2) / t ** 2,
        't': lambda s, u, v, a: (v - u) / a,
    }

    if solve_for not in equations:
        raise ValueError("Invalid 'solve_for' value. Must be one of 's', 'u', 'v', 'a', or 't'.")

    variables = {'s': s, 'u': u, 'v': v, 'a': a, 't': t}
    known_vars = [var for var, value in variables.items() if value is not None]

    if len(known_vars) < 3:
        raise ValueError("There must be at least 3 known variables to solve the equation.")

    try:
        result = equations[solve_for](*[variables[var] for var in 'suvat' if var != solve_for])
    except ZeroDivisionError:
        raise ValueError("Cannot solve for the given variables, division by zero encountered.")

    return result

def vis_viva_equation(r_au, a_au, m1, m2):
    """
    Returns the orbital velocity of a body in an orbital motion
    """
    r = r_au * 1.496*10**11
    a = a_au * 1.496*10**11
    standard_grav_param = G*(m1 + m2)
    return sqrt(standard_grav_param*(2/r - 1/a))

def einsteinian_force(mass, acceleration, v):
    """
    Returns the force taking into account Einstein's laws of motion
    """
    return mass * acceleration / (1 - v**2/c**2)**(3/2)

def terminal_velocity(m, cross_area, drag_coefficient=0.294, air_density=1.225, gravity=g):
    """
    Calculates the terminal velocity based on mass and cross sectional area, drag_coefficient pre defined to headfirst human.
    """
    return sqrt(2*m*gravity/(cross_area*air_density*drag_coefficient))

def acceleration_constant(v, u, t):
    """
    Returns the acceleration when given v (final velocity), u (initial velocity, and t (time).
    """
    return (v-u)/t

def kinetic_energy(m, v):
    """
    Returns the kinetic energy for the given mass and velocity.
    """
    return 0.5 * m * v**2

def potential_energy(m, g, h):
    """
    Returns the potential energy for the given mass, gravity, and height.
    """
    return m * g * h

def power(w, t):
    """
    Returns the power as the ratio of work done to time.
    """
    return w / t

def momentum(m, v):
    """
    Returns the momentum for the given mass and velocity.
    """
    return m * v

def impulse_momentum_theorem(f, delta_t):
    """
    Returns the impulse, equal to the product of force and time interval.
    """
    return f * delta_t

def ideal_gas_law(p, v, n, T):
    """
    Returns the result of the ideal gas law equation for given pressure, volume, moles, gas constant, and temperature.
    """
    return p * v - n * R * T

def heat_capacity(m, c, delta_t):
    """
    Returns the heat capacity for the given mass, specific heat capacity, and temperature change.
    """
    return m * c * delta_t

def ohms_law(v, I, R):
    """
    Returns the result of Ohm's Law for the given voltage, current, and resistance.
    """
    return v - I * R

def coulombs_law(k, q1, q2, r):
    """
    Returns the electrostatic force between two charges according to Coulomb's Law.
    """
    return coulomb_constant * q1 * q2 / r**2

def faradays_law_em_induction(d_phi_b, dt):
    """
    Returns the induced electromotive force according to Faraday's Law of Electromagnetic Induction.
    """
    return -d_phi_b / dt

def lensmakers_equation(n, R1, R2):
    """
    Returns the focal length of a lens using the lensmaker's equation.
    """
    return (n - 1) * (1 / R1 - 1 / R2)

def time_dilation(delta_t0, v, c):
    """
    Returns the time dilation for a given proper time, relative velocity, and speed of light.
    """
    return delta_t0 / sqrt(1 - v**2 / c**2)

def length_contraction(length, v):
    """
    Returns the length contraction for a given proper length, relative velocity, and speed of light.
    """
    return length * sqrt((1 - v**2 / c**2))

def wave_speed(frequency, wavelength):
    """
    Returns the wave speed given the frequency and wavelength.
    """
    return frequency * wavelength

def boltzmann_entropy(W):
    """
    Returns the entropy according to Boltzmann's entropy formula.
    """
    return boltzmanns_constant * ln(W)

def particle_in_box_energy(n, L, m):
    """
    Returns the energy of a particle in a one-dimensional box for the given quantum number.
    """
    return (n**2 * pi**2 * h_bar**2) / (2 * m * L**2)

def planck_law(wavelength, T):
    """
    Returns the spectral radiance for a blackbody at a given temperature and wavelength.
    """
    return (2 * pi * h * c**2) / (wavelength**5 * (np.exp((h * c) / (wavelength * k * T)) - 1))

def lorentz_force(q, E, B, v):
    """
    Returns the Lorentz force experienced by a charged particle in an electric and magnetic field.
    """
    return q * (E + np.cross(v, B))

def lorentz_factor(v):
    """
    Returns the Lorentz factor for a given velocity.
    """
    return 1 / sqrt(1 - v**2 / c**2)

def decay_law(N0, lambda_, t):
    """
    Returns the number of radioactive nuclei remaining after a given time.
    """
    return N0 * e ** (-lambda_ * t)

def relativistic_doppler_shift(wavelength, v):
    """
    Returns the shifted wavelength due to the relativistic Doppler effect.
    """
    return wavelength * sqrt((1 + v/c) / (1 - v/c))

def escape_velocity(m, r):
    """
    Returns the escape velocity for a celestial body of mass m and radius r.
    """
    return sqrt(2 * G * m / r)

def heat_engine_efficiency(W, Qh):
    """
    Returns the efficiency of a heat engine given the work done and heat input.
    """
    return W / Qh

def first_law_of_thermodynamics(Q, W, U1, U2):
    """
    Returns the relationship between heat, work, and internal energy changes in a thermodynamic process.
    """
    return Q - W == U2 - U1

def de_broglie_wavelength(m, v):
    """
    Returns the de Broglie wavelength of a particle with a given mass and velocity.
    """
    return h_bar / (m * v)

def photon_energy(frequency):
    """
    Returns the energy of a photon given its frequency.
    """
    return h * frequency

def efs_line(d, L, lmd):
    """
    Perpendicular electric field strength L away from a line of uniform charge lmd and length L
    """
    return k_e * (L * lmd / (d * (d ** 2 + (L ** 2) / 4) ** (1/2)))

def efs_disk(d, R, lmd):
    """
    Perpendicular electric field strength L away from a disk of uniform charge lmd and radius R
    """
    return (lmd / (2 * epsilon_0)) * (1 - (d / (R ** 2 + d ** 2) ** (1/2)))

def orbital_v(d, m):
    """
    The orbital velocity of a body d distance away from mass m
    """
    return (G * m / d) ** (1/2)

def magnetic_field_solenoid(I, L, N):
    """
    Magnetic field at center of coils given current, length, and number of coils.
    """
    return vacuum_permeability * N * I / L

def magnetic_field_toroid(I, R, N):
    """
    Magnetic field at center of coils given current, radius, and number of coils.
    """
    return vacuum_permeability * N * I / R

def biot_savart_law(I, r):
    """
    Magnetic field r away from conductor enclosing current I.
    """
    return I * 10 ** -7 / r

def mutual_inductance(N1, N2, A1, L1):
    """
    Solenoid 1 of cross section A1 with N1 Loops over length L1 surrounded by N2 loops.
    """
    return vacuum_permeability * N1 * N2 * A1 / L1

def self_inductance(N, L, A):
    """
    Self inductance of solenoid with N loops, length L, and cross sectional area A.
    """
    return vacuum_permeability * N ** 2 * A  / L

def induced_emf(change_flux, N):
    """
    Faraday's Law in a solenoid.
    """
    return -N * change_flux

def change_magnetic_flux(A, theta_normal, dBdt):
    """
    Change in magnetic flux over surface of area A with field changing at angle theta.
    """
    return A * cos(theta_normal) * dBdt

def time_dilation_lorentz(t, lorentz_factor):
    """
    Dilation of time t (change in t) given the lorentz factor.
    """
    return t * lorentz_factor

def length_contraction_lorentz(l, lorentz_factor):
    """
    Change in length l (l shortens) given the lorentz factor from stationary reference frame.
    """
    return l / lorentz_factor

def v_from_lorentz(lorentz_factor):
    """
    Returns velocity when given the lorentz factor
    """
    return c * (1 - lorentz_factor ** -2) ** 0.5

def rayleigh_jeans_law(wavelength, temperature):
    """
    Computes the spectral radiance of a blackbody at a given temperature using the Rayleigh-Jeans Law.
    """
    spectral_radiance = (2 * c * k * temperature) / (wavelength ** 4)
    return spectral_radiance

def schrodinger_1d_infinite_potential_well(L, N, m=9.10938356e-31):
    """
    Solves the time-independent Schrödinger equation for a particle in a 1D infinite potential well.
    """
    dx = L / (N + 1)
    x = np.linspace(0, L, N)
    H = np.zeros((N, N))

    for i in range(N):
        H[i, i] = -2
        if i > 0:
            H[i, i - 1] = 1
        if i < N - 1:
            H[i, i + 1] = 1

    H = - (h_bar**2 / (2 * m * dx**2)) * H

    eigenvalues, eigenvectors = np.linalg.eigh(H)
    
    return eigenvalues, eigenvectors

def feynman_path_integral(x0, x1, T, N, V, m):
    """
    Computes the Feynman path integral for a particle moving from x0 to x1 in potential V(x)
    """
    paths = np.linspace(x0, x1, N)
    dt = T / N
    integral = 0.0

    for i in range(N-1):
        dx = paths[i+1] - paths[i]
        action = 0.5 * m * (dx / dt) ** 2 - V(paths[i]) * dt
        integral += np.exp(-1j * action / h_bar)
    
    return integral

def heat_transfer_finite_difference(L, T, alpha, Nx, Nt):
    """
    Simulates heat transfer in a 1D rod using the finite difference method.
    """
    dx = L / (Nx - 1)
    dt = T / Nt
    r = alpha * dt / dx**2

    u = np.zeros((Nt, Nx))
    u[0, :] = np.sin(np.pi * np.linspace(0, L, Nx) / L) 
    
    for n in range(0, Nt-1):
        for i in range(1, Nx-1):
            u[n+1, i] = u[n, i] + r * (u[n, i+1] - 2 * u[n, i] + u[n, i-1])
    
    return u

def photoelectric_effect_simulation(frequency, work_function, intensity, duration):
    """
    Simulates the photoelectric effect.
    """
    power_per_photon = h * frequency
    photon_flux = intensity / power_per_photon  
    area = 1.0 
    total_photons = photon_flux * area * duration

    if power_per_photon > work_function:
        excess_energy_per_photon = power_per_photon - work_function
        electrons_emitted = total_photons * (excess_energy_per_photon / power_per_photon)
    else:
        electrons_emitted = 0  

    return electrons_emitted

"""
END OF PHYSICS
"""
