# **Problem Statement**

The primary goal of this project was to build a game using the rules of cellular automata. The project is inspired from the game ‘Noita’ which is marketed as ‘The game in which each pixel is simulated’. The basic concept is that there is a grid of cells (pixels) and each cell updates over time as a function of its neighboring cells. By changing the function we can create different behaviors and complexities can emerge from it.

Goal was to first implement the concept to create various elements (stone, wood, sand, water, fire, lava,steam,oil) and their interactions with each other and then create a game around it. We finalized the game to be a dungeon crawler with various game mechanics which were possible with elements.

**Tech Stack**

Preferable was C++ and OpenGL but due to time constraints we used Python and Pygame.

**What is cellular automata?**

A cellular automaton (CA) is a collection of cells arranged in a grid of specified shape, such that each cell changes state as a function of time, according to a defined set of rules driven by the states of neighboring cells.

**Goals Achieved**



* **The sandbox simulator**

Implementation of grid and cells as elements of grid is complete and can be experienced in the file Simul.py. There are 8 elements in total and their interactions with each other are implemented.



* **Optimization**

Previously the game was running in O(n1*n2) which was bad for maintaining a good framerate for the game. We implemented a chunk based optimization where the world is broken into chunks and specific chunks which are required are updated rather than using the double for loop over all the pixels. Currently it works good but just for some elements (like liquids) it adds a bit of chunky behavior but it can be worked upon.

It is in optimization2.py



* **Player mechanics and collision**

It is not completed and has some bugs. But we were able to implement jumping behavior and some parts of collision. Also the code for player sprite was being worked upon simultaneously.
