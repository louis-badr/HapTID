import matplotlib.pyplot as plt
import samplerate
import soundfile as sf


filename = input("Enter the name of the wav file (ex: filename.wav -> filename) > ")
soundfile = filename + '.wav'
desired_sample_rate = int(input("Enter the desired sample rate > "))
pwm_resolution = int(input("Enter the desired bit depth (between 8 and 11) > "))
output_filename = input("Enter the name of the output file (default is 'audiofile') > ")
if (output_filename == ''):
    output_filename = 'audiofile'
data_in, datasamplerate = sf.read(soundfile)
# This means stereo so extract one channel 0
if len(data_in.shape)>1:
    data_in = data_in[:,0]

converter = 'sinc_best'  # or 'sinc_fastest', ...
ratio = desired_sample_rate/datasamplerate
data_out = samplerate.resample(data_in, ratio, converter)
#print(data_out)
maxValue = max(data_out)
minValue = min(data_out)
#print("length", len(data_out))
#print("max value", max(data_out))
#print("min value", min(data_out))
vrange = (maxValue - minValue) 
#print("value range", vrange)

m68code = "//    File "+soundfile+ "\r\n\r\n"
m68code += "int " + output_filename + "_pwm_res = " + str(pwm_resolution) + ";\r\n"
m68code += "int " + output_filename + "_samplerate = " + str(int(desired_sample_rate)) + ";\r\n"
m68code += "unsigned int " + output_filename + "_raw_len = " + str(len(data_out)) + "; \r\n\r\n"
m68code += "const unsigned char " + output_filename + "_raw[] = {\r\n    "
maxitemsperline = 16
itemsonline = maxitemsperline
firstvalue = 0
lastvalue = 0
data_plot_y = []
for v in data_out:
    # scale v to between 0 and 1
    isin = (v-minValue)/vrange   
    #v =  int((isin * 255))
    v = int(isin * (2**pwm_resolution-1))
    vstr = str(hex(v))
    data_plot_y.append(v)
    if (firstvalue==0):
        firstvalue= v
    lastvalue = v
    m68code+=vstr
    itemsonline-=1
    if (itemsonline>0):
        m68code+=','
    else:
        itemsonline = maxitemsperline
        m68code+=',\r\n    '
        
# keep track of first and last values to avoid
# blip when the loop restarts.. make the end value
# the average of the first and last. 
end_value = int( (firstvalue + lastvalue) / 2)
m68code+=str(hex(end_value))+'    \r\n};'
#print(m68code)

with open(output_filename + '.h', 'wb') as file:
    file.write(m68code.encode('utf-8'))

# plot wav file
data_plot_x = range(len(data_plot_y))
# divide by sample rate to get time in seconds
data_plot_x = [x / desired_sample_rate for x in data_plot_x]
plt.step(data_plot_x, data_plot_y)
plt.xlabel('time (s)')
plt.ylabel('PWM value')
plt.title(soundfile)
plt.show()