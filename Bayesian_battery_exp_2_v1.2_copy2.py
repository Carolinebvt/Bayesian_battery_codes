#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 08:03:27 2019

@author: carolinebevalot
"""
import expyriment
import random
from Bayesian_battery_functions_v1 import random_pictures, rate_confidence

#### Global variables
BLACK = (0, 0, 0)
path = '/Users/carolinebevalot/Desktop/Bayesian_battery'

exp = expyriment.design.Experiment(name="Second Experiment")

# Position of pictures in response_window
left_pos = (-150, 0)
right_pos = (150, 0)

# Times
time_prior = 800 
time_interblocks = 1500
time_waiting = 200
time_morph = 800
nb_of_trials = 20
#nb of trials should be a multiple of 5 and 2 for the nb of morphs to be an integer

prop_levels = 0.50 # proportion of noise 1,2 or 4,5 

frequency = 220 # frequency of the lowest tone (A)

expyriment.control.initialize(exp) 

##### Functions
def execute_trial_2(block_nb):
    """Function which runs a block. For each trial, it presents the morph, 
    presents the response window, wait for the right or left answer and record 
    them with the corresponding response time. One trial out of 4, it asks for 
    confidence rating."""
    
    count = 0 # confidence rating 1 trial out of 4
    for trial in block_nb.trials:
        expyriment.stimuli.BlankScreen(colour=BLACK).present()  
        exp.clock.wait(time_waiting)
        trial.stimuli[0].present()  # display the morph
        exp.clock.wait(time_morph)      
        expyriment.stimuli.BlankScreen(colour=BLACK).present()  # black screen
        exp.clock.wait(time_waiting)
        response_window.present() #response screen
        #Wait for an answer and highlight the answer
        key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                     expyriment.misc.constants.K_RIGHT])
        if key == 275 :#pressing right arrow
            face_right.present()
            exp.clock.wait(time_waiting)
        elif key == 276:#pressing left arrow
            house_left.present()
            exp.clock.wait(time_waiting) 
        count+=1
        if count == 4 : 
            confidence_score = rate_confidence(exp, time_waiting)
            count = 0
            exp.data.add([block_nb.name, trial.id, trial.get_factor('name'), 
                                                key, rt, confidence_score])
        else :
            exp.data.add([block_nb.name, trial.id, trial.get_factor('name'),
                                                                  key, rt])


#####                           
INSTRUCTIONS1 = """
A nouveau, une image va vous être présentée. 
Vous devrez identifier s'il s'agit d'une maison ou d'un visage. 
La proportion d'images et de maison est possiblement différente d'une session à l'autre.
L'indice visuel ne vous sera plus présenté au début de chaque manche. 
Appuyez sur les flèches de droite ou de gauche 
pour sélectionner votre réponse. 
Appuyez sur entrer pour avancer."""



#Creating set of pictures
house_left = expyriment.stimuli.Picture(path + '/Priors_and_responses/House_left.png', 
                                        position=left_pos)
face_right = expyriment.stimuli.Picture(path + '/Priors_and_responses/Face_right.png', 
                                        position = right_pos)
#Creating the response window
response_window = expyriment.stimuli.BlankScreen()
house_left.plot(response_window)
face_right.plot(response_window)

##### Hierarchy : 5 blocks of x trials
#Block1
block1 = expyriment.design.Block(name="First block")
#Load morphes for block1 with 80%H(50%, noise 4 and 5)
#20%F(50%, noise 1 and 2), sampled from the whole files
houses, faces = random_pictures (0.80, 0.20, nb_of_trials, path)
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
#Load morphes for block2 with 20%H(50%, noise 4 and 5)
#80%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.20, 0.80, nb_of_trials, path)
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

#####Present instructions and preload
instructions1 = expyriment.stimuli.TextScreen("Instructions",text=INSTRUCTIONS1)
instructions1.preload()
expyriment.control.start()
instructions1.present()
exp.keyboard.wait(keys = 13) #press enter
house_left.preload(), face_right.preload(), response_window.preload()


#Experiment starts
expyriment.stimuli.BlankScreen(colour=BLACK).present()  # clear screen
exp.clock.wait(time_waiting)

#Block 1
session = expyriment.stimuli.TextScreen('Session 1', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
execute_trial_2(block1)
exp.clock.wait(time_interblocks)

#Block2
session = expyriment.stimuli.TextScreen('Session 2',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
execute_trial_2(block2)
exp.clock.wait(time_interblocks)

#Block3
session = expyriment.stimuli.TextScreen('Session 3', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
execute_trial_2(block3)
exp.clock.wait(time_interblocks)

#Block4
session = expyriment.stimuli.TextScreen('Session 4',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
execute_trial_2(block4)
exp.clock.wait(time_interblocks)

#Block5
session = expyriment.stimuli.TextScreen('Session 5',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
execute_trial_2(block5)
exp.clock.wait(time_interblocks)  
  
expyriment.control.end()

##to see data : 
#expyriment.misc.data_preprocessing.read_datafile(path+'/Bayesian_battery_codes/data/Bayesain_battery_exp_1.3_copy_03_201909191709.xpd')    


