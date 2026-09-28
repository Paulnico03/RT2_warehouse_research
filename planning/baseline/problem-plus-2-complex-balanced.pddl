(define (problem continuous-delivery-complex-balanced)
    (:domain warehouse-continuous-robot)
    (:objects 
        robby - robot
        pkg1 pkg2 pkg3 - package
        dock aisle-A aisle-B shipping - location
    )
    
    (:init
        ;; Graph Topology (Two-way paths)
        (connected dock aisle-A)
        (connected aisle-A dock)
        (connected dock aisle-B)
        (connected aisle-B dock)
        (connected aisle-A shipping)
        (connected shipping aisle-A)
        (connected aisle-B shipping)
        (connected shipping aisle-B)
        
        ;; Scaled-down distances to keep h(I) low and manageable
        (= (distance dock aisle-A) 2)
        (= (distance aisle-A dock) 2)
        (= (distance dock aisle-B) 3)
        (= (distance aisle-B dock) 3)
        (= (distance aisle-A shipping) 2)
        (= (distance shipping aisle-A) 2)
        (= (distance aisle-B shipping) 3)
        (= (distance shipping aisle-B) 3)

        ;; Initial Robot State
        (at-robot robby dock)
        (hand-empty robby)
        (= (distance-left robby) 0)
        
        ;; Sequential, generous deadlines to clear the heuristic bottleneck
        (at-package pkg1 aisle-A)
        (target-location pkg1 shipping)
        (= (time-remaining pkg1) 30) 
        
        (at-package pkg2 aisle-A)
        (target-location pkg2 shipping)
        (= (time-remaining pkg2) 45)
        
        (at-package pkg3 aisle-B)
        (target-location pkg3 shipping)
        (= (time-remaining pkg3) 60)
    )
    
    (:goal
        (and
            ;; All packages must be successfully delivered within their windows
            (delivered pkg1)
            (delivered pkg2)
            (delivered pkg3)
        )
    )
)