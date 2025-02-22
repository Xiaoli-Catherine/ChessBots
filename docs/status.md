---
layout: default
title: Status
---

## Project Summary
Our project aims to explore and analyze the specific performance task of a robot arm setting a chessboard within the RLBench environment. Our approach involves experimenting with existing algorithms in the RLBench environment, tweaking them to improve their performance, and conducting a comparative study to understand the impact of these modifications. For this project, the input will include task specifications and environmental observations, such as RGB, depth, and segmentation masks, while the output will involve the successful completion of the checkerboard setup task. 

## Approach
To tackle the checkerboard setup task, we primarily use Proximal Policy Optimization (PPO) as our reinforcement learning baseline. PPO is a model-free policy gradient method that improves sample efficiency by constraining policy updates using a clipped objective function. The loss function is formulated as follows:

$\(L(\theta) = \mathbb{E}_t \left[ \min(r_t(\theta) A_t, \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon) A_t ) \right]\)$

where $r_t(\theta)$ is the probability ratio between the new and old policies, $A_t$ is the advantage function, and  is a small constant (default is 0.2). We set hyperparameters based on OpenAI’s default PPO settings, adjusting them as necessary:

Learning rate: 3e-4
Clip parameter: 0.2
Number of epochs per update: 10
Mini-batch size: 64
Discount factor: 0.99

Alongside PPO, we integrate Model Predictive Control (MPC) to introduce a model-based planning component. MPC uses a learned dynamics model to predict future states and optimize action sequences accordingly. This helps in cases where pure model-free RL struggles with complex dependencies in the checkerboard setup.

For hierarchical structure, we employ Hierarchical Reinforcement Learning (HRL), breaking down the task into sub-goals such as:

Grasping a piece
Moving it to the correct location
Placing the piece accurately

Each sub-goal is managed by a lower-level policy, while a high-level policy orchestrates overall execution. To improve learning efficiency, we bootstrap training with Imitation Learning (IL) by collecting expert demonstrations and using Behavior Cloning (BC) to pre-train the agent before transitioning to reinforcement learning.

We evaluate our models over 500,000 training steps, analyzing performance in terms of task success rate, execution time, and reward accumulation. Our experiments involve ablations, such as removing hierarchical structures or imitation learning, to measure their individual contributions.

## Evaluation
#### Quantitative Evaluation
Our project aims to get the robot arm to properly set up the checkerboard. The most obvious criterion is that the robot arm be able to set up the checkerboard. We will start by modifying the number of pieces to be set up to create different levels of difficulty. Starting from small pieces, in case we can not complete the task.
If we are able to set up the checkerboard, then the next metric would be the speed at which it is able to do so. Another quantitative metric to use that amalgamates all of the above in a less human-understandable way is just the expected reward of the agent.

#### Qualitative Evaluation
We will observe if our modifications in the algorithm improve the system’s adaptability and efficiency, particularly in precision placement and reduced execution time. For now, we just completed the RLBench environment setup. The output shows the RLBench environment works well. Meanwhile, we want to make sure we have to make logical decisions and choices along the way. We make educated guesses about what could work, try it, see the result, and use that to continue making guesses. The key idea here is to make sure that we have learned something during the project.

<img width="500" alt="Screenshot 2025-02-21 at 2 30 50 PM" src="https://github.com/user-attachments/assets/5bd61a07-b1fa-4502-841c-78729e3b8e04" />

Screenshot of the output of RLBench environment test

## Remaining Goals and Challenges
Goals for the Remainder of the Quarter

Hyperparameter Tuning: We plan to fine-tune PPO parameters to maximize efficiency and stability in training.
Data Augmentation: Expanding our dataset by varying lighting conditions, object orientations, and perturbations to make the policy more robust.
Algorithm Comparisons: We aim to compare PPO with alternative approaches such as Soft Actor-Critic (SAC) and Deep Q-Networks (DQN) to determine the most effective method for this task.
Error Analysis: Conduct failure case studies to identify common errors in checkerboard setup and refine our reward function accordingly.

Challenges Anticipated

Sample Efficiency: RLBench tasks require extensive training, and PPO, despite its efficiency, still demands substantial data. We may explore offline RL or experience replay to enhance learning from limited interactions.
Precision in Placement: The fine motor control needed for checkerboard setup remains challenging. We might incorporate spatial attention mechanisms to improve accuracy.

By the end of the quarter, we aim to have a robust, well-evaluated RL model capable of efficiently solving the checkerboard setup task while also contributing insights into improving RLBench benchmarks.

## Resources Used
source code:
- [https://github.com/stepjam/RLBench](https://github.com/stepjam/RLBench)
  
Related source:
-  [ https://peract.github.io/](https://peract.github.io/)
  
Environment setup:

By using gymnasium and rlbench, we have set up a test RLBench environment that looks like below image

<img width="500" alt="Screenshot 2025-02-21 at 2 30 50 PM" src="https://github.com/user-attachments/assets/5bd61a07-b1fa-4502-841c-78729e3b8e04" />


