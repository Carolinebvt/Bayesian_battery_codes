#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 17:44:17 2019

@author: carolinebevalot
"""
import expyriment
import random
from Bayesian_battery_functions_v1 import random_pictures, rate_confidence, \
     create_note, play_notes, associate_morph_tone, define_tones, select_response

#### Global variables
BLACK = (0, 0, 0)
path = '/Users/carolinebevalot/Desktop/Bayesian_battery'

exp = expyriment.design.Experiment(name="Fifth Experiment")

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
def execute_trial_5(block_nb, shuffle = True, param_1 = False, param_2 = False):
    """Function which runs blocks. For each trial, it presents the tone, 
    the morph and the response window and save the block name, the trial ID 
    and name, the tone name, the response key and response time.
   
    Block is divided into three parts : first half where the tone is predictive
    of the morph, second half divided into a part where the tone is oppositely 
    predictive of the morph and a part where the tone is unpredictive.
    
    Each part calls define_tones() to set lists of tones for houses and faces, 
    then associate_morph_tone() to choose randomly between a pur or 80% tone, 
    to play it and present the morph. 3 morphs are presented with the response 
    window and the confidence scale is presented for the 4th morph. 
       
    By default, whether the 2nd part is oppositely predictive and 3rd is 
    unpredictive or whether it is the opposite is randomised for each block.
    It is possible to set block as : 
        predictive-opposite-unpredictive with param_1 = True, (shuffle=False)
        predictive-unpredictive-opposite with param_2 = True, (shuffle=False)
    """
    # Define the parameters that will be apply in the 3 parts of the block 
    # to define tones as predictive, oppositely predictive or unpredictive
    param_1 = [{'opposite':False, 'unpredictive':False}, 
              {'opposite':True, 'unpredictive':False}, 
              {'opposite':False, 'unpredictive':True}]
    
    param_2 = [{'opposite' :False, 'unpredictive':False}, 
              {'opposite':False, 'unpredictive':True}, 
              {'opposite':True, 'unpredictive':False}]
    if shuffle == True : 
        param = random.choice([param_1, param_2])
    elif param_1 == True :
        param = param_1
    elif param_2 == True :
        param = param_2
    
  

    # Start the block with asking 1 question out of 5 trials,
    # Each block is divided into 3 three parts : predictive /opposite / unpredictive 
    count = 0
    #first half
    for trial in block_nb.trials[:int(nb_of_trials/2)] :
       #predictive tone
       houses_tones, faces_tones = define_tones(A_high, A_80_high, A_low, 
                                                A_80_low, *param[0].values())
       image_noise, tone_name = associate_morph_tone(exp, trial, houses_tones, 
                                                    faces_tones, time_waiting)
       trial.stimuli[0].present()  # display the morphes
       exp.clock.wait(time_morph)       
       count +=1
       key, rt = select_response(exp, time_waiting, response_window, 
                                                 face_right, house_left)
       exp.data.add([block_nb.name, param[0], trial.id, 
               trial.get_factor('name'), tone_name, key, rt])
       if count == 4 :
           confidence_score = rate_confidence(exp)
           count = 0
           exp.data.add([block_nb.name, param[0], trial.id, 
               trial.get_factor('name'), tone_name, key, rt, confidence_score])
        
    # 2nd half divided into opposite and unpredictive randomly by default
    for trial in block_nb.trials[int(nb_of_trials/2):int(3/4 * nb_of_trials)] :
       #predictive tone
       houses_tones, faces_tones = define_tones(A_high, A_80_high, A_low, 
                                                A_80_low, *param[1].values())
       image_noise, tone_name = associate_morph_tone(exp, trial, houses_tones, 
                                                    faces_tones, time_waiting)
       trial.stimuli[0].present()  # display the morphes
       exp.clock.wait(time_morph)       
       count +=1
       key, rt = select_response(exp, time_waiting, response_window, 
                                                 face_right, house_left)
       exp.data.add([block_nb.name, param[1], trial.id, 
               trial.get_factor('name'), tone_name, key, rt])
       if count == 4 :
           confidence_score = rate_confidence(exp)
           count = 0
           exp.data.add([block_nb.name, param[1], trial.id, 
               trial.get_factor('name'), tone_name, key, rt, confidence_score])
        
    for trial in block_nb.trials[int(3/4 * nb_of_trials):] : 
        #predictive tone
       houses_tones, faces_tones = define_tones(A_high, A_80_high, A_low, 
                                                A_80_low, *param[2].values())
       image_noise, tone_name = associate_morph_tone(exp, trial, houses_tones, 
                                                    faces_tones, time_waiting)
       trial.stimuli[0].present()  # display the morphes
       exp.clock.wait(time_morph)       
       count +=1
       key, rt = select_response(exp, time_waiting, response_window, 
                                                 face_right, house_left)
       exp.data.add([block_nb.name, param[2], trial.id, 
               trial.get_factor('name'), tone_name, key, rt])
       if count == 4 :
           confidence_score = rate_confidence(exp)
           count = 0
           exp.data.add([block_nb.name, param[2], trial.id, 
               trial.get_factor('name'), tone_name, key, rt, confidence_score])
        

#####
INSTRUCTIONS = """
Une image va vous être présentée. 
Vous devrez identifier s'il s'agit d'une maison ou d'un visage. 
Un indice auditif vous sera présenté au début de chaque manche. 
Le sens de l'association peut changer au cours du temps.
La proportion d'images et de maison est 
possiblement différente d'une session à l'autre.
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

#Load morphes for block2 with 50%H(50%, noise 4 and 5)
#50%F(50%, noise 1 and 2), sampled from the whole file
houses, faces = random_pictures (0.40, 0.60, nb_of_trials, path)
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
houses, faces = random_pictures (0.20, 0.80, nb_of_trials, path)
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
houses, faces = random_pictures (0.50, 0.50, nb_of_trials, path)
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
instructions = expyriment.stimuli.TextScreen("Instructions",text=INSTRUCTIONS)
instructions.preload()
expyriment.control.start()
instructions.present()
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
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_5(block1, shuffle=True)
exp.clock.wait(time_interblocks)

    
#Block2
session = expyriment.stimuli.TextScreen('Session 2',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_5(block2)    
exp.clock.wait(time_interblocks)

#Block3
session = expyriment.stimuli.TextScreen('Session 3', text = '')
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_5(block3) 
exp.clock.wait(time_interblocks)

#Block4
session = expyriment.stimuli.TextScreen('Session 4',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_5(block4) 
exp.clock.wait(time_interblocks)

#Block5
session = expyriment.stimuli.TextScreen('Session 5',text ='' )
session.preload()
session.present()
exp.clock.wait(time_prior)
play_notes(A_low, A_80_low, A_high, A_80_high)
execute_trial_5(block5, shuffle = True)    
exp.clock.wait(time_interblocks) 
  
expyriment.control.end()

##to see data : 
#expyriment.misc.data_preprocessing.read_datafile(path+'/Bayesian_battery_codes/Bayesian_battery_exp_5_01_201909161835.xpd')    
