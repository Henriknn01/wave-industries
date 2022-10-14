import math
import random
from math import sin
from os.path import exists
import json
from matplotlib import pyplot as plt


# TODO: implement noise to the signals
#  link: https://stackoverflow.com/questions/14058340/adding-noise-to-a-signal-in-python

# TODO: implement navigatinal data + noise on the navigational data to simulate non-perfect navigation
#  + wind and wave disturbance

# TODO: USE SINUS WAVES for everything except nav data

# TODO: add effects of wave and wind to the boat

class SimulationComponent:
    pass


class Engine:
    def __init__(self, engine_name, signal_noise: int = 1, signal_amplitude: int = 1):
        self.name = engine_name
        self.signal_noise = signal_noise
        self.signal_amplitude = signal_amplitude
        self.rpm = 0
        self.temperature = 0
        self.fuel_consumption = 0
        self.base_rpm = 0
        self.base_fuel_consumption = 0
        self.mode = ""

    def set_mode(self, mode_base_rpm, mode_base_fuel_consumption, mode_name):
        self.base_rpm = mode_base_rpm
        self.base_fuel_consumption = mode_base_fuel_consumption
        self.mode = mode_name


# Generator inherits from engine as it is essentially an engine that produces power
class Generator(Engine):
    def __init__(self, vars_here):
        super().__init__(vars_here)

    def get_output(self):
        return 0


# To make things simple we will only simulate one engine and one generator
class Ship:
    ship_name = "Undefined"
    # Fuel vars
    ship_fuel_capacity = 0
    ship_fuel_level = 0
    # Engine vars
    ship_engine_runtime = 0
    ship_engine_rpm = 0
    ship_engine_fuel_consumption = 0
    ship_engine_temp = 0
    # ship_engine_oil_temp = 0 - NOT SURE IF NEEDED FOR NOW
    # Generator vars
    ship_generator_output = 0
    ship_generator_fuel_consumption = 0
    ship_generator_temp = 0
    # Navigation vars
    ship_spead = 0
    ship_heading = 0
    ship_lat = 0
    ship_long = 0

    # simulation settings
    simulation_speed = 0.1 # this would mean that 1 second is equal to 10 turns
    operation_transition_time = 100 # 50 = 5 seconds
    simulation_time = 0

    ship_operations = {}

    def load_config(self, config_file):
        # TODO: set ship values from the config file
        pass

    def simulate(self):
        in_transition = False
        transition_turn = 0


if __name__ == "__main__":
    count = 0
    rpm_list = []
    fuel_consumption = []

    base_rpm = 100
    base_fuel_con = 250
    while count < 100000:
        if count > 500:
            base_rpm = 50
            base_fuel_con = 125

        rpm = base_rpm + (random.randrange(120, 150)*(math.sin((math.radians(count)/2))/20)
                     + random.randrange(220, 250)*(math.sin((math.radians(count)/3))/40)
                     + random.randrange(100, 120)*(math.sin((math.radians(count)/5))/30)
                     )
        rpm_list.append(rpm)
        fuel_consumption.append(base_fuel_con + (
                random.randrange(60, 70)*(((
                                            math.sin((math.radians(count)/3)))
                                           +(math.sin((math.radians(count)/6)))
                                           +(-math.sin((math.radians(count/2*math.pi)/3))))/20)))
        count += 1
    plt.plot(rpm_list, label="RPM")
    plt.plot(fuel_consumption, label="Fuel")
    plt.show()

# TODO: create seperate classes for engine and generator

class Simulation:
    pass
