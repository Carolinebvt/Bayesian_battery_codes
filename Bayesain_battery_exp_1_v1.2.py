#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 16:34:55 2019

@author: carolinebevalot
"""
import expyriment
import random
from Bayesian_battery_functions_v1 import random_pictures, rate_confidence

#### Global variables
BLACK = (0, 0, 0)
path = '/Users/carolinebevalot/Desktop/Bayesian_battery'

exp = expyriment.design.Experiment(name="First Experiment")

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


def execute_trial_1(block_nb):
    """Function which runs a block. For each trial, it presents the prior and 
    the morph, presents the response window, wait for the right or left answer 
    and record them with the corresponding response time. One trial out of 4, 
    it asks for confidence rating."""
    count = 0
    for trial in block_nb.trials:
        prior.present()
        exp.clock.wait(time_prior)
        expyriment.stimuli.BlankScreen(colour=BLACK).present()  # clear screen
        exp.clock.wait(time_waiting)
        trial.stimuli[0].present()  # display the morphes
        exp.clock.wait(time_morph)      
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
        count+=1
        if count == 4 : 
            confidence_score = rate_confidence(exp)
            count = 0
            exp.data.add([block_nb.name, trial.id, trial.get_factor('name'), 
                                                key, rt, confidence_score])
        else :
            exp.data.add([block_nb.name, trial.id, trial.get_factor('name'),
                                                                  key, rt])


INSTRUCTIONS1 = """
Une image va vous être présentée. 
Vous devrez identifier s'il s'agit d'une maison ou d'un visage. 
La proportion d'images et de maison est possiblement différente d'une session à l'autre.
Un indice visuel vous sera présenté au début de chaque manche. 
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
#Creating the priors
prior_80H20F = expyriment.stimuli.Picture(path + '/Priors_and_responses/Prior_80H20F.png')
prior_20H80F = expyriment.stimuli.Picture(path + '/Priors_and_responses/Prior_20H80F.png')
prior_50H50F = expyriment.stimuli.Picture(path + '/Priors_and_responses/Prior_50H50F.png')

#Hierarchy : 3 blocks of 20 trials
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
    trial.set_factor('name', image[-19:])
    block1.add_trial(trial)
exp.add_block(block1)

#Block2
block2 = expyriment.design.Block(name="Second block")

#Load morphes for block12 with 20%H(50%, noise 4 and 5)
#80%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.20, 0.80, nb_of_trials, path)
block2_images = (houses + faces)
random.shuffle(block2_images)

#Add every image as stimulus of one trial and add them to the block
for image in block2_images:
    trial = expyriment.design.Trial()
    trial.add_stimulus(expyriment.stimuli.Picture(image))
    trial.set_factor('name', image[-19:])
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
    trial.set_factor('name', image[-19:])
    block3.add_trial(trial)
exp.add_block(block3)
    
    
#Present instructions and preload
instructions1 = expyriment.stimuli.TextScreen("Instructions",text=INSTRUCTIONS1)
instructions1.preload()
expyriment.control.start()
instructions1.present()
exp.keyboard.wait(keys = 13) #press enter
prior_80H20F.preload(),prior_20H80F.preload(), prior_50H50F.preload() 
house_left.preload(), face_right.preload(), response_window.preload()


#Experiment starts
expyriment.stimuli.BlankScreen(colour=BLACK).present()  # clear screen
exp.clock.wait(time_waiting)


#Block 1
session = expyriment.stimuli.TextScreen('Session 1', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
prior = prior_80H20F
execute_trial_1(block1)
exp.clock.wait(time_interblocks)

#Block2
session = expyriment.stimuli.TextScreen('Session 2',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
prior = prior_20H80F
execute_trial_1(block2)
exp.clock.wait(time_interblocks)

#Block3
session = expyriment.stimuli.TextScreen('Session 3', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
prior = prior_50H50F
execute_trial_1(block3)
exp.clock.wait(time_interblocks)
    
expyriment.control.end()

##to see data : 
#expyriment.misc.data_preprocessing.read_datafile(path+'/Bayesian_battery_codes/data/Bayesain_battery_exp_1.3_copy_03_201909191709.xpd')    


