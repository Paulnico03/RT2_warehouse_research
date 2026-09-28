(define (problem continuous-delivery-simple)
    (:domain warehouse-continuous-robot)
    (:objects 
        robby - robot
        pkg1 - package
        dock aisle-A shipping - location
    )
    
    (:init
        ;; Simplified Graph Topology
        (connected dock aisle-A)
        (connected aisle-A dock)
        (connected aisle-A shipping)
        (connected shipping aisle-A)
        
        ;; Micro-Distances to crush the branching factor
        (= (distance dock aisle-A) 1)
        (= (distance aisle-A dock) 1)
        (= (distance aisle-A shipping) 1)
        (= (distance shipping aisle-A) 1)

        ;; Initial Robot State
        (at-robot robby dock)
        (hand-empty robby)
        (= (distance-left robby) 0)
        
        ;; Single Package State & Deadline
        (at-package pkg1 aisle-A)
        (target-location pkg1 shipping)
        (= (time-remaining pkg1) 10) 
    )
    
    (:goal
        (and
            (delivered pkg1)
        )
    )
)