import math
import random
import time
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
class Mode:
    base_rpm = 0
    base_fuel_consumption = 0
    base_temperature = 0
    base_energy_output = 0
    mode_base_speed = 0
    name = "unknown"
    def __init__(self, mode_base_rpm, mode_base_fuel_consumption, mode_base_temperature, mode_name,
                 mode_base_energy_output, mode_base_speed):
        self.base_rpm = mode_base_rpm
        self.base_fuel_consumption = mode_base_fuel_consumption
        self.base_temperature = mode_base_temperature
        self.base_energy_output = mode_base_energy_output
        self.mode_base_speed = mode_base_speed
        self.name = mode_name


class Engine:
    def __init__(self, engine_name, signal_noise: int = 1, simulation_turn: int = 0):
        self.name = engine_name
        self.signal_noise = signal_noise
        self.rpm = 0
        self.temperature = 0
        self.fuel_consumption = 0
        # Set base values

        self.simulation_turn = simulation_turn
        self.mode = None

    def set_mode(self, mode: Mode):
        self.mode = mode

    def get_rpm(self):
        # Used as base numbers for the amplifications of the sinus waves
        b_rpm = self.mode.base_rpm if self.mode is not None else 0
        wave_1_base = b_rpm
        wave_2_base = (b_rpm + (round(b_rpm * 0.6)))
        wave_3_base = (b_rpm + (round(b_rpm * 0.35)))

        # used for the sinus waves
        degrees = math.radians(self.simulation_turn)

        # create a combination of 3 sinus waves to make the rpm's go up and down at seemingly random times
        wave = (
                random.randrange(wave_1_base, round(wave_1_base*1.20))*(math.sin((degrees/2))/20)
                + random.randrange(wave_2_base, round(wave_2_base*1.25))*(math.sin((degrees/3))/40)
                + random.randrange(wave_3_base, round(wave_3_base*1.15))*(math.sin((degrees/5))/30)
        )
        return b_rpm + wave

    def get_fuel_consumption(self):
        # used for the sinus waves
        degrees = math.radians(self.simulation_turn)

        # create a combination of 3 sinus waves to make the fuel consumption to go up and down
        wave = 5*((math.sin((degrees / 3)))
                + (math.sin((degrees / 6)))
                + (-math.sin(((degrees / 2) * math.pi) / 3))
        )
        return self.mode.base_fuel_consumption + wave

    def get_temperature(self):
        return self.mode.base_temperature + (self.mode.base_temperature*0.2)*math.sin(math.radians(self.simulation_turn+50)/2)

    def get_energy_output(self):
        return self.mode.base_energy_output + (self.mode.base_temperature*0.2)*(math.sin(math.radians(self.simulation_turn+50)/2)
                                                                    * math.sin(math.radians(self.simulation_turn+32)/3))

    def next_turn(self):
        self.simulation_turn += 1


# To make things simple we will only simulate one engine and one generator
class Ship:
    ship_name = "Undefined"
    # Fuel vars
    ship_fuel_capacity = 0
    ship_fuel_level = 0
    # Engine vars
    ship_engine = None
    # Generator vars
    ship_generators = []
    # Navigation vars
    ship_spead = 0
    ship_heading = 0
    ship_lat = 0
    ship_long = 0

    # simulation settings
    simulation_speed = 0.1  # this would mean that 1 second is equal to 10 turns
    operation_transition_time = 100  # 50 = 5 seconds
    simulation_turns = 0
    running = False
    modes = []

    def load_config(self, config_file):
        f = open(config_file)
        data = json.load(f)
        self.ship_name = data['name']
        self.ship_fuel_capacity = data['fuel_capacity']
        self.ship_fuel_level = self.ship_fuel_capacity
        for mode in data['modes']:
            m = Mode(
                mode_base_rpm=mode['base_rpm'],
                mode_base_speed=mode['base_speed'],
                mode_base_temperature=mode['base_temperature'],
                mode_base_energy_output=mode['base_energy_output'],
                mode_base_fuel_consumption=mode['base_fuel_consumption'],
                mode_name=mode['name']
            )
            self.modes.append(m)
        for engine in data['engines']:
            e = Engine(engine['name'])
            self.ship_engine = e
        for generator in data['generators']:
            g = Engine(generator['name'])
            self.ship_generators.append(g)

    def set_mode(self, mode: Mode):
        self.ship_engine.set_mode(mode)
        for g in self.ship_generators:
            g.set_mode(mode)

    def start_simulation(self):
        self.running = True
        in_transition = False
        transition_turn = 0
        self.set_mode(self.modes[0])

        while self.running:
            total_fuel_consumption = 0
            data = {
                'engine_rpm': self.ship_engine.get_rpm(),
                'engine_output': self.ship_engine.get_energy_output(),
                'engine_temperature': self.ship_engine.get_temperature(),
                'engine_fuel_consumption': self.ship_engine.get_fuel_consumption(),
                'generators': [],
                'total_fuel_consumption': 0,
                'fuel_level': self.ship_fuel_level,
                'fuel_capacity': self.ship_fuel_capacity,
            }
            total_fuel_consumption += self.ship_engine.get_fuel_consumption()
            self.ship_engine.next_turn()
            for g in self.ship_generators:
                generator_data = {
                    'generator_rpm': g.get_rpm(),
                    'generator_output': g.get_energy_output(),
                    'generator_temperature': g.get_temperature(),
                    'generator_fuel_consumption': g.get_fuel_consumption()
                }
                total_fuel_consumption += g.get_fuel_consumption()
                data['generators'].append(generator_data)
                g.next_turn()

            turn_fuel_consumed = (total_fuel_consumption/60/60)*self.simulation_speed
            data['total_fuel_consumption'] = total_fuel_consumption
            self.ship_fuel_level -= turn_fuel_consumed
            self.simulation_turns += 1
            time.sleep(self.simulation_speed)
            # TEST
            print(data)

    def stop_simulation(self):
        self.running = False


if __name__ == "__main__":
    ship = Ship()
    ship.load_config("ship_config.json")
    ship.start_simulation()
