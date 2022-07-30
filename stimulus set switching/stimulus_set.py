# Code for stimulus set switching experiment to present to ACT-R


#----------------------------------------------------------
# setup

# Import the actr module 
import actr

# Import the importlib library to reload ACT-R models when changed
# import importlib
# importlib.reload(episodic)
# importlib.reload(model_name)

# Import other libraries
import random


# Load the corresponding model for the task
actr.load_act_r_model("ACT-R:my models;stimulus set switching;stimulus_set_model.lisp")

# Global variables to hold the trials to present & the results that have
# been collected
trials = []
results = []

# human data for later comparison
# in the order 
# - RR-repetition/SS-repetition
# - RR-repetition/SS-switch
# - RR-switch/SS-repetition
# - RR-switch/SS-switch
human_rts = [1.176, 1.430, 1.431, 1.555]
human_accuracy = [0.973, 0.964, 0.944, 0.948] 

# global variable to indicate whether it will be a model or person
run_model = True

# class to hold information pertaining to a single trial
class trial():
    def __init__(self, block, cue, cue_colour, stim_left, stim_right, 
                stim_left_colour, stim_right_colour, response_set_sequence,
                stimulus_set_sequence, correct_response, visible = None):
                self.block = block
                self.cue = cue
                self.cue_colour = cue_colour
                self.stim_left = stim_left
                self.stim_right = stim_right
                self.stim_left_colour = stim_left_colour
                self.stim_right_colour = stim_right_colour
                self.response_set_sequence = response_set_sequence
                self.stimulus_set_sequence = stimulus_set_sequence
                self.correct_response = correct_response
                if visible == None:
                    self.visible = not(run_model)
                else:
                    self.visible = visible
                self.correct = False



#----------------------------------------------------------
# function to rune one participant through the experiment
def do_experiment(n_blocks, n_trials, visible = None):

    actr.reset()

    global trials
    trials = []

    global results
    results = []  

    get_trial_info(n_blocks = n_blocks, n_trials = n_trials, visible = visible)
    collect_responses()
    # analyse_results()



#----------------------------------------------------------
# get trial information for run through the experiment
def get_trial_info(n_blocks, n_trials, visible = True):

    global results
    results = []

    global trials 
    trials = []

    # declare the possible cues, stimuli, and colours etc.
    response_sets = ['magnitude', 'parity']
    stimulus_sets = ['red', 'blue']
    stimuli = ['1', '2', '3', '4', '6', '7', '8', '9']
    stim_colours = ['red', 'blue']
    stimulus_locations = ['left', 'right']

    # decalre other trial variables
    current_cue = 'null'
    current_cue_colour = 'null'
    current_a_stim = 'null'
    current_b_stim = 'null'
    stim_left = 'null'
    stim_right = 'null'
    stim_left_colour = 'null'
    stim_right_colour = 'null'
    relevant_location = 'null'
    relevant_stimulus = 'null'
    irrelevant_stimulus = 'null'
    relevant_stimulus_colour = 'null'
    irrelevant_stimulus_colour = 'null'
    current_response_set = 'null'
    previous_response_set = 'null'
    current_stimulus_set = 'null'
    previous_stimulus_set = 'null'
    sequence_response_set = 'null'
    sequence_stimulus_set = 'null'
    relevant_response = 'null'
    irrelevant_response = 'null'

    # loop over blocks...
    for i in range(n_blocks):
        
        block = i + 1
        
        # loop over trials...
        for j in range(n_trials):

            # get the current response & stimulus sets
            current_response_set = random.choice(response_sets)
            current_stimulus_set = random.choice(stimulus_sets)

            # set the cue colour & stimuli colours
            current_cue_colour = current_stimulus_set
            
            if current_stimulus_set == 'red':
                relevant_stimulus_colour = 'red'
                irrelevant_stimulus_colour = 'blue'
            else:
                relevant_stimulus_colour = 'blue'
                irrelevant_stimulus_colour = 'red'


            # set the current response set sequence
            if current_response_set == previous_response_set:
                sequence_response_set = 'repetition'
            else:
                sequence_response_set = 'switch'
            
            # set the current stimulus set sequence
            if current_stimulus_set == previous_stimulus_set:
                sequence_stimulus_set = 'repetition'
            else:
                sequence_stimulus_set = 'switch'
            
            # get the current cue
            if current_response_set == 'magnitude':
                current_cue = 'LowHigh'
            else:
                current_cue = 'OddEven'
            
            # get the current stimuli
            random.shuffle(stimuli)
            current_a_stim = stimuli[0]
            current_b_stim = stimuli[1]

            # choose the relevant and irrelevant stimuli
            if current_stimulus_set == "red":
                relevant_stimulus = current_a_stim
                irrelevant_stimulus = current_b_stim
            else:
                relevant_stimulus = current_b_stim
                irrelevant_stimulus = current_a_stim

            # place the stimuli in the relevant location
            random.shuffle(stimulus_locations)
            relevant_location = stimulus_locations[0]

            if relevant_location == 'left':
                stim_left = relevant_stimulus
                stim_right = irrelevant_stimulus
                stim_left_colour = relevant_stimulus_colour
                stim_right_colour = irrelevant_stimulus_colour
            else:
                stim_left = irrelevant_stimulus
                stim_right = relevant_stimulus
                stim_left_colour = irrelevant_stimulus_colour
                stim_right_colour = relevant_stimulus_colour

            # set the correct response to the relevant stimulus
            if current_response_set == 'magnitude':
                if relevant_stimulus == '1' or relevant_stimulus == '2' or relevant_stimulus == '3' or relevant_stimulus == '4':
                    relevant_response = 'z'
                else:
                    relevant_response = 'm'
            if current_response_set == 'parity':
                if relevant_stimulus == '1' or relevant_stimulus == '3' or relevant_stimulus == '7' or relevant_stimulus == '9':
                    relevant_response = 'z'
                else:
                    relevant_response = 'm'


            # save all trial data
            trials.append(trial(block, 
                        current_cue,
                        current_cue_colour, 
                        stim_left, 
                        stim_right, 
                        stim_left_colour, 
                        stim_right_colour, 
                        sequence_response_set, 
                        sequence_stimulus_set, 
                        relevant_response, 
                        visible))

            # set the currrent trial information to previous trial information
            previous_response_set = current_response_set
            previous_stimulus_set = current_stimulus_set



#----------------------------------------------------------
# collect the responses for all of the trials available
def collect_responses():

    # record how many trials need to be run
    total_trials = len(trials)

    # create a command for respond_to_key_press and monitor output-key
    actr.add_command("stimulus-set-response", respond_to_key_press,
                     "stimulus-set task key press response monitor")
    actr.monitor_command("output-key","stimulus-set-response")

    # present the trial
    present_trial(trials[0])

    # if it's a model doing the task run for 10s per trial,
    # and if it's a person loop until there are as many results
    # as there were trials to run
    if run_model:
        actr.run(10 * total_trials)
    else: 
        if actr.visible_virtuals_available():
            while len(results) < total_trials:
                actr.process_events()   

    # stop monitoring the ACT-R commands and remove them
    actr.remove_command_monitor("output-key", "stimulus-set-response")
    actr.remove_command("stimulus-set-response")



#----------------------------------------------------------
# respond_to_key_press function monitors the output-key actions, 
# and thus will be called with two parameters when a key is pressed: 
# the name of the model that pressed the key (or None if it is a person) 
# and the string naming the key that was pressed. 
def respond_to_key_press(model, key):

    global trials, results
    
    # get the response time of the response
    trials[0].time = (actr.get_time(run_model) - trials[0].start) / 1000.0

    # get the accuracy of the response
    if key.lower() == trials[0].correct_response:
        trials[0].correct = True
    
    # append the results
    results.append(trials[0])

    # remove the current trial from the list of trials to execute
    # if there are more trials to present, present the next trial now
    trials = trials[1:]
    if len(trials) > 0:
        present_trial(trials[0], new_window = False)



#----------------------------------------------------------
# present a single trial
def present_trial(trial, new_window = True):
    # only start a new windown when needed (e.g., on first trial of participant)
    # otherwise, just clear the current experiment window
    # this saves time
    if new_window == True:
        window = actr.open_exp_window("Stimulus set switching", visible = trial.visible)
        if run_model:
            actr.install_device(window)
    else:
         actr.clear_exp_window()
    
    # add the cue to the screen
    actr.add_text_to_exp_window(None, text = trial.cue, color = trial.cue_colour, 
                                x = 125, y = 120)

    # add the two stimuli to the screen
    actr.add_text_to_exp_window(None, text = trial.stim_left, 
                                color = trial.stim_left_colour, 
                                x = 135, y = 150)
    actr.add_text_to_exp_window(None, text = trial.stim_right, 
                                color = trial.stim_right_colour, 
                                x = 165, y = 150)
    
    # add the time the trial started to the trial information
    trial.start = actr.get_time(run_model)




#----------------------------------------------------------
# analyse the results
def analyse_results():

    # TODO: average over blocks
    blocks = []

    # containers for response times
    rs_rep_ss_rep_rts = []
    rs_rep_ss_sw_rts = []
    rs_sw_ss_rep_rts = []
    rs_sw_ss_sw_rts = []

    # containers for accuracy
    rs_rep_ss_rep_acc = []
    rs_rep_ss_sw_acc = []
    rs_sw_ss_rep_acc = []
    rs_sw_ss_sw_acc = []

    # extract the response times
    for i in results:
        if i.response_set_sequence == 'repetition':
            if i.stimulus_set_sequence == 'repetition':
                rs_rep_ss_rep_rts.append(i.time)
            if i.stimulus_set_sequence == 'switch':
                rs_rep_ss_sw_rts.append(i.time)
        if i.response_set_sequence == 'switch':
            if i.stimulus_set_sequence == 'repetition':
                rs_sw_ss_rep_rts.append(i.time)
            if i.stimulus_set_sequence == 'switch':
                rs_sw_ss_sw_rts.append(i.time)
    
    # extract the accuracy
    for i in results:
        if i.response_set_sequence == 'repetition':
            if i.stimulus_set_sequence == 'repetition':
                if i.correct == True:
                    rs_rep_ss_rep_acc.append(1)
                else:
                    rs_rep_ss_rep_acc.append(0)
            if i.stimulus_set_sequence == 'switch':
                if i.correct == True:
                    rs_rep_ss_sw_acc.append(1)
                else:
                    rs_rep_ss_sw_acc.append(0)
        if i.response_set_sequence == 'switch':
            if i.stimulus_set_sequence == 'repetition':
                if i.correct == True:
                    rs_sw_ss_rep_acc.append(1)
                else:
                    rs_sw_ss_rep_acc.append(0)
            if i.stimulus_set_sequence == 'switch':
                if i.correct == True:
                    rs_sw_ss_sw_acc.append(1)
                else:
                    rs_sw_ss_sw_acc.append(0)
    
    # get the mean rts
    mean_rs_rep_ss_rep_rts = round(sum(rs_rep_ss_rep_rts) / len(rs_rep_ss_rep_rts), 3)
    mean_rs_rep_ss_sw_rts = round(sum(rs_rep_ss_sw_rts) / len(rs_rep_ss_sw_rts), 3)
    mean_rs_sw_ss_rep_rts = round(sum(rs_sw_ss_rep_rts) / len(rs_sw_ss_rep_rts), 3)
    mean_rs_sw_ss_sw_rts = round(sum(rs_sw_ss_sw_rts) / len(rs_sw_ss_sw_rts), 3)

    # get the mean accuracy
    mean_rs_rep_ss_rep_acc = round(sum(rs_rep_ss_rep_acc) / len(rs_rep_ss_rep_acc), 3)
    mean_rs_rep_ss_sw_acc = round(sum(rs_rep_ss_sw_acc) / len(rs_rep_ss_sw_acc), 3)
    mean_rs_sw_ss_rep_acc = round(sum(rs_sw_ss_rep_acc) / len(rs_sw_ss_rep_acc), 3)
    mean_rs_sw_ss_sw_acc = round(sum(rs_sw_ss_sw_acc) / len(rs_sw_ss_sw_acc), 3)

    model_rts = [mean_rs_rep_ss_rep_rts, 
                mean_rs_rep_ss_sw_rts, 
                mean_rs_sw_ss_rep_rts, 
                mean_rs_sw_ss_sw_rts]

    model_acc = [mean_rs_rep_ss_rep_acc, 
                mean_rs_rep_ss_sw_acc, 
                mean_rs_sw_ss_rep_acc, 
                mean_rs_sw_ss_sw_acc]
    

    print("         ")
    print("RTs: ")
    print("Model: ", model_rts)
    print("Human: ", human_rts)
    print("         ")
    print("ACCURACY: ")
    print("Model:", model_acc)
    print("Human:", human_accuracy)
    print("---------")
    actr.correlation(model_rts + model_acc, human_rts + human_accuracy)
    actr.mean_deviation(model_rts, human_rts)