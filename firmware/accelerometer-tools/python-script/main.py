import matplotlib.pyplot as plt
import serial
from serial.tools import list_ports
import time
import numpy as np

# in progress
def test_latency(freq, vol):
    # start timer
    start_time = time.time()
    str_mcu = str(freq) + str(vol * 1000)
    # send vibration
    ser_haptid.write(str_mcu.encode())
    # wait for the motor to reach the threshold vibration intensity
    # stop timer
    end_time = time.time()
    # calculate latency
    latency = end_time - start_time
    print(latency)

def plot_freq_response(freq_min, freq_max, step_size, vol):
    # step size is a float
    frequency_values = np.arange(freq_min, freq_max, step_size)
    acceleration_values = []
    for freq in frequency_values:
        acceleration = 0
        # test 3 times each frequency and average the results
        for i in range(3):
            str_mcu = str(freq) + str(vol * 1000)
            # start vibration
            ser_haptid.write(str_mcu.encode())
            # wait 3 seconds
            time.sleep(3)
            # measure acceleration
            ser_accelerometer.write(b'4')
            # read result from accelerometer
            result = ser_accelerometer.readline()
            # stop vibration
            ser_haptid.write(b'0')
        # add average acceleration to freq_response
        acceleration_values.append(accel/3)
    print(acceleration_values)
    # generate equalizer coefficients
    eq_coefficients = []
    min_acceleration = min(acceleration_values)
    for accel in acceleration_values:
        eq_coefficients.append(min_acceleration/accel)
    # plot frequency response
    plt.plot(frequency_values, acceleration_values)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Acceleration (g)')
    plt.show()
    # plot equalizer coefficients
    plt.plot(frequency_values, eq_coefficients)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Equalizer coefficient')
    plt.show()
    print(eq_coefficients)

def plot_volume_response(freq, vol_min, vol_max, step_size):
    # wait
    time.sleep(3)
    # start calibration
    ser_accelerometer.write(b'1')
    # wait
    time.sleep(3)
    # step size is a float
    volume_values = np.arange(vol_min, vol_max, step_size)
    acceleration_values = []
    for vol in volume_values:
        acceleration = 0
        # test 3 times each volume and average the results
        for i in range(3):
            str_mcu = str(freq)
            vol_str = str(int(vol * 1000))
            # add 0 before so it is always 5 digits
            vol_str = vol_str.zfill(5)
            str_mcu += vol_str
            print(str_mcu)
            # start vibration
            ser_haptid.write(str_mcu.encode())
            # wait 3 seconds
            time.sleep(3)
            # measure acceleration
            ser_accelerometer.write(b'4')
            # read result from accelerometer
            result = ser_accelerometer.readline()
            print(float(result.decode()))
            # convert output to float
            acceleration += float(result.decode())
            # wait a bit
            time.sleep(3)
            # stop vibration
            ser_haptid.write(b'0')
            # wait
            time.sleep(3)
        # add average acceleration to freq_response
        acceleration_values.append(acceleration/3)
    print(acceleration_values)
    # plot volume response
    plt.plot(volume_values, acceleration_values)
    plt.xlabel('Volume (%)')
    plt.ylabel('Acceleration (g)')
    plt.show()

if __name__ == "__main__":
    # list available serial ports
    ports = list_ports.comports()
    print("\nAvailable COM ports:")
    for port, desc, hwid in sorted(ports):
        print("{}: {}".format(port, desc))
    com_port_haptid = 'COM' + input('\nEnter the HapTID bord COM port n°: ')
    com_port_accelerometer = 'COM' + input('\nEnter the accelerometer MCU COM port n°: ')
    # arduino things
    ser_haptid = serial.Serial(com_port_haptid, 115200, timeout=.1)
    ser_accelerometer = serial.Serial(com_port_accelerometer, 115200, timeout=.1)
    # dirty fix to make sure the arduino is ready to receive data
    ser_haptid.close()
    ser_haptid.open()
    ser_accelerometer.close()
    ser_accelerometer.open()

    print("\nPlease type the number of the function you want to use:")
    print("1. Measure latency")
    print("2. Record accelerometer data")
    print("3. Plot acceleration as a function of a frequency range and generate equalizer coefficients")
    print("4. Plot acceleration as a function of volume for a single frequency")
    input_num = input(">> ")
    match input_num:
        case "1":
            print('\nAt what frequency do you want to test the latency? (ex: 100):')
            freq = input('>> ')
            test_latency(freq)
        case "2":
            print('\nHow long do you want to record data in seconds? (ex: 10):')
            duration = int(input('>> '))
            print('\nWhat frequency do you want to use? (ex: 100):')
            freq = input('>> ')
        case "3":
            print('\nWhat frequency range do you want to test? (ex: 20:500):')
            freq_min, freq_max = [int(x) for x in input('>> ').split(':')]
            print('\nWhat step size do you want to use? (ex: 10):')
            step_size = float(input('>> '))
            plot_freq_response(freq_min, freq_max, step_size)
        case "4":
            print('\nWhat frequency do you want to use? (ex: 100):')
            freq = input('>> ')
            print('\nWhat volume range do you want to test (in %)? (ex: 0:50):')
            vol_min, vol_max = [int(x) for x in input('>> ').split(':')]
            print('\nWhat step size do you want to use? (ex:0.1)')
            step_size = float(input('>> '))
            plot_volume_response(freq, vol_min, vol_max, step_size)
        case _:
            print("Invalid input")