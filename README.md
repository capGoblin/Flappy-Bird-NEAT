# Flappy Bird NEAT
This repository contains an implementation of the Flappy Bird game using reinforcement learning (RL) techniques. The goal of the project is to train an RL agent to play Flappy Bird autonomously by learning from its interactions with the game environment. Using the NEAT(NeuroEvolution of Augmenting Topologies) python module. The game was designed using the pygame library while NEAT was implemented using the Python-NEAT package. 

- config.txt has the configuration settings required for NEAT implementation.
- FlappyBird-NEAT.py Implements NEAT algorithm to train the pop_size/birds for every generation(group or population of genomes).
- winner.pkl saves the best performing genome of a bird trained through all the generations.
- FlappyBird-NEAT.py the winner genome is loaded in this code.
- running the FlappyBird-NEAT.py with the requirements installed you can see the trained bird playing Flappy Bird autonomously.(Top Score seen - more than 1674)
- FlappyBird.py Basic pygame. Allows user to play Flappy Bird.

# NEAT Python
Here is the documentation for the genetic module : https://neat-python.readthedocs.io/en/latest/

# Reference
Blog that did a great job of explaining what's happening here : https://medium.com/chris-nielsen/teaching-an-ai-to-play-flappy-bird-f0b18d65569b

# Tutorial
Tim at techwithtim does a great job of teaching all the nitty gritty details of the project. Check it out here : https://www.youtube.com/watch?v=OGHA-elMrxI
