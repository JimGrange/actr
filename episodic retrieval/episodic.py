# Code for episodic retrieval experiment to present to ACT-R


#----------------------------------------------------------
# setup

# Import the actr module for tutorial tasks
from re import X
import actr

# Import the importlib library to reload ACT-R models when changed
# import importlib
# importlib.reload(episodic)
# importlib.reload(model_name)

# Import other libraries
import random


# Load the corresponding model for the task
actr.load_act_r_model("ACT-R:my models;episodic retrieval;episodic_retrieval_model.lisp")

# Global variables to hold the trials to present, the results that have
# been collected, and the original data for comparison (Grange et al., 2017; experiment 2 shapes)
trials = []
results = []
grange_rts = [1.053, 1.027, 1.148, 1.039] # (in the order ABA_rep, CBA_rep, ABA_sw, CBA_sw)
grange_accuracy = [0.969, 0.958, 0.942, 0.966] # (in the order ABA_rep, CBA_rep, ABA_sw, CBA_sw)

# global variable to indicate whether it will be a model or person
run_model = False

# class to hold information pertaining to a single trial
class trial():
    def __init__(self, block, cue, rule, rule_sequence, stimulus, stim_x, stim_y, 
                 response_sequence, correct_response, visible = None):
        self.block = block
        self.cue = cue
        self.rule = rule
        self.rule_sequence = rule_sequence
        self.stimulus = stimulus
        self.stim_x = stim_x
        self.stim_y = stim_y
        self.response_sequence = response_sequence
        self.correct_response = correct_response
        if visible == None:
            self.visible = not(run_model)
        else:
            self.visible = visible
        self.correct = False



#----------------------------------------------------------
def do_experiment(n_blocks, n_trials, visible = None):

    actr.reset()

    global trials
    trials = []

    global results
    results = []  

    get_trial_info(n_blocks = n_blocks, n_trials = n_trials, visible = visible)
    collect_responses()
    analyse_results()



#----------------------------------------------------------
# get trial information for run through the experiment

def get_trial_info(n_blocks, n_trials, visible = True):

    global results
    results = []

    global trials
    trials = []

    # declare the possible cues, stimuli, and stimulus location
    # square = vertical
    # triangle = horizontal
    # hexagon = diagonal
    cues = ['square', 'triangle', 'hexagon']
    stimuli = ['tl', 'tr', 'bl', 'br']
    stimulus_identity = 'X'

    # declare possible next cues based on previous trial
    # (to ensure no immediate task repetitions)
    square_prev = ['triangle', 'hexagon']
    triangle_prev = ['square', 'hexagon']
    hexagon_prev = ['square', 'triangle']

    # declare stimulus positions
    stim_x = 50
    stim_y = 50

    # declare variables to hold infomration from previous trials
    curr_cue = 'null'
    curr_rule = 'null'
    n1_cue = 'null'
    n2_cue = 'null'
    
    curr_stim = 'null'

    curr_response = 'null'
    n1_response = 'null'
    n2_response = 'null'

    curr_seq = 'null'
    curr_response_seq = 'null'

    
    for i in range(n_blocks):
        
        block = i + 1

        # loop over desired trials and create structure
        for j in range(n_trials):

            # get the current cue 
            if n1_cue == 'null':
                curr_cue = random.choice(cues)
            if n1_cue == 'square':
                curr_cue = random.choice(square_prev)
            if n1_cue == 'triangle':
                curr_cue = random.choice(triangle_prev)
            if n1_cue == 'hexagon':
                curr_cue = random.choice(hexagon_prev)

            # get the current rule
            if curr_cue == 'square':
                curr_rule = 'vertical'
            if curr_cue == 'triangle':
                curr_rule = 'horizontal'    
            if curr_cue == 'hexagon':
                curr_rule = 'diagonal'

            # get the current stimulus location
            curr_stim = random.choice(stimuli)

            # get rule sequencing information
            if curr_cue == n2_cue:
                curr_seq = 'ABA'
            else:
                curr_seq = 'CBA'
            
            # set the location of the stimulus
            if curr_stim == 'tl':
                stim_x = 50
                stim_y = 50
            if curr_stim == 'tr':
                stim_x = 250
                stim_y = 50
            if curr_stim == 'bl':
                stim_x = 50
                stim_y = 250
            if curr_stim == 'br':
                stim_x = 250
                stim_y = 250

            # set the correct response
            if curr_rule == 'horizontal':
                if curr_stim == 'tl':
                    curr_response = 'j'
                if curr_stim == 'tr':
                    curr_response = 'd'
                if curr_stim == 'bl':
                    curr_response = 'n'
                if curr_stim == 'br':
                    curr_response = 'c'

            if curr_rule == 'vertical':
                if curr_stim == 'tl':
                    curr_response = 'c'
                if curr_stim == 'tr':
                    curr_response = 'n'
                if curr_stim == 'bl':
                    curr_response = 'd'
                if curr_stim == 'br':
                    curr_response = 'j'

            if curr_rule == 'diagonal':
                if curr_stim == 'tl':
                    curr_response = 'n'
                if curr_stim == 'tr':
                    curr_response = 'c'
                if curr_stim == 'bl':
                    curr_response = 'j'
                if curr_stim == 'br':
                    curr_response = 'd'
            
            # decide whether it is an n-2 response repetition or not
            if curr_response == n2_response:
                curr_response_seq = 'repetition'
            else:
                curr_response_seq = 'switch'
            
            # save all the trial data
            trials.append(trial(block, 
                        curr_cue, 
                        curr_rule,
                        curr_seq, 
                        stimulus_identity,
                        stim_x,
                        stim_y, 
                        curr_response_seq, 
                        curr_response, 
                        visible))
            
            # set the current trial information as previous trial etc.
            n2_cue = n1_cue
            n1_cue = curr_cue

            n2_response = n1_response
            n1_response = curr_response  
    


#----------------------------------------------------------
# analyse the results
def analyse_results():

    # TODO: average over blocks
    blocks = []

    # containers for response times
    aba_rep_rts = []
    cba_rep_rts = []
    aba_sw_rts = []
    cba_sw_rts = []

    # containers for accuracy
    aba_rep_acc = []
    cba_rep_acc = []
    aba_sw_acc = []
    cba_sw_acc = []

    # harvest the response times 
    # TODO: remove error trials and 2 trials following error
    for i in results:
        if i.rule_sequence == "ABA":
            if i.response_sequence == "repetition":
                aba_rep_rts.append(i.time)
            if i.response_sequence == "switch":
                aba_sw_rts.append(i.time)
        if i.rule_sequence == "CBA":
            if i.response_sequence == "repetition":
                cba_rep_rts.append(i.time)
            if i.response_sequence == "switch":
                cba_sw_rts.append(i.time)

    # harvest the accuracy
    # TODO: remove 2 trials following an error
    for i in results:
        if i.rule_sequence == "ABA":
            if i.response_sequence == "repetition":
                if i.correct == True:
                    aba_rep_acc.append(1)
                else:
                    aba_rep_acc.append(0)
            if i.response_sequence == "switch":
                if i.correct == True:
                    aba_sw_acc.append(1)
                else:
                    aba_sw_acc.append(0)
        if i.rule_sequence == "CBA":
            if i.response_sequence == "repetition":
                if i.correct == True:
                    cba_rep_acc.append(1)
                else:
                    cba_rep_acc.append(0)
            if i.response_sequence == "switch":
                if i.correct == True:
                    cba_sw_acc.append(1)
                else:
                    cba_sw_acc.append(0)

    #print(sum(aba_rep_rts) / len(aba_rep_rts))

    # get the mean rts
    mean_aba_rep_rts = round(sum(aba_rep_rts) / len(aba_rep_rts), 3)
    mean_aba_sw_rts = round(sum(aba_sw_rts) / len(aba_sw_rts), 3)
    mean_cba_rep_rts = round(sum(cba_rep_rts) / len(cba_rep_rts), 3)
    mean_cba_sw_rts = round(sum(cba_sw_rts) / len(cba_sw_rts), 3)

    # get the mean accuracy
    mean_aba_rep_acc = round(sum(aba_rep_acc) / len(aba_rep_acc), 3)
    mean_aba_sw_acc = round(sum(aba_sw_acc) / len(aba_sw_acc), 3)
    mean_cba_rep_acc = round(sum(cba_rep_acc) / len(cba_rep_acc), 3)
    mean_cba_sw_acc = round(sum(cba_sw_acc) / len(cba_sw_acc), 3)
    
    model_rts = [mean_aba_rep_rts, mean_cba_rep_rts, mean_aba_sw_rts, mean_cba_sw_rts]
    model_accuracy = [mean_aba_rep_acc, mean_cba_rep_acc, mean_aba_sw_acc, mean_cba_sw_acc]

    print("         ")
    print("RTs: ")
    print("Model: ", model_rts)
    print("Human: ", grange_rts)
    print("         ")
    print("ACCURACY: ")
    print("Model:", model_accuracy)
    print("Human:", grange_accuracy)
    print("---------")
    actr.correlation(model_rts + model_accuracy, grange_rts + grange_accuracy)
    actr.mean_deviation(model_rts, grange_rts)
 

   
#----------------------------------------------------------
# collect the responses for all of the trials available
def collect_responses():

    # record how many trials need to be run
    total_trials = len(trials)

    # create a command for respond_to_key_press and monitor output-key
    actr.add_command("episodic-response", respond_to_key_press,
                     "episodic task key press response monitor")
    actr.monitor_command("output-key","episodic-response")

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
    actr.remove_command_monitor("output-key", "episodic-response")
    actr.remove_command("episodic-response")



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
        window = actr.open_exp_window("Episodic Retrieval", visible = trial.visible)
        if run_model:
            actr.install_device(window)
    else:
         actr.clear_exp_window()

    actr.add_text_to_exp_window(None, text = trial.cue, x = 150, y = 150)
    actr.add_text_to_exp_window(None, text = trial.stimulus, 
                                x = trial.stim_x, y = trial.stim_y)

    ## WHERE DO I PUT THIS SO THAT I CAN HAVE AN RCI?????
    # actr.schedule_event_relative(900 + actr.random(200),
    #                             "clear-exp-window",
    #                             params=[window],
    #                             time_in_ms=True)

    # add the time the trial started to the trial information
    trial.start = actr.get_time(run_model)