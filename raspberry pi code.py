import RPi.GPIO as GPIO
import time

# GPIO pin setup (change these pin numbers to match your wiring)
LEFT_MOTOR_FORWARD = 17
LEFT_MOTOR_BACKWARD = 27
RIGHT_MOTOR_FORWARD = 22
RIGHT_MOTOR_BACKWARD = 23

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_MOTOR_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_BACKWARD, GPIO.OUT)

# Motor control functions
def move_forward():
    print("Moving forward")
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.LOW)

def stop():
    print("Stopping")
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.LOW)

def turn_left():
    print("Turning left")
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.LOW)
    time.sleep(0.5)
    stop()  # Stop after the turn

def turn_right():
    print("Turning right")
    GPIO.output(LEFT_MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_BACKWARD, GPIO.HIGH)
    time.sleep(0.5)
    stop()  # Stop after the turn

# Clean up GPIO pins when done
def cleanup():
    GPIO.cleanup()

# Example usage
try:
    move_forward()
    time.sleep(1)
    stop()
    time.sleep(1)
    turn_left()
    time.sleep(1)
    turn_right()
    time.sleep(1)
finally:
    cleanup()
