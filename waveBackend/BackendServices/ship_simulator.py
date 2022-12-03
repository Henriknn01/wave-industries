import math
import random
import time
from math import sin
from os.path import exists
import json
import paho.mqtt.client as paho


class Mode:
    """
    The mode class contains information about the mode, such as base_rpm etc.
    This is then used in other methods to calculate other values.
    """
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
        """
        Sets the engine mode to the specified mode.
        :param mode: Mode to use
        """
        self.mode = mode

    def get_rpm(self):
        # Used as base numbers for the amplifications of the sinus waves
        """
        Gets the engines current rpm.
        Multiple sinus waves are added together to simulate realistic changes to the engine rpm.
        Once we have the sinus waves combined we add it to the current engine mode's base rpm.

        :return: Engine rpm
        """
        b_rpm = self.mode.base_rpm if self.mode is not None else 0
        wave_1_base = b_rpm
        wave_2_base = (b_rpm + (round(b_rpm * 0.6)))
        wave_3_base = (b_rpm + (round(b_rpm * 0.35)))

        # used for the sinus waves
        degrees = math.radians(self.simulation_turn)

        # create a combination of 3 sinus waves to make the rpm's go up and down at seemingly random times
        wave = (
                random.randrange(wave_1_base, round(wave_1_base*1.20+1))*(math.sin((degrees/2))/20)
                + random.randrange(wave_2_base, round(wave_2_base*1.25+1))*(math.sin((degrees/3))/40)
                + random.randrange(wave_3_base, round(wave_3_base*1.15+1))*(math.sin((degrees/5))/30)
        )
        return b_rpm + wave

    def get_fuel_consumption(self):
        """
        Gets the current fuel consumption for the engine in liters per hour.
        The method combines multiple sinus waves together and then adds the base fuel consumption to this wave.
        a random number between 5 and 7 is selected as the wave amplification, this is done to simulate noise from the sensor.

        :return: Current fuel consumption in liters per hour
        """
        # used for the sinus waves
        degrees = math.radians(self.simulation_turn)

        # create a combination of 3 sinus waves to make the fuel consumption to go up and down
        wave = random.randrange(5, 7)*((math.sin((degrees / 3)))
                + (math.sin((degrees / 6)))
                + (-math.sin(((degrees / 2) * math.pi) / 3))
        )
        return self.mode.base_fuel_consumption + wave

    def get_temperature(self):
        """
        Gets the current engine temperature in celsius.
        :return: Current engine temperature in celsius
        """
        return self.mode.base_temperature + (self.mode.base_temperature*0.2)*math.sin(math.radians(self.simulation_turn+50)/2)

    def get_energy_output(self):
        """
        Gets the current engine energy output in kWh.
        :return: current engine energy output in kWh
        """
        return self.mode.base_energy_output + (self.mode.base_temperature*0.2)*(math.sin(math.radians(self.simulation_turn+50)/2)
                                                                    * math.sin(math.radians(self.simulation_turn+32)/3))

    def get_name(self):
        """
        Gets the engine name.
        :return: engine name
        """
        return self.name

    def next_turn(self):
        """
        Increases the simulation turn by one.
        """
        self.simulation_turn += 1


# To make things simple we will only simulate one engine and one generator
class Ship:
    """
    Ship class

    This is the main class of the simulator.
    """
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
    simulation_speed = 1  # 0.1 would mean that 1 second is equal to 10 turns, and 1 = 1 update per second
    simulation_turns = 0
    running = False
    modes = []
    mode = None

    # mqtt settings
    broker = "test.mosquitto.org"  # "79.160.34.197"  # CHANGE: change this to your MQTT broker
    port = 1883

    def on_publish(client, userdata, result):  # create function for callback
        # print("data published \n")
        pass
    mqttclient = paho.Client("ship_client")  # create client object
    mqttclient.on_publish = on_publish  # assign function to callback

    def load_config(self, config_file):
        """
        Loads ship variables from the specified config file, see ship_config.json file for example config.

        :param config_file: json config file
        """
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
            e = Engine(engine['name'], simulation_turn=random.randrange(0, 1000))
            self.ship_engine = e
        for generator in data['generators']:
            g = Engine(generator['name'], simulation_turn=random.randrange(0, 10000))
            self.ship_generators.append(g)

    def set_mode(self, mode: Mode):
        """
        Sets the ship mode to specified mode of type Mode.
        :param mode: Mode object
        """
        self.mode = mode
        self.ship_engine.set_mode(mode)
        for g in self.ship_generators:
            g.set_mode(mode)

    def get_mode(self):
        """
        Gets the current ship mode.

        :return: current ship mode
        """
        return self.mode

    def get_speed(self):
        """
        Returns the vessels speed in knots.

        :return: vessel speed
        """
        base_speed = self.mode.mode_base_speed
        speed = base_speed + random.randrange(4, 9)*math.sin(math.radians(self.simulation_turns)/55)
        return speed

    def start_simulation(self):
        """
        Main simulation method. This is responsible for updating variables and publishing mqtt messages to the broker.
        """
        self.running = True
        self.set_mode(self.modes[0])
        self.mqttclient.connect(self.broker, self.port)

        next_mode_switch = random.randrange(500, 1000)

        while self.running:
            total_fuel_consumption = 0
            if self.simulation_turns == next_mode_switch:
                rand_num = random.randrange(0, len(self.modes))
                rand_mode = self.modes[rand_num]
                print(f"Mode switch: {self.mode.name} -> {rand_mode.name}")
                self.set_mode(rand_mode)
                next_mode_switch = random.randrange(500, 1000) + self.simulation_turns

            data = {
                'engine_rpm': self.ship_engine.get_rpm(),
                'engine_output': self.ship_engine.get_energy_output(),
                'engine_temperature': self.ship_engine.get_temperature(),
                'engine_fuel_consumption': self.ship_engine.get_fuel_consumption(),
                'generators': [],
                'total_fuel_consumption': 0,
                'fuel_level': self.ship_fuel_level,
                'fuel_capacity': self.ship_fuel_capacity,
                'speed': self.get_speed(),
            }
            total_fuel_consumption += self.ship_engine.get_fuel_consumption()
            self.ship_engine.next_turn()
            for g in self.ship_generators:
                generator_data = {
                    'generator_name': g.get_name().replace(" ", "_").lower(),
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

            # ship data
            self.mqttclient.publish(f"/{self.ship_name}/total_fuel_consumption", round(data["total_fuel_consumption"], 4), qos=2)
            self.mqttclient.publish(f"/{self.ship_name}/fuel_level", round(data["fuel_level"], 4), qos=2)
            self.mqttclient.publish(f"/{self.ship_name}/fuel_capacity", round(data["fuel_capacity"], 4), qos=2)
            self.mqttclient.publish(f"/{self.ship_name}/speed", round(data["speed"], 2), qos=2)

            # engine data
            self.mqttclient.publish(f"/{self.ship_name}/engine/engine_rpm", round(data["engine_rpm"], 4), qos=2)
            self.mqttclient.publish(f"/{self.ship_name}/engine/engine_output", round(data["engine_output"], 4), qos=2)
            self.mqttclient.publish(f"/{self.ship_name}/engine/engine_temperature", round(data["engine_temperature"], 2), qos=2)
            self.mqttclient.publish(f"/{self.ship_name}/engine/engine_fuel_consumption", round(data["engine_fuel_consumption"], 4), qos=2)

            # generator data
            for g in data["generators"]:
                self.mqttclient.publish(f"/{self.ship_name}/generators/{g['generator_name']}/engine_rpm", round(g['generator_rpm'], 4), qos=2)
                self.mqttclient.publish(f"/{self.ship_name}/generators/{g['generator_name']}/engine_output", round(g['generator_output'], 4), qos=2)
                self.mqttclient.publish(f"/{self.ship_name}/generators/{g['generator_name']}/engine_temperature", round(g['generator_temperature'], 2), qos=2)
                self.mqttclient.publish(f"/{self.ship_name}/generators/{g['generator_name']}/engine_fuel_consumption", round(g['generator_fuel_consumption'], 4), qos=2)

    def stop_simulation(self):
        """
        Stops the simulation.
        """
        self.running = False


if __name__ == "__main__":
    ship = Ship()
    ship.load_config("ship_config.json")
    ship.start_simulation()
