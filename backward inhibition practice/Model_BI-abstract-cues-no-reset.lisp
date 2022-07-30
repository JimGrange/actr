;;;;;; Model n-2 back 
;;;;;; Model developed by Ion Juvina based on specifications by Jim Grange 
;;;;;; 2013
;;;;;; 

;;; Abstract cues (the cue-target relation is arbitrary): 
;;; Square cue = shaded target
;;; Actagon cue = angled target
;;; Briangle cue = border target. 
;;; 
;;; this one does cue-target translation through varying sji between cues and targets  
;;; proceduralization 

;;; Changes: 
;;; replaced decaying finsts (Juvina & Taatgen, 2009) with base-level inhibition (Lebiere & Best, 2009)
;;; increase strengths of association with session to model associative learning 
;;; increase retreival threshold with session to model speed-accuracy tradeoff 
     
 
;;; To do: 
;;; add 10ms to the fixed time
;;;
   
(defvar *border-dist* '((AngledStim ShadedStim OvalStim) (AngledStim OvalStim ShadedStim) (OvalStim AngledStim ShadedStim) 
                        (OvalStim ShadedStim AngledStim) (ShadedStim OvalStim AngledStim) (ShadedStim AngledStim OvalStim)))

(defvar *shaded-dist* '((AngledStim BorderStim OvalStim) (AngledStim OvalStim BorderStim) (OvalStim AngledStim BorderStim) 
                        (OvalStim BorderStim AngledStim) (BorderStim OvalStim AngledStim) (BorderStim AngledStim OvalStim)))

(defvar *angled-dist* '((ShadedStim BorderStim OvalStim) (ShadedStim OvalStim BorderStim) (OvalStim ShadedStim BorderStim) 
                        (OvalStim BorderStim ShadedStim) (BorderStim OvalStim ShadedStim) (BorderStim ShadedStim OvalStim)))

(defparameter *response* "w")

(defparameter *last-stim* (+ 1 (random 3)))

(defparameter *load-dir* (make-pathname
                          :directory (pathname-directory *load-truename*))
  "The directory containing this source file at load time.")

(defun random-next (number)
  (let ((res (mod (+ number (+ 1 (random 2))) 3)))
    (if (= res 0) (setf res 3))
    res)
)

(defun select-stim (number)
  (let* ((stim-list nil)
         (border-dist-list (nth (random 6) *border-dist*))
         (border-list (list (list 'BorderStim (nth 0 border-dist-list) (nth 1 border-dist-list) (nth 2 border-dist-list)) 
                            (list (nth 0 border-dist-list) 'BorderStim (nth 1 border-dist-list) (nth 2 border-dist-list))
                            (list (nth 0 border-dist-list) (nth 1 border-dist-list) 'BorderStim (nth 2 border-dist-list)) 
                            (list (nth 0 border-dist-list) (nth 1 border-dist-list) (nth 2 border-dist-list) 'BorderStim)))
         (shaded-dist-list (nth (random 6) *shaded-dist*))
         (shaded-list (list (list 'ShadedStim (nth 0 shaded-dist-list) (nth 1 shaded-dist-list) (nth 2 shaded-dist-list)) 
                            (list (nth 0 shaded-dist-list) 'ShadedStim (nth 1 shaded-dist-list) (nth 2 shaded-dist-list))
                            (list (nth 0 shaded-dist-list) (nth 1 shaded-dist-list) 'ShadedStim (nth 2 shaded-dist-list)) 
                            (list (nth 0 shaded-dist-list) (nth 1 shaded-dist-list) (nth 2 shaded-dist-list) 'ShadedStim)))
         (angled-dist-list (nth (random 6) *angled-dist*))
         (angled-list (list (list 'AngledStim (nth 0 angled-dist-list) (nth 1 angled-dist-list) (nth 2 angled-dist-list)) 
                            (list (nth 0 angled-dist-list) 'AngledStim (nth 1 angled-dist-list) (nth 2 angled-dist-list))
                            (list (nth 0 angled-dist-list) (nth 1 angled-dist-list) 'AngledStim (nth 2 angled-dist-list)) 
                            (list (nth 0 angled-dist-list) (nth 1 angled-dist-list) (nth 2 angled-dist-list) 'AngledStim))))
    (if (= number 3) (setf stim-list (nth (random 4) angled-list))
      (if (= number 2) (setf stim-list (nth (random 4) border-list))
        (setf stim-list (nth (random 4) shaded-list))))
    stim-list))

(defun display-cue (cue)
  (add-text-to-exp-window :text cue :x 100 :y 100 :color 'black)
  (proc-display)
)

(defun display-stimuli (stim-list)
  (add-text-to-exp-window :text (string (first stim-list)) :x 40 :y 50 :color 'black)
  (add-text-to-exp-window :text (string (second stim-list)) :x 150 :y 50 :color 'black)
  (add-text-to-exp-window :text (string (third stim-list)) :x 50 :y 150 :color 'black)
  (add-text-to-exp-window :text (string (fourth stim-list)) :x 150 :y 150 :color 'black)
  (proc-display))

(defun do-trial ()
  (let* ((current-stim (random-next *last-stim*))
         (cue (if (= current-stim 3) "Actagon" (if (= current-stim 2) "Briangle" "Square")))
         (stim-list (select-stim current-stim))
         (RT 0)
         (start-time -1))
    (let* ((window (open-exp-window "N-2Back" :visible nil)))           ;;; change :visible to t to see the experiment window
      (install-device window)
      (display-cue cue)
      (schedule-event-relative 0.5 'clear-exp-window)
      (run-full-time 0.750 :real-time nil)
      (display-stimuli stim-list)
      (setf start-time (get-time))
      (schedule-break-after-module ':motor) 
      (run 5 :real-time nil)
      (setf RT (+ 100 (- (get-time) start-time)))
      (clear-exp-window)
      (run-full-time 0.600 :real-time nil)                             ;;; 0.100 motor movement (was 300) plus 0.5 ISI
      )
    (setf *last-stim* current-stim)
;    (cond
;     ((and (equal (subseq Cue 0 1) (subseq (string (nth 0 stim-list)) 0 1)) (equal *response* "D")) (trigger-reward 1))
;     ((and (equal (subseq Cue 0 1) (subseq (string (nth 1 stim-list)) 0 1)) (equal *response* "J")) (trigger-reward 1))
;     ((and (equal (subseq Cue 0 1) (subseq (string (nth 2 stim-list)) 0 1)) (equal *response* "C")) (trigger-reward 1))
;     ((and (equal (subseq Cue 0 1) (subseq (string (nth 3 stim-list)) 0 1)) (equal *response* "N")) (trigger-reward 1))
;     (t (trigger-reward -10)))
    (list *response* RT cue stim-list))
)

(defun do-block (subj-no session-no block-no no-of-trials)                        ;;; no-of-trials is 42
  (loop for i from 1 to no-of-trials do 
        (let ((res (do-trial))
              (path nil))
          (setq path (merge-pathnames "n2back15-scale14.txt" *load-dir*))
          (with-open-file (s path :direction :output :if-exists :append)
            (format s "~6,1F ~6,1F ~6,1F ~6,1F ~A ~6,1F ~6,1F ~6,1F ~6,1F ~6,1F ~6,1F ~%" subj-no session-no block-no i (nth 0 res) (nth 1 res) (nth 2 res) (nth 0 (nth 3 res)) (nth 1 (nth 3 res)) (nth 2 (nth 3 res)) (nth 3 (nth 3 res)))))))

(defun do-subject (subj-no no-of-sessions no-of-blocks no-of-trials)                  ;;; no-of-blocks is 10
  (reset)
  (loop for i from 1 to no-of-sessions do 
    (cond 
     ((= i 1) (add-sji-fct '((actagon angledstim 0.05)(briangle borderstim 0.05)(square shadedstim 0.05))))
     ((= i 2) (add-sji-fct '((actagon angledstim 0.25)(briangle borderstim 0.25)(square shadedstim 0.25))))
     ((= i 3) (add-sji-fct '((actagon angledstim 0.60)(briangle borderstim 0.60)(square shadedstim 0.60))))
     ((= i 4) (add-sji-fct '((actagon angledstim 1.20)(briangle borderstim 1.20)(square shadedstim 1.20))))
     ((= i 5) (add-sji-fct '((actagon angledstim 2.00)(briangle borderstim 2.00)(square shadedstim 2.00)))))
    (cond 
     ((= i 1) (sgp-fct (list :ans 0.50)))
     ((= i 2) (sgp-fct (list :ans 0.35)))
     ((= i 3) (sgp-fct (list :ans 0.25)))
     ((= i 4) (sgp-fct (list :ans 0.15)))
     ((= i 5) (sgp-fct (list :ans 0.05))))
    (loop for j from 1 to no-of-blocks do 
      (do-block subj-no i j no-of-trials)
      (format t "~A" i))))

(defun do-exp (no-of-subj no-of-sessions no-of-blocks no-of-trials)                   ;;; 100 10 42   ;;; learning study 1 5 10 122
  (let ((p (merge-pathnames "n2back15-scale14.txt" *load-dir*)))
    (with-open-file (s p :direction :output :if-exists :supersede)
      (format s "~6,1F ~6,1F ~6,1F ~6,1F ~A ~6,1F ~6,1F ~6,1F ~6,1F ~6,1F ~6,1F ~%" "Subject" "Session" "Block" "Trial" "Response" "RT" "Cue" "TopLeft" "TopRight" "BottomLeft" "BottomRight")))
  (dotimes (k no-of-subj)  
    (do-subject (+ k 1) no-of-sessions no-of-blocks no-of-trials)
    (format t "~6,1F ~%" (+ k 1))))

(clear-all)

(define-model n-2back

(sgp :esc t :trace-detail low :v nil :pct t
:ACT nil
:lf                        0.7 ;   was 0.4
:bll                       0.5 ;   was 0.5 
;:ans                      0.25 ; 
:rt                       -2.6 ;   was -0.6  
:MAS                         4 ;   default: NIL        : Maximum Associative Strength
:GA                        2.5 ;   default: 1          : source spread for the GOAL buffer
:VISUAL-ATTENTION-LATENCY 0.03 ;   default: 0.085      : Time for a shift of visual attention
:MOTOR-INITIATION-TIME   0.001 ;   default: 0.05       : Time to initiate a motor movement.
:MOTOR-BURST-TIME        0.001 ;   default: 0.05       : Minimum time for any movement.
:INHIBITION-DECAY          1.1 ;   was 1.1 default: 1.0        : Base-level inhibition decay (ds)
:ENABLE-INHIBITION           t ;   default: T          : Enable base-level inhibition calculation : make it nil for the no-inhibiton model
:INHIBITION-SCALE           14 ;   was 9.0 default: 5          : Base-level inhibition scale (ts) : make it 7.0 for the inhibition model 
:ol                        nil ;   default: t 
:egs                       0.2 ;   was 0.2
:alpha                    0.01 ;   was 0.2
:epl                       nil
:ul                        nil
:tt                       0.07 ;   default: 2.0        : Threshold time
)

(chunk-type find-target cue target state)
(chunk-type cue name)
(chunk-type target name cue)

(add-dm (attend isa chunk))
(add-dm (start isa chunk))
(add-dm (encode isa chunk))
(add-dm (retrieve-word isa chunk))
(add-dm (retrieve-meaning isa chunk))
(add-dm (retrieve-target isa chunk))
(add-dm (re-retrieve isa chunk))
(add-dm (attend-target isa chunk))
(add-dm (attend-target-location isa chunk))
(add-dm (attend-target-tl isa chunk))
(add-dm (attend-target-tl1 isa chunk))
(add-dm (respond-tl isa chunk))
(add-dm (respond-tr isa chunk))
(add-dm (respond-bl isa chunk))
(add-dm (respond-br isa chunk))

(add-dm (actagon isa cue name "Actagon"))
(add-dm (briangle isa cue name "Briangle"))
(add-dm (square isa cue name "Square"))

(add-dm (angledstim isa target name "ANGLEDSTIM" cue actagon))
(add-dm (borderstim isa target name "BORDERSTIM" cue briangle))
(add-dm (shadedstim isa target name "SHADEDSTIM" cue square))

(add-dm (goal isa find-target state attend))

; (add-sji (actagon angledstim 0.25)(briangle borderstim 0.25)(square shadedstim 0.25))   ; this is meant to model how strong the association between cue and target is 

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; attend cue ;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(P attend-cue-location
   =goal>
      ISA         find-target
      state       attend
   =visual-location>
      ISA         visual-location
   ?visual-location>
      state       free
==>
   +visual-location>
      ISA         visual-location
      > screen-x  60
      < screen-x  140
      > screen-y  60
      < screen-y  140
   =goal>
      state       start
)

(P attend-cue
   =goal>
      ISA         find-target
      cue         nil
      state       start
   =visual-location>
      ISA         visual-location
   ?visual>
      state       free
==>
   +visual>
      ISA         move-attention
      screen-pos  =visual-location
   =goal>
      state       encode
)

;;; this is the encoding of the cue in the goal ;;;;;;;;;;;;;;;;;;;;; encoding ;;;;;;;;;;;;;;;;;;;;;;;;;;;

(P encode-actagon-cue-in-goal  
   =goal>
      ISA         find-target
      state       encode
   =visual>
      isa         text
      value       "Actagon"
==>
   =goal>
      cue         actagon
      state       retrieve-target)

(P encode-briangle-cue-in-goal  
   =goal>
      ISA         find-target
      state       encode
   =visual>
      isa         text
      value       "Briangle"
==>
   =goal>
      cue         briangle
      state       retrieve-target)

(P encode-square-cue-in-goal  
   =goal>
      ISA         find-target
      state       encode
   =visual>
      isa         text
      value       "Square"
==>
   =goal>
      cue         square
      state       retrieve-target)

;;; here it attempts to retrive the target  ;;;;;;;;;;;;;;;;;;;;; retrieve target associated with meaning ;;;;;;;;;;;;;;;;;;;;;;;;;;;

(P retrieve-target 
   =goal>
      ISA         find-target
      cue         =cue
      target      nil
      state       retrieve-target
   =visual-location>
      ISA         visual-location
   ?retrieval>
      state       free
==>
   +retrieval> 
      isa         target
      cue         =cue
   =goal>
      state       attend-target-tl)

(P found-target 
   =goal>
      ISA         find-target
      cue         =cue
      target      nil
      state       attend-target-tl
   =retrieval> 
      isa         target
      name        =name
      cue         =cue
   ?imaginal>
      state       free
==>
   +imaginal> 
      isa         target
      name        =name
      cue         =cue
   =goal>
      cue         nil)

;;;;; when retrieval fails, respond randomly and possibly make error

(P failure-to-retrieve-target   
   =goal>
      ISA         find-target
      cue         =cue
      target      nil
      state       attend-target-tl
   ?retrieval>
      state       error
==>
   =goal>
      cue         nil
      state       respond-br
)

;;; here it starts looking for the target on the screen ;;;;;;;;;;;;;;;;;;;;

(P attend-target-location
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       attend-target-tl
   ?visual-location>
      state       free
==>
   +visual-location>
      ISA         visual-location
      > screen-x  10
      < screen-x  90
      > screen-y  10
      < screen-y  90
   =goal>
      state       attend-target-tl1
)

(P attend-target-tl
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       attend-target-tl1
   =visual-location>
      ISA         visual-location
      > screen-x  10
      < screen-x  90
      > screen-y  10
      < screen-y  90
   ?visual>
      state       free
   ?visual-location>
      state       free
   ?retrieval>
      state       free
==>
   +visual>
      ISA         move-attention
      screen-pos  =visual-location
   +visual-location>
      ISA         visual-location
      > screen-x  110
      < screen-x  190
      > screen-y  10
      < screen-y  90
   =goal>
      state       respond-tl
)

(P attend-target-tr
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-tl
   =visual-location>
      ISA         visual-location
      > screen-x  110
      < screen-x  190
      > screen-y  10
      < screen-y  90
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
    - name        =target
   ?visual>
      state       free
   ?visual-location>
      state       free
==>
   =imaginal>
   +visual>
      ISA         move-attention
      screen-pos  =visual-location
   +visual-location>
      ISA         visual-location
      > screen-x  10
      < screen-x  90
      > screen-y  110
      < screen-y  190
   =goal>
      state       respond-tr
)

(P attend-target-bl
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-tr
   =visual-location>
      ISA         visual-location
      > screen-x  10
      < screen-x  90
      > screen-y  110
      < screen-y  190
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
    - name        =target
   ?visual>
      state       free
   ?visual-location>
      state       free
==>
   =imaginal>
   +visual>
      ISA         move-attention
      screen-pos  =visual-location
   +visual-location>
      ISA         visual-location
      > screen-x  110
      < screen-x  190
      > screen-y  110
      < screen-y  190
   =goal>
      state       respond-bl
)

(P attend-target-br
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-bl
   =visual-location>
      ISA         visual-location
      > screen-x  110
      < screen-x  190
      > screen-y  110
      < screen-y  190
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
    - name        =target
   ?visual>
      state       free
==>
   =imaginal>
   +visual>
      ISA         move-attention
      screen-pos  =visual-location
   =goal>
      state       respond-br
)

;;; here the model responds  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; response ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(P respond-tl
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-tl
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
      name        =target
   ?manual>
      state       free
==>
   +manual>              
     isa          press-key     
     key          "D"
   -visual-location>
   =goal>
      cue         nil
      target      nil
      state       attend
!eval! (setf *response* "D")
)

(P respond-tr
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-tr
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
      name        =target
   ?manual>
      state       free
==>
   +manual>              
     isa          press-key     
     key          "J"
   -visual-location>
   =goal>
      cue         nil
      target      nil
      state       attend
!eval! (setf *response* "J")
)

(P respond-bl
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-bl
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
      name        =target
   ?manual>
      state       free
==>
   +manual>              
     isa          press-key     
     key          "C"
   -visual-location>
   =goal>
      cue         nil
      target      nil
      state       attend
!eval! (setf *response* "C")
)

(P respond-br
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-br
   =visual>
      isa         text
      value       =target
   =imaginal>
      isa         target
      name        =target
   ?manual>
      state       free
==>
   +manual>              
     isa          press-key     
     key          "N"
   -visual-location>
   =goal>
      cue         nil
      target      nil
      state       attend
!eval! (setf *response* "N")
)

(P respond-randomly
   =goal>
      ISA         find-target
      cue         nil
      target      nil
      state       respond-br
   ?retrieval>
      buffer      empty
   ?imaginal>
      buffer      empty
   ?manual>
      state       free
   !bind! =key (nth (random 4) '("D" "J" "C" "N"))
==>
   +manual>              
     isa          press-key     
     key          =key
   -visual-location>
   =goal>
      cue         nil
      target      nil
      state       attend
!eval! (setf *response* =key)
)

(spp :u 100)
(sgp :nu 0)
(spp (respond-tl :u 100 :at 0.01))
(spp (respond-tr :u 100 :at 0.01))
(spp (respond-bl :u 100 :at 0.01))
(spp (respond-br :u 100 :at 0.01))

(spp (attend-target-location :at 0.001))
(spp (attend-target-tl :at 0.001))
(spp (attend-target-tr :at 0.001))
(spp (attend-target-bl :at 0.001))
(spp (attend-target-br :at 0.001))

(spp (failure-to-retrieve-target :at 0.001))
(spp (respond-randomly :at 0.001))

(goal-focus goal))


