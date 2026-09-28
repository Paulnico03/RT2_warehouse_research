(define (problem warehouse-s1152-capacity1)
    (:domain warehouse-continuous-robot)
    (:objects
        robby - robot
        pkg1 pkg2 pkg3 - package
        dock aisle-A aisle-B shipping - location
    )

    (:init
        ;; Graph topology
        (connected dock aisle-A)
        (connected aisle-A dock)
        (connected dock aisle-B)
        (connected aisle-B dock)
        (connected aisle-A shipping)
        (connected shipping aisle-A)
        (connected aisle-B shipping)
        (connected shipping aisle-B)

        ;; Distances
        (= (distance dock aisle-A) 2)
        (= (distance aisle-A dock) 2)
        (= (distance dock aisle-B) 3)
        (= (distance aisle-B dock) 3)
        (= (distance aisle-A shipping) 2)
        (= (distance shipping aisle-A) 2)
        (= (distance aisle-B shipping) 3)
        (= (distance shipping aisle-B) 3)

        ;; Initial robot state
        (at-robot robby dock)
        (= (distance-left robby) 0)
        (= (current-load robby) 0)
        (= (max-capacity robby) 1)

        ;; Package states and deadlines
        (at-package pkg1 aisle-A)
        (target-location pkg1 shipping)
        (= (time-remaining pkg1) 14)

        (at-package pkg2 aisle-B)
        (target-location pkg2 shipping)
        (= (time-remaining pkg2) 13)

        (at-package pkg3 aisle-A)
        (target-location pkg3 shipping)
        (= (time-remaining pkg3) 12)

    )

    (:goal
        (and
            (delivered pkg1)
            (delivered pkg2)
            (delivered pkg3)
        )
    )
)
