import os
import time
from datetime import datetime
import RPi.GPIO as GPIO
import picamera

DATA_PATH = "/data"

CAMERA_CAPTURE_PERIOD = 3 # in seconds
WAIT_PERIOD = 60 # in seconds

START_HOUR = 21
END_HOUR = 8

PIN_LED_INFO = 18

def clean_up():
    for root, dirs, files in os.walk(DATA_PATH, topdown=False):
        if len(dirs) >= 3:
            print("Cleaning up old images")
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

def start_camera():
    print("Starting camera")
    with picamera.PiCamera() as camera:
        camera.resolution=(1280, 720),
        camera.led = False

        for filename in camera.capture_continuous(DATA_PATH + "/{timestamp:%Y-%m-%d}/{timestamp:%H-%M-%s}.jpg"):
            print("Captured %s" % filename)

            GPIO.output(PIN_LED_INFO, GPIO.HIGH)

            time.sleep(CAMERA_CAPTURE_PERIOD / 2)

            GPIO.output(PIN_LED_INFO, GPIO.LOW)

            time.sleep(CAMERA_CAPTURE_PERIOD / 2)

            # continue until end time
            now = datetime.today()
            if now.hour < START_HOUR and now.hour >= END_HOUR:
                print("Camera stopped")
                wait()
                return

def wait():
    GPIO.output(PIN_LED_INFO, GPIO.HIGH)

    # wait until start time
    while datetime.today().hour < START_HOUR and datetime.today().hour >= END_HOUR:
        time.sleep(WAIT_PERIOD)

    clean_up()
    start_camera()

def main():
    # setup leds
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_LED_INFO, GPIO.OUT)

    wait()

if __name__ == "__main__":
    main()
