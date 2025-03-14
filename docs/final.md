---
layout: default
title: Final Report
---
## Video

## Project Summary
Our project aims to explore and analyze the specific performance task of a robot arm setting a chessboard within the RLBench environment. Our approach involves experimenting with existing algorithms in the RLBench environment, tweaking them to improve their performance, and conducting a comparative study to understand the impact of these modifications. For this project, the input will include task specifications and environmental observations, such as RGB, depth, and segmentation masks, while the output will involve the successful completion of the checkerboard setup task.

To achieve the goals of our project, we added rewards to encourage the robot to prioritize correctly placed pieces and efficiently move toward misplaced pieces. We also have an incremental reward system that continually rewards progress even when full success has not yet occurred.

We used the Proximal Policy Optimization (PPO) to train our robot arm. Through tweaking different train parameters of the ppo model to observe the influences on the train model in order to improve the accuracy and efficiency of the robot arm. Specifically, we mainly change the parameters such as learning_rate, batch_size, clip_range, etc to observe the model.

## Approaches

To tackle the checkerboard setup task, we primarily use PPO as our reinforcement learning baseline. PPO is a model-free policy gradient method that improves sample efficiency by constraining policy updates using a clipped objective function. The loss function is formulated as follows:

$\(L(\theta) = \mathbb{E}_t \left[ \min(r_t(\theta) A_t, \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon) A_t ) \right]\)$

where $r_t(\theta)$ is the probability ratio between the new and old policies, $A_t$ is the advantage function, and  is a small constant (default is 0.2). We set hyperparameters based on OpenAI’s default PPO settings and then adjust them as necessary.

The OpenAI’s default PPO settings:
* Learning rate: 3e-4
* Clip parameter: 0.2
* Number of epochs per update: 10
* Mini-batch size: 64
* Discount factor: 0.99

Then we trained the modal with the learning rate at 1e-3, 3e-3, 1e-2, 1e-4, 3e-5, 1e-5, etc in order to get a better learning rate for our model. We also change the batch size to 128 or 256 to see the effects. We also tweaked the clip range and entropy coefficient for improvements.

Alongside PPO, we integrate Model Predictive Control (MPC) to introduce a model-based planning component. MPC uses a learned dynamics model to predict future states and optimize action sequences accordingly. This helps in cases where pure model-free RL struggles with complex dependencies in the checkerboard setup.

For hierarchical structure, we employ Hierarchical Reinforcement Learning (HRL), breaking down the task into sub-goals such as:

Grasping a piece
Moving it to the correct location
Placing the piece accurately
Each sub-goal is managed by a lower-level policy, while a high-level policy orchestrates overall execution. To improve learning efficiency, we bootstrap training with Imitation Learning (IL) by collecting expert demonstrations and using Behavior Cloning (BC) to pre-train the agent before transitioning to reinforcement learning.

We evaluate our models over 500,000 training steps, analyzing performance in terms of task success rate, execution time, and reward accumulation. Our experiments involve ablations, such as removing hierarchical structures or imitation learning, to measure their individual contributions.
## Evaluation
#### Quantitative Evaluation
The first problem that we meet is the environment setup. For example, we have to use the Ubuntu18_04 version of CoppeliaSim since 20_04 requires GLIBC=2.29 (for pyrep) and Rocky 8.10 Green Obsidian only has GLIBC=2.28. Our remote machine can't git clone for some reason so manually download the compressed repository and then pip install directly. Also, we don't have the privileges to use sudo. After getting help from the TA, we set our environment up successfully. We also build a "[RLBench Setup for HPC3.md](https://github.com/Xiaoli-Catherine/ChessBots/blob/main/RLBench/RLBench%20Setup%20for%20HPC3.md)" for future people to set up the RLBench in HPC3. After the environment setup, we got a test video of the environment test, it was the first success we made in this project. The following picture is the screenshot of the RLBench environment test.

<img width="500" alt="Screenshot 2025-02-21 at 2 30 50 PM" src="https://github.com/user-attachments/assets/5bd61a07-b1fa-4502-841c-78729e3b8e04" />

Screenshot of the output of RLBench environment test

To achieve the project goals, we used PPO as the training model. We trained multiple PPO models and observed the impact of different parameters to obtain a better model. However, we have not gained a satisfying model so far even though we have tried many different parameters.

#### Qualitative Evaluation
We will observe if our modifications in the algorithm improve the system’s adaptability and efficiency, particularly in precision placement and reduced execution time. For now, we just completed the RLBench environment setup. The output shows the RLBench environment works well. Meanwhile, we want to make sure we have to make logical decisions and choices along the way. We make educated guesses about what could work, try it, see the result, and use that to continue making guesses. The key idea here is to make sure that we have learned something during the project.


## References
source code:
- [https://github.com/stepjam/RLBench](https://github.com/stepjam/RLBench)
  
Related source:
-  [ https://peract.github.io/](https://peract.github.io/)

## AI Tool Usage
