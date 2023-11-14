import matplotlib.pyplot as plt
import numpy as np
import os
import resampy
import scipy.io.wavfile as wav
import sys
import wave

def read_h_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

            # Assuming the array is defined as unsigned char array[] = {...};
            start_marker = 'const unsigned char wav_data[] = {'
            end_marker = '};'

            start_index = content.find(start_marker)
            end_index = content.find(end_marker)

            if start_index != -1 and end_index != -1:
                array_content = content[start_index + len(start_marker):end_index]
                array_content = array_content.strip()  # Remove leading and trailing spaces
                array_elements = array_content.split(',')

                # Convert array elements to integers (assuming hexadecimal format)
                array_data = [int(element.strip(), 16) for element in array_elements]

                # Print the array
                print("Extracted Array:", array_data)
                plt.plot(array_data)
                plt.title(file_path)
                plt.show()
            else:
                print("Array not found in the file.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")

def resample_wav(input_file, target_sr, output_file):
    try:
        # Read the input WAV file
        original_sr, data = wav.read(input_file)
        # Check if the input WAV file is already at the target sample rate
        if original_sr == target_sr:
            print("The input WAV file is already at the target sample rate.")
            return
        # Perform the resampling
        resampled_data = resampy.resample(data, original_sr, target_sr, axis=0)
        # Ensure the data type is the same as the original
        resampled_data = resampled_data.astype(data.dtype)
        # Save the resampled data to the output WAV file
        wav.write(output_file, target_sr, resampled_data)
        print(f"Resampled WAV file saved as {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def wav_to_c_array(input_file, output_file):
    try:
        # Read the .wav file content
        with open(input_file, "rb") as f:
            data = f.read()
        # Convert the data to a C array
        c_array = ', '.join(['0x{:02x}'.format(byte) for byte in data])
        # Prepare the C code
        c_code = '// Filename: {}\n\nconst unsigned char {}[] = {{\n    {}\n}};\nunsigned int {}_len = {};'.format(input_file, "wav_data", c_array, "wav_data", len(data))
        # Write the C code to the output file
        with open(output_file, "w") as f:
            f.write(c_code)
        print("Conversion successful! C code written to", output_file)
    except Exception as e:
        print("An error occurred:", str(e))

def read_wav_file(file_path):
    try:
        with wave.open(file_path, 'rb') as wf:
            print("WAV File Header Information:")
            print(f"File Name: {file_path}")
            print(f"Number of Channels: {wf.getnchannels()}")
            print(f"Bit Depth (bits per sample): {wf.getsampwidth() * 8}")
            print(f"Compression Type: {wf.getcompname()}")
            duration = wf.getnframes() / wf.getframerate()
            print(f"Duration (seconds): {duration}")
            sample_rate, audio_buffer = wav.read(file_path)
            print(f"Sample Rate: {sample_rate}")
            time = np.arange(0, duration, 1.0 / wf.getframerate())
        plt.plot(time, audio_buffer)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title(file_path)
        plt.show()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("\nPlease type the number of the function you want to use:")
    print("1. get .wav file header information and plot the audio signal")
    print("2. get .h file header information and plot the audio signal")
    print("3. resample a .wav file")
    print("2. convert a .wav file into a .h file")
    
    input_num = input(">> ")
    match input_num:
        case "1":
            print('\nEnter the path of the .wav file (ex: ./test.wav):')
            file_path = input('>> ')
            read_wav_file(file_path)
        case "2":
            print('\nEnter the path of the .h file (ex: ./test.wav):')
            file_path = input('>> ')
            read_h_file(file_path)
        case "3":
            print('\nEnter the path of the .wav file (ex: ./input.wav):')
            input_file = input('>> ')
            print('Type the new sample rate value (ex: 8000):')
            target_sr = input('>> ')
            target_sr = int(target_sr)
            print('Enter the path for the new .wav file (ex: ./output.wav):')
            output_file = input('>> ')
            resample_wav(input_file, target_sr, output_file)
        case "4":
            print('\nEnter the path of the .wav file (ex: ./input.wav):')
            input_file = input('>> ')
            print('Enter the path of the new .h file (ex: ./output.h):')
            output_file = input('>> ')
            wav_to_c_array(input_file, output_file)
        case _:
            print("Invalid input")