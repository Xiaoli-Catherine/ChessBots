# ChessBots
# CS 175: Projectin AI


# RLBench Setup for HPC3
Overview
We translate the following github commands to be HPC3 compatible.
https://github.com/stepjam/RLBench/tree/master?tab=readme-ov-
file#install
1. We have to use the Ubuntu18_04 version of CoppeliaSim since 20_04
requires GLIBC=2.29 (for pyrep) and Rocky 8.10 Green Obsidian only
has GLIBC=2.28.
2. Our remote machine can't git clone for some reason so manually
download the compressed repository and then pip install directly.
3. Run headless by starting an xvfb server similar to x server from
1. https://github.com/stepjam/PyRep?tab=readme-ov-file#running-
headless
For the details of setting up the environment please look at 
