#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 14:31:45 2019

@author: carolinebevalot
"""
import expyriment
import random
import glob
import numpy as np
import simpleaudio as sa

BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
BLACK = (0, 0, 0)
pos_bar=(0,-100) # bar for confidence rating

def define_tones(A_high, A_80_high, A_low, A_80_low, 
                 opposite = False, unpredictive = False):
    """ Function which defines tones corresponding to the category. 
    It returns a list of tones for houses and a list for faces that contains, 
    in 2 tupples, tones as arrays and their name (tone, tone_name).
    By defaults, opposite = False and unpredictive = False, which means that
    houses are associated to high tones and faces to low tones.
    If opposite = True, high tones will predict faces and low tones houses.
    If unpredictive = True, tones are unpredictives."""
    
    if opposite == False : #zip the name to the array 
        houses_tones = [(A_80_high, 'A_80_high'),(A_high, 'A_high')]   
        faces_tones = [(A_80_low, 'A_80_low'),(A_low, 'A_low')]
        return houses_tones, faces_tones
    elif opposite == True : #zip the name to the array 
        faces_tones = [(A_80_high, 'A_80_high'),(A_high, 'A_high')]
        houses_tones = [(A_80_low, 'A_80_low'),(A_low, 'A_low')]
        return houses_tones, faces_tones

    if unpredictive == True :
        houses_tones += faces_tones
        faces_tones += houses_tones
        return houses_tones, faces_tones

def associate_morph_tone(exp, trial, houses_tones, faces_tones, time_waiting):
    """Function which plays, for a trial of the experiment, the adequate tone 
       before presenting morph. 
       For one trial, the function detects if the morph is a house or a face, 
       associate a random pur or 80% tone taken in houses_tones or faces_tones 
       lists and plays it.
       It returns morph type as image_noise and the tone played as tone_name."""
       
    sample_rate = 44100# 44100 samples per second 

    expyriment.stimuli.BlankScreen(colour=BLACK).present()  # clear screen
    exp.clock.wait(time_waiting)
    image_noise = trial.get_factor('name')[-10:] #get noise of the morph   
        
    if image_noise == 'noise1.jpg' or image_noise == 'noise2.jpg' : 
        #the morph is a face, so we play randomly a low or 80% low tone
        tone, tone_name = random.choice(faces_tones)
        #unzip to save the name picked
        play_tone = sa.play_buffer(tone, 1, 2, sample_rate)
        play_tone.wait_done()
        exp.clock.wait(time_waiting)

    elif image_noise == 'noise4.jpg' or  image_noise == 'noise5.jpg': 
        #the morph is a house, so we play randomly a high or 80% high tone
        tone, tone_name = random.choice(houses_tones)
        #unzip to save the name picked
        play_tone = sa.play_buffer(tone, 1, 2, sample_rate)
        play_tone.wait_done() 
        exp.clock.wait(time_waiting)

    return image_noise, tone_name

def select_response(exp, time_waiting, response_window, face_right, house_left):
    """Function which presents the response window, wait for the right or left 
    answer and return them with the corresponding response time. """
    response_window.present() #response screen
    #Wait for an answer and highlight the answer
    key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                         expyriment.misc.constants.K_RIGHT])
    if key == 275 :#key of pressing right button
        face_right.present()
        exp.clock.wait(time_waiting)
    elif key == 276:#key of pressing leftt button
        house_left.present()
        exp.clock.wait(time_waiting) 
    return key, rt 

def rate_confidence(exp, time_waiting, pos = pos_bar, slider_var = 40, bar_length = 300, 
                    bar_thick = 5):
    """Function which presents a scale to rate confidence 
    and saves the confidence rate between ± bar_lenght/2.
    By default, the slider variation will be of 20, its initial position 
    is at the middle of the bar. 
    The bar is 300 long and 5 thick."""

    right_end = bar_length/2
    left_end = - bar_length/2
    question = expyriment.stimuli.TextLine("Êtes-vous sûr(e)?", 
                           position = (pos_bar[0],pos_bar[1]+30), text_size=16)
    no = expyriment.stimuli.TextLine("Pas du tout",
                           position = (left_end, pos_bar[1]-20), text_size =14)
    yes = expyriment.stimuli.TextLine("Complètement",
                           position = (right_end, pos_bar[1]-20), text_size=14)
    bar = expyriment.stimuli.Rectangle((bar_length,bar_thick), 
                                               colour = GRAY, position=pos_bar)
    bar.preload()
    
    commit = 0
    while commit==0:
        # create a canvas object to show multiple elements at the same time
        scale = expyriment.stimuli.BlankScreen()
        bar.plot(scale)
        no.plot(scale)
        yes.plot(scale)
        question.plot(scale)
        slider = expyriment.stimuli.Rectangle((3,30),position=pos, colour = BLUE)
        slider.plot(scale)
        scale.present()
        # participants can use left and right buttons to adjust slider position
        # and commit with enter
        key, rt = exp.keyboard.wait(process_control_events=True)
        if key == 13: #enter 
            commit = 1
            expyriment.stimuli.BlankScreen(colour=BLACK).present()  # black screen
            exp.clock.wait(time_waiting)
            return pos[0]
        elif key == 275:# right button
            pos = (pos[0]+slider_var, pos[1])
            if pos[0] > right_end : # fixes upper end of the scale
                pos = (right_end, pos[1])
        elif key == 276:# left button
            pos = (pos[0]-slider_var, pos[1])
            if pos[0] < left_end : # fixes lower end of the scale
                pos = (left_end,pos[1])

                


def random_pictures (prop_houses, prop_faces, nb_of_trials, path,
                                              prop_levels = 0.50):
    """ Function which create a list of file names according to the proportion 
    of houses and faces in the blocks """
    nb_houses = int(prop_houses * prop_levels * nb_of_trials)
    houses = random.choices(glob.glob (path + '/Morphes/*noise4.jpg'), k=nb_houses) + \
             random.choices(glob.glob (path + '/Morphes/*noise5.jpg'), k=nb_houses) 
    nb_faces = int(prop_faces * prop_levels * nb_of_trials)
    faces = random.choices(glob.glob (path + '/Morphes/*noise1.jpg'), k=nb_faces)+ \
            random.choices(glob.glob (path + '/Morphes/*noise2.jpg'), k=nb_faces)     
    return houses, faces            

def create_note(frequency):
    """ Function which takes a frequency as argument and return a note 
    lasting 1 second (audio)
    To play the note and wait for the end :
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()
    """
    sample_rate = 44100  # 44100 samples per second
    seconds = 0.1  # Note duration of 1 second
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * sample_rate, False)
    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)
    return audio

    
def play_notes(A_low, A_80_low, A_high, A_80_high, sample_rate = 44100):
    """ Function which plays the 4 tones"""
    play_A_low = sa.play_buffer(A_low, 1, 2, sample_rate)
    play_A_low.wait_done()
    play_A_80_low = sa.play_buffer(A_80_low, 1, 2, sample_rate)
    play_A_80_low.wait_done()
  #  play_A_medium = sa.play_buffer(A_medium, 1, 2, sample_rate)
  #  play_A_medium.wait_done()
    play_A_80_high = sa.play_buffer(A_80_high, 1, 2, sample_rate)
    play_A_80_high.wait_done()
    play_A_high = sa.play_buffer(A_high, 1, 2, sample_rate)
    play_A_high.wait_done()
    