
(clear-all)

(define-model episodic
    
(sgp :v nil :esc t :lf 0.4 :bll 0.5 :ans 0.5 :rt 0 :ncnar nil)

(sgp :show-focus t)

(chunk-type problem arg1 arg2 result)
(chunk-type goal state count target next-let next-num)
(chunk-type number number next visual-rep vocal-rep)
(chunk-type letter letter next visual-rep vocal-rep)

(add-dm
 (goal isa goal)
 (attending) (read) (count) (counting) (encode))

(set-visloc-default screen-x lowest)

(set-all-base-levels 100000 -1000)
(goal-focus goal)
)
