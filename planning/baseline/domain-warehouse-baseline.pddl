(define (domain warehouse-continuous-robot)
    (:requirements :strips :typing :numeric-fluents :continuous-effects :negative-preconditions)
    (:types robot package location)

    (:predicates
        (at-robot ?r - robot ?l - location)
        (at-package ?p - package ?l - location)
        (connected ?l1 - location ?l2 - location)
        (holding ?r - robot ?p - package)
        (hand-empty ?r - robot)
        
        (is-moving ?r - robot)
        (departed-from ?r - robot ?l - location)
        (moving-to ?r - robot ?l - location)
        
        (target-location ?p - package ?l - location)
        (delivered ?p - package)
        (missed-deadline ?p - package)
    )

    (:functions
        (distance-left ?r - robot)
        (distance ?l1 - location ?l2 - location)
        (time-remaining ?p - package)
    )

    ;; ===================================================
    ;; CONTINUOUS PROCESSES (Counting Down to Zero)
    ;; ===================================================

    (:process robot-transit
        :parameters (?r - robot)
        ;; The distance shrinks as long as it's greater than 0
        :precondition (and (is-moving ?r) (> (distance-left ?r) 0))
        :effect (decrease (distance-left ?r) (* #t 1))
    )

    (:process package-aging
        :parameters (?p - package)
        ;; The package loses time as long as it isn't delivered
        :precondition (and (not (delivered ?p)) (> (time-remaining ?p) 0))
        :effect (decrease (time-remaining ?p) (* #t 1))
    )

    ;; ===================================================
    ;; EVENTS (Automatic System Triggers)
    ;; ===================================================

    (:event deadline-breach
        :parameters (?p - package)
        ;; Triggers the exact moment the countdown hits 0
        :precondition (and 
            (not (delivered ?p))
            (<= (time-remaining ?p) 0)
            (not (missed-deadline ?p)) ; <-- THE MAGIC FIX! Stops the infinite loop.
        )
        :effect (missed-deadline ?p)
    )

    ;; ===================================================
    ;; ACTIONS
    ;; ===================================================

    (:action start-move
        :parameters (?r - robot ?from - location ?to - location)
        :precondition (and 
            (at-robot ?r ?from)
            (connected ?from ?to)
            (not (is-moving ?r))
        )
        :effect (and 
            (not (at-robot ?r ?from))
            (is-moving ?r)
            (departed-from ?r ?from)
            (moving-to ?r ?to)
            (assign (distance-left ?r) (distance ?from ?to)) ; Load the distance
        )
    )

    (:action end-move
        :parameters (?r - robot ?from - location ?to - location)
        :precondition (and 
            (is-moving ?r)
            (departed-from ?r ?from)
            (moving-to ?r ?to)
            (<= (distance-left ?r) 0) ; Arrive when countdown is 0
        )
        :effect (and 
            (not (is-moving ?r))
            (not (departed-from ?r ?from))
            (not (moving-to ?r ?to))
            (at-robot ?r ?to)
            (assign (distance-left ?r) 0)
        )
    )

    (:action pick
        :parameters (?r - robot ?p - package ?l - location)
        :precondition (and 
            (at-robot ?r ?l)
            (at-package ?p ?l)
            (hand-empty ?r)
        )
        :effect (and 
            (not (at-package ?p ?l))
            (not (hand-empty ?r))
            (holding ?r ?p)
        )
    )

    (:action drop-intermediate
        :parameters (?r - robot ?p - package ?l - location)
        :precondition (and 
            (at-robot ?r ?l)
            (holding ?r ?p)
        )
        :effect (and 
            (not (holding ?r ?p))
            (hand-empty ?r)
            (at-package ?p ?l)
        )
    )

    (:action deliver-package
        :parameters (?r - robot ?p - package ?l - location)
        :precondition (and 
            (at-robot ?r ?l)
            (holding ?r ?p)
            (target-location ?p ?l)
            (not (missed-deadline ?p)) ; Cannot deliver if it's too late!
        )
        :effect (and 
            (not (holding ?r ?p))
            (hand-empty ?r)
            (at-package ?p ?l)
            (delivered ?p)
        )
    )
)