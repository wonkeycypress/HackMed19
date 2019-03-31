#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:44:57 2019

@author: harrycooper
"""
#Measure pitch of all wav files in directory
import glob
import numpy as np
import pandas as pd
import parselmouth
import urllib.request

from parselmouth.praat import call
from ml2 import classify
from ml2 import sendSMS

urllib.request.urlretrieve('https://parkinsons.nodered.nexmodev.com/audio', './Sounds/audio.mp3')

# This is the function to measure voice pitch
def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    # Pitch
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    median_pitch = call(pitch, "Get quantile", 0.0, 0.0, 0.5, unit)
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    # Jitter
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)*100
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    # Shimmer
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    # Pulses
    num_pulses = parselmouth.praat.call(pointProcess, "Get number of points")
    num_period = parselmouth.praat.call(pointProcess, "Get number of periods", 0.0, 0.0, 0.0001, 0.02, 1.3)
    
#    print(num_pulses)
#    print(num_period)
#    print(median_pitch)

    return meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer, num_pulses, num_period, median_pitch

# create lists to put the results
file_list = []
mean_F0_list = []
sd_F0_list = []
hnr_list = []
localJitter_list = []
localabsoluteJitter_list = []
rapJitter_list = []
ppq5Jitter_list = []
ddpJitter_list = []
localShimmer_list = []
localdbShimmer_list = []
apq3Shimmer_list = []
aqpq5Shimmer_list = []
apq11Shimmer_list = []
ddaShimmer_list = []
num_pulses_list = []
num_period_list = []
median_pitch_list = []

# Go through all the wave files in the folder and measure pitch
for wave_file in glob.glob("Sounds/*.mp3"):
    sound = parselmouth.Sound(wave_file)
    (meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer, num_pulses, num_period, median_pitch) = measurePitch(sound, 75, 500, "Hertz")
    
    localJitter_list.append(localJitter)
    localabsoluteJitter_list.append(localabsoluteJitter)
    rapJitter_list.append(rapJitter)
    ppq5Jitter_list.append(ppq5Jitter)
    localShimmer_list.append(localShimmer)
    localdbShimmer_list.append(localdbShimmer)
    apq3Shimmer_list.append(apq3Shimmer)
    apq11Shimmer_list.append(apq11Shimmer)
    ddaShimmer_list.append(ddaShimmer)
    median_pitch_list.append(median_pitch)
    mean_F0_list.append(meanF0) # make a mean F0 list
    sd_F0_list.append(stdevF0) # make a sd F0 list
    num_pulses_list.append(num_pulses)
    num_period_list.append(num_period)
    
    file_list.append(wave_file) # make an ID list    
    hnr_list.append(hnr)
    ddpJitter_list.append(ddpJitter)
    aqpq5Shimmer_list.append(aqpq5Shimmer) 
    
#    print(wave_file)
    
df = pd.DataFrame(np.column_stack([localJitter_list, localabsoluteJitter_list, 
                                   rapJitter_list, ppq5Jitter_list, ddpJitter_list, 
                                   localShimmer_list, localdbShimmer_list, 
                                   apq3Shimmer_list, aqpq5Shimmer_list, apq11Shimmer_list, 
                                   ddaShimmer_list, median_pitch_list, 
                                   mean_F0_list, sd_F0_list, num_pulses_list, 
                                   num_period_list]),
                               columns=['Jitter (local)', 'Jitter (local, absolute)', 
                                        'Jitter (rap)', 'Jitter (ppq5)', 'Jitter (ddp)',  
                                        'Shimmer (local)', 'Shimmer (local, dB)', 
                                        'Shimmer (apq3)', 'Shimmer (apq5)', 'Shimmer (apq11)', 
                                        'Shimmer (dda)', 'Median Pitch', 'Mean Pitch', 
                                        'Standard Deviation', 'Number of pulses', 
                                        'Number of periods'])  #add these lists to pandas in the right order

# Write out the updated dataframe
df.to_csv("processed_results.csv", index=False)

# Classify phone call
prob, res = classify("./processed_results.csv")

# Send results to doctor
sendSMS(prob,res)
