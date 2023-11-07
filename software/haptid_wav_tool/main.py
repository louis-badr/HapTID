import matplotlib.pyplot as plt
import numpy as np
import os
import resampy
import scipy.io.wavfile as wav
import sys
import wave

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

def read_wav_header(file_path):
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
    print("1. resample .WAV file")
    print("2. convert .WAV file to .h")
    print("3. read header and plot .WAV file")
    input_num = input(">> ")
    match input_num:
        case "1":
            print('\nType the path of the .WAV file you want to resample (ex: ./test.wav):')
            input_file = input('>> ')
            print('Type the new sample rate value (ex: 8000):')
            target_sr = input('>> ')
            target_sr = int(target_sr)
            print('Type the path of the new .WAV file (ex: ./test.wav):')
            output_file = input('>> ')
            resample_wav(input_file, target_sr, output_file)
        case "2":
            print('\nType the path of the .WAV file you want to convert (ex: ./test.wav):')
            input_file = input('>> ')
            print('Type the path of the output .h file (ex: ./test.h):')
            output_file = input('>> ')
            wav_to_c_array(input_file, output_file)
        case "3":
            print('\nType the path of the .WAV file you want to read the header of (ex: ./test.wav):')
            file_path = input('>> ')
            read_wav_header(file_path)
        case _:
            print("Invalid input")