Bouncing Robot Game Requirement Doc
-----------------------------------

How to win the game:

- get robot from start region to goal region
- get robot to colored/numbered regions in order
- get all robots into the same region (aggregation) or into specific goals (sorting)
- cover whole space (with different sensor models)

Interaction with game:

- design finite state machine which controls bounce angle
    - FSM with counter (for expressivity: bounce at angle A n times)
    - deterministic or nondeterministic?
- graphical or programmatic? or both?
- visualize resulting trajectory during program design?
    - can slide single point around polygon and rotate heading
    - can run entire program from any point at any time
- points scale with conciseness of program, success rate

Progression:

- harder levels introduce more error into bounces, narrower passages
- single robot, or multiple robots, or single/multi robots starting from random
  points in regions
- can place one polygon in interior and modify its shape (or select from a few
  shapes)
