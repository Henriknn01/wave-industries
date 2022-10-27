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
    def __init__(self, engine_name, signal_noise: int = 1, simulation_turn: int = 0):
        self.name = engine_name
        self.signal_noise = signal_noise
        self.rpm = 0
        self.temperature = 0
        self.fuel_consumption = 0
        # Set base values
        self.base_rpm = 0
        self.base_fuel_consumption = 0
        self.base_temperature = 0
        self.simulation_turn = simulation_turn
        self.mode = ""

    def set_mode(self, mode_base_rpm, mode_base_fuel_consumption, mode_base_temperature, mode_name):
        self.base_rpm = mode_base_rpm
        self.base_fuel_consumption = mode_base_fuel_consumption
        self.base_temperature = mode_base_temperature
        self.mode = mode_name

    def get_rpm(self):
        # Used as base numbers for the amplifications of the sinus waves
        wave_1_base = self.base_rpm
        wave_2_base = (self.base_rpm + (round(self.base_rpm * 0.6)))
        wave_3_base = (self.base_rpm + (round(self.base_rpm * 0.35)))

        # used for the sinus waves
        degrees = math.radians(self.simulation_turn)

        # create a combination of 3 sinus waves to make the rpm's go up and down at seemingly random times
        wave = (
                random.randrange(wave_1_base, round(wave_1_base*1.20))*(math.sin((degrees/2))/20)
                + random.randrange(wave_2_base, round(wave_2_base*1.25))*(math.sin((degrees/3))/40)
                + random.randrange(wave_3_base, round(wave_3_base*1.15))*(math.sin((degrees/5))/30)
        )
        return self.base_rpm + wave

    def get_fuel_consumption(self):
        # Used as base numbers for the amplifications of the sinus waves
        wave_1_base = self.base_rpm

        # used for the sinus waves
        degrees = math.radians(self.simulation_turn)

        # create a combination of 3 sinus waves to make the fuel consumption to go up and down
        wave = ((math.sin((degrees / 3)))
                + (math.sin((degrees / 6)))
                + (-math.sin(((degrees / 2) * math.pi) / 3))
        )
        return (self.base_fuel_consumption + wave)/20

    def get_temperature(self):
        return self.base_temperature



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
    engine_1 = Engine()
class Simulation:
    pass
