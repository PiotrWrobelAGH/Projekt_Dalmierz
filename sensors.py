import RPi.GPIO as GPIO
import threading
import time


class Sensors:

    def __init__(self):
        self.gpio_trigger = 18
        self.gpio_echo = 24
        self.distance = None
        self.threads = []
        self.prepare_gpio_ports()
        self.start_sensor_agent()

    def start_sensor_agent(self):
        self.threads.append(threading.Thread(target=self.update_distance, args=[]))
        self.threads[-1].daemon = True
        self.threads[-1].start()
        self._wait_for_sensors_measure()

    def update_distance(self):
        while True:
            self._calculate_distance()

    def prepare_gpio_ports(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

    def _get_echo_time_from_hcsr04(self):
        GPIO.output(self.gpio_trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)

        start_time = time.time()
        stop_time = time.time()
        while GPIO.input(self.gpio_echo) == 0:
            start_time = time.time()

        while GPIO.input(self.gpio_echo) == 1:
            stop_time = time.time()

        return stop_time - start_time

    def _calculate_distance(self):
        sound_speed = 331.5
        self.distance = ((sound_speed * 100) * self._get_echo_time_from_hcsr04()) / 2

    def _wait_for_sensors_measure(self):
        measurements_ongoing = True
        timer = 0
        while measurements_ongoing or timer > 20:
            time.sleep(1)


sensor = Sensors()

while True:
    print(sensor.distance)
    time.sleep(1)
