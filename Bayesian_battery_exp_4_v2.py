#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 18:36:09 2019

@author: carolinebevalot
"""
import expyriment
import glob
import random
import numpy as np
import simpleaudio as sa
from Bayesian_battery_functions_v2 import random_pictures, rate_confidence, \
     create_note, play_notes, associate_morph_tone, define_tones

##### Global variables
BLACK = (0, 0, 0)
path = '/Users/carolinebevalot/Desktop/Bayesian_battery'

exp = expyriment.design.Experiment(name="Fourth Experiment")

# Position of pictures in response_window
left_pos = (-150, 0)
right_pos = (150, 0)

# Times
time_prior = 1500 
time_interblocks = 3000
time_waiting = 700
time_morph = 1500
nb_of_trials = 20
#nb of trials should be a multiple of 5 and 2 for the nb of morphs to be an integer

prop_levels = 0.50 # proportion of noise 1,2 or 4,5 

frequency = 220 # frequency of the lowest tone (A)

expyriment.control.initialize(exp) 


##### Functions 

def execute_trial_4(block_nb, shuffle = True, param_1 = False, param_2 = False):
    """Function which runs blocks. For each trial, it presents the tone, 
    the morph and the response window and save the block name, the trial ID 
    and name, the tone name, the response key and response time.
    
    Each part calls define_tones() to set lists of tones for houses and faces, 
    then associate_morph_tone() to choose randomly between a pur or 80% tone, 
    to play it and present the morph. 3 morphs are presented and the response 
    window is presented for the 4th morph with the confidence rate.
    
    The association between tones and morphs is : 
        - high tones predict houses and low tones faces with param_1 being True
        - high tones predict faces and low tones houses with param_2 being True
        - the association is random between these two possibilities by default,
          with shuffle being True"""
          
    param_1 = {'opposite':False, 'unpredictive':False} 
    
    param_2 = {'opposite':True, 'unpredictive':False}
    
    if shuffle == True : 
        param = random.choice([param_1, param_2])
    elif param_1 == True :
        param = param_1
    elif param_2 == True :
        param = param_2

    counter = 0
    for trial in block_nb.trials :
        houses_tones, faces_tones = define_tones(A_high, A_80_high, A_low, 
                                                A_80_low, *param.values())
        image_noise, tone_name = associate_morph_tone(exp, trial, houses_tones, 
                                                    faces_tones, time_waiting)
        trial.stimuli[0].present()  # display the morphes
        exp.clock.wait(time_morph)
        counter +=1
        if counter == 4 :
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
            confidence_score = rate_confidence(exp)
            counter = 0
            exp.data.add([block_nb.name, trial.id, trial.get_factor('name'), 
                                     tone_name, key, rt, confidence_score])
#####
INSTRUCTIONS = """
A nouveau, une image va vous être présentée. 
Vous devrez identifier s'il s'agit d'une maison ou d'un visage. 
La proportion d'images et de maison est fixe d'une session à l'autre.
Un indice auditif vous sera présenté au début de chaque manche. 
Appuyez sur les flèches de droite ou de gauche 
pour sélectionner votre réponse. 
Appuyez sur entrer pour avancer."""

# Creating notes
A_low = create_note(frequency)
A_80_low = create_note(frequency*1.2) #Note which is 80% low
A_medium = create_note(frequency*1.5)
A_80_high = create_note(frequency*1.8) #Note which is 80% high 
A_high = create_note(frequency*2)

#Creating set of pictures
house_left = expyriment.stimuli.Picture(path + '/Priors_and_responses/House_left.png', 
                                        position=left_pos)
face_right = expyriment.stimuli.Picture(path + '/Priors_and_responses/Face_right.png', 
                                        position = right_pos)
#Creating the response window
response_window = expyriment.stimuli.BlankScreen()
house_left.plot(response_window)
face_right.plot(response_window)

#####Hierarchy : 5 blocks of 20 trials
#Block1
block1 = expyriment.design.Block(name="First block")
#Load morphes for block1 with 50%H(50%, noise 4 and 5)
#50%F(50%, noise 1 and 2), sampled from the whole files
houses, faces = random_pictures (0.50, 0.50, nb_of_trials, path)
block1_images = (houses + faces)
random.shuffle(block1_images)

#Add every image as stimulus of one trial and add them to the block
for image in block1_images: 
    trial = expyriment.design.Trial()
    trial.add_stimulus(expyriment.stimuli.Picture(image))
    trial.set_factor('name', image[-19:]) #save picture name without path
    block1.add_trial(trial)
exp.add_block(block1)
    
#Block2
block2 = expyriment.design.Block(name="Second block")

#Load morphes for block2 with 50%H(50%, noise 4 and 5)
#50%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.50, 0.50, nb_of_trials, path)
block2_images = (houses + faces)
random.shuffle(block2_images)

#Add every image as stimulus of one trial and add them to the block
for image in block2_images:
    trial = expyriment.design.Trial()
    trial.add_stimulus(expyriment.stimuli.Picture(image))
    trial.set_factor('name', image[-19:]) #save picture name without path
    block2.add_trial(trial)
exp.add_block(block2)

#Block3
block3 = expyriment.design.Block(name="Third block")

#Load morphes for block3 with 50%H(50%, noise 4 and 5)
#50%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.50, 0.50, nb_of_trials, path)
block3_images = (houses + faces)
random.shuffle(block3_images)

#Add every image as stimulus of one trial and add them to the block
for image in block3_images:
    trial = expyriment.design.Trial()
    trial.add_stimulus(expyriment.stimuli.Picture(image))
    trial.set_factor('name', image[-19:]) #save picture name without path
    block3.add_trial(trial)
exp.add_block(block3)
    
#Block4
block4 = expyriment.design.Block(name="Fourth block")

#Load morphes for block4 with 40%H(50%, noise 4 and 5)
#60%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.40, 0.60, nb_of_trials, path)
block4_images = (houses + faces)
random.shuffle(block4_images)

#Add every image as stimulus of one trial and add them to the block
for image in block4_images:
    trial = expyriment.design.Trial()
    trial.add_stimulus(expyriment.stimuli.Picture(image))
    trial.set_factor('name', image[-19:]) #save picture name without path
    block4.add_trial(trial)
exp.add_block(block4)
 
#Block5
block5 = expyriment.design.Block(name="Fifth block")

#Load morphes for block5 with 60%H(50%, noise 4 and 5)
#40%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.60, 0.40, nb_of_trials, path)
block5_images = (houses + faces)
random.shuffle(block5_images)

#Add every image as stimulus of one trial and add them to the block
for image in block5_images:
    trial = expyriment.design.Trial()
    trial.add_stimulus(expyriment.stimuli.Picture(image))
    trial.set_factor('name', image[-19:]) #save picture name without path
    block5.add_trial(trial)
exp.add_block(block5)   

#Present instructions and preload
instructions = expyriment.stimuli.TextScreen("Instructions",text=INSTRUCTIONS)
instructions.preload()
expyriment.control.start()
instructions.present()
exp.keyboard.wait(keys = 13) #press enter
house_left.preload(), face_right.preload(), response_window.preload()

#####
#Experiment starts
expyriment.stimuli.BlankScreen(colour=BLACK).present()  # clear screen
exp.clock.wait(time_waiting)

#Block 1
session = expyriment.stimuli.TextScreen('Session 1', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_4(block1)
exp.clock.wait(time_interblocks)

    
#Block2
session = expyriment.stimuli.TextScreen('Session 2',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_4(block2)
exp.clock.wait(time_interblocks)

#Block3
session = expyriment.stimuli.TextScreen('Session 3', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_4(block3)
exp.clock.wait(time_interblocks)

#Block4
session = expyriment.stimuli.TextScreen('Session 4',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_4(block4)
exp.clock.wait(time_interblocks)

#Block5
session = expyriment.stimuli.TextScreen('Session 5',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_4(block5)
exp.clock.wait(time_interblocks)  
  
expyriment.control.end()

##to see data : 
#expyriment.misc.data_preprocessing.read_datafile(path+'/Bayesian_battery_codes/data/Bayesian_battery_exp_4.1_copy_11_201909161447.xpd')    
