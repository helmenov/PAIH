# coding: utf-8

import paih
#from matplotlib import pyplt as plt 
import soundfile as sf 
from IPython.display import display,Audio 
import time

message = "Hello, world!"
bps = 10
SecDuration = 10
FreqSampling = 44100
wavname = str(time.strftime("%Y%m%d%H%M%S"))+".wav"

steg,Code_frame = paih.genPAIHv0(message,SecDuration)

sf.write(wavname,steg,FreqSampling)
Audio(wavname)


