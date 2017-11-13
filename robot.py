import os
import time
from datetime import datetime
import picamera

DATA_PATH = "/data"

CAMERA_CAPTURE_PERIOD = 5 # in seconds
WAIT_PERIOD = 60 # in seconds

START_HOUR = 23
END_HOUR = 7

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
        camera.resolution = (1400, 1000)

        # create folder
        os.system("mkdir " + DATA_PATH + "/`date +%Y-%m-%d`")

        for filename in camera.capture_continuous(DATA_PATH + "/{timestamp:%Y-%m-%d}/{timestamp:%H-%M-%S}.jpg"):
            print("Captured %s" % filename)

            time.sleep(CAMERA_CAPTURE_PERIOD)

            # continue until end time
            now = datetime.today()
            if now.hour < START_HOUR and now.hour >= END_HOUR:
                camera.close()
                print("Camera stopped")
                wait()
                return

def wait():
    print("Waiting until start time...")

    # wait until start time
    while datetime.today().hour < START_HOUR and datetime.today().hour >= END_HOUR:
        time.sleep(WAIT_PERIOD)

    clean_up()
    start_camera()

def main():
    wait()

if __name__ == "__main__":
    main()
