---
layout: default
title: Proposal
---

## Summary of the Project:

The goal of our project is to explore and analyze the performance of various algorithms within RLBench, focusing on a specific task where the robot must set up a checkerboard. RLBench is a large-scale benchmark and learning environment featuring 100 unique, hand-designed tasks designed for vision-guided robotic manipulation. For this project, the input will include task specifications and environmental observations, such as RGB, depth, and segmentation masks, while the output will involve the successful completion of the checkerboard setup task. Our approach involves experimenting with existing algorithms in the RLBench environment, tweaking them to improve their performance, and conducting a comparative study to understand the impact of these modifications. This project emphasizes learning from existing algorithms and making informed choices, such as selecting specific algorithms and explaining their relevance. The insights gained from this project can contribute to advancing robotic manipulation research, particularly in vision-guided tasks and algorithmic improvements.

## AI/ML Algorithms:

In this project, we use algorithms such as model-free, model-based, hierarchical RL, and imitation learning. Specifically, we start with Proximal Policy Optimization (PPO) as a baseline model-free RL algorithm to establish a foundational policy. Concurrently, we use Model Predictive Control (MPC) to plan actions by leveraging a predictive dynamics model of the environment. We bootstrap the learning process using imitation learning and employ hierarchical RL to divide the task into subgoals if needed.

## Evaluation Plan:

#### Quantitative Evaluation

Consider the first task of getting the robot arm to properly set up the checkerboard. The most obvious criteria is that the robot arm should actually be able to properly set up the checkerboard. To make this less discrete by not being binary, our metric could be the average number of pieces it is able to place. This would take care of the event that we aren't able to complete the task. If we are able to set up the checkerboard, then the next metric would be the speed at which it is able to do so. Another quantitative metric to use that amalgamates all of the above in a less human understandable way is just the expected reward of the agent.

I expect we should be able to master the checkerboard setting task. I think we may struggle a bit with the chessboard setting task afterward.

#### Qualitative Evaluation

More subjective metrics that are important are of course the humans training the model itself! We want to make sure we have to make logical decision and choices along the way. In other words, make educated guesses about what could work, try it, see the result, and use that to continue making guesses (wow a meta RL algo?). I think the key ideal here is making sure we learn and aren't just copy pasting mindlessly. This is hard to measure, but since we are naturally curious, if we are having fun along the way that means we are answering those questions through true understanding. "Have fun" could be more than a cliche but a metric in this case!
