import matplotlib.pyplot as plt
import samplerate
import soundfile as sf


filename = input("Enter the name of the wav file (ex: filename.wav -> filename) > ")
soundfile = filename + '.wav'
desired_sample_rate = int(input("Enter the desired sample rate > "))
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

m68code = "/*    File "+soundfile+ "\r\n *    Sample rate "+str(int(desired_sample_rate)) +" Hz\r\n */\r\n"
m68code += "int " + filename + "_samplerate = " + str(int(desired_sample_rate)) + ";\r\n"
m68code += "unsigned int " + filename + "_raw_len = " + str(len(data_out)) + "; \r\n\r\n"
m68code += "const unsigned char " + filename + "_raw[] = {\r\n    "
maxitemsperline = 16
itemsonline = maxitemsperline
firstvalue = 0
lastvalue = 0
for v in data_out:
    # scale v to between 0 and 1
    isin = (v-minValue)/vrange   
    v =  int((isin * 255))
    vstr = str(hex(v))
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

with open(filename + '.h', 'wb') as file:
    file.write(m68code.encode('utf-8'))

# plot wav file
plt.plot(data_out)
#plt.xlabel('time')
#plt.ylabel('amplitude')
plt.title(soundfile)
plt.show()