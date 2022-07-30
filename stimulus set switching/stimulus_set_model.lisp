
(clear-all)

(define-model stimulus_set
    
(sgp 
:v t 
:esc t 
:lf 0.4 
:bll 0.5 
:egs 0.2 ; adds noise to production utilities
:ans 0.5 
:rt 0 
:ncnar nil
)

(sgp :show-focus t)

(chunk-type goal state attend-cue encode-cue attend-stim encode-stim)
(chunk-type task-representation cue-id cue-col r-set s-set)

(add-dm
 (goal isa goal)
 (attend-cue) (encode-cue) (encode-elements) (encode-rs) (encode-ss) 
 (attend-stim) (encode-stim))

;;(set-visloc-default screen-x lowest)


;;-----------------------------------------------------------------------------
; productions

; find the cue
(P find-cue
    =goal>
        isa         goal
        state       nil
    =visual-location>
==>
    +visual-location>
        screen-y    lowest
    =goal>
        state       attend-cue
)

; move attention to the cue
(P attend-cue
    =goal>
        isa         goal
        state       attend-cue
    =visual-location>
    ?visual>
        state       free
==>
    +visual>
        cmd         move-attention
        screen-pos  =visual-location
    =goal>
        state       encode-cue
)

(P encode-cue
    =goal>
        isa         goal
        state       encode-cue
    =visual>
        isa         visual-object
        value       =value
        color       =color
    ?imaginal>
        buffer      empty
        state       free
==>
    =goal>
        state       encode-elements
    =imaginal>
        isa         task-representation
        cue-id      =value
        cue-col     =color
)


; encode the response set
(P encode-rs
    =goal>  
        isa         goal
        state       encode-elements
    =imaginal>
        isa         task-representation
        cue-id      =value
        cue-col     =color
        r-set      nil
==>
    =goal>
        state       attend-rs
)

; encode the stimulus set
(P encode-ss
    =goal>  
        isa         goal
        state       encode-elements
    =imaginal>
        isa         task-representation
        cue-id      =value
        cue-col     =color
        s-set      nil
==>
    =goal>
        state       attend-ss
)

; TODO: Note that it's important that the above two productions match on their left hand side.
;       This means that they will compete for selection during the conflict resolution, meaning
;       the order of encoding of response set and stimulus set information is random



(set-all-base-levels 100000 -1000)
(goal-focus goal)
)
