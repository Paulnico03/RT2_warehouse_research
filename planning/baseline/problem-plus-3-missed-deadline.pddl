(define (problem continuous-delivery-missed-deadline)
    (:domain warehouse-continuous-robot)
    (:objects 
        robby - robot
        pkg1 - package
        dock aisle-A shipping - location
    )
    
    (:init
        (connected dock aisle-A)
        (connected aisle-A dock)
        (connected aisle-A shipping)
        (connected shipping aisle-A)
        
        (= (distance dock aisle-A) 2)
        (= (distance aisle-A dock) 2)
        (= (distance aisle-A shipping) 2)
        (= (distance shipping aisle-A) 2)

        (at-robot robby dock)
        (hand-empty robby)
        (= (distance-left robby) 0)
        
        (at-package pkg1 aisle-A)
        (target-location pkg1 shipping)
        
        
        (= (time-remaining pkg1) 2)
    )
    
    (:goal
        (and
            (delivered pkg1)
            (not (missed-deadline pkg1))
        )
    )
)