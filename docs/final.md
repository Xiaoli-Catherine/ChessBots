---
layout: default
title: Final Report
---
## Video

## Project Summary
Our project aims to explore and analyze the specific performance task of a robot arm setting a checkerboard within the RLBench environment. Our approach involves experimenting with existing algorithms in the RLBench environment, tweaking them to improve their performance, and conducting a comparative study to understand the impact of these modifications. For this project, the input will include task specifications and environmental observations, such as RGB, depth, and segmentation masks, while the output will involve the successful completion of the checkerboard setup task.

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

Our project aims to optimize PPO-based reinforcement learning for a robotic arm setup of a checkerboard using RLBench. We conducted hyperparameter tuning and analyzed training performance through various metrics, including mean episode reward, training stability, and hyperparameter sensitivity.

1. Hyperparameter Tuning & Impact Analysis
   
We experimented with learning rate, clip range, and entropy coefficient to assess their impact on performance. The top 18 configurations ranked by mean reward are summarized in the table below:

<img width="500" alt="Screenshot 2025-03-19 at 12 14 29 PM" src="https://github.com/user-attachments/assets/b8ae0476-9da6-4fd2-96cb-c566bb95fd9f" />

From the picture, we observed:

* The best-performing configuration used a learning rate of 3.0e-05, a clip range of 0.30, and an entropy coefficient of 0.030, achieving a mean reward of -6.47.
* Increasing the clip range to 0.30 tended to improve results, indicating better gradient stability.
* Lower entropy coefficients (0.003) generally resulted in poorer performance, suggesting insufficient exploration.

<img width="500" alt="Screenshot 2025-03-19 at 12 10 09 PM" src="https://github.com/user-attachments/assets/1b7a7f5e-433c-4bf7-8127-ede3f89c95e6" />

<img width="500" alt="Screenshot 2025-03-19 at 12 10 22 PM" src="https://github.com/user-attachments/assets/3e6c555c-eaae-4222-9df2-da8aa5481faf" />

<img width="500" alt="Screenshot 2025-03-19 at 12 10 31 PM" src="https://github.com/user-attachments/assets/a2e906be-711d-4df4-8051-ea4e68e54d2e" />

<img width="500" alt="Screenshot 2025-03-19 at 12 11 02 PM" src="https://github.com/user-attachments/assets/12ee1dbb-723d-41c4-9fb9-ae5c74b374b8" />

#### Qualitative Evaluation
Our project focuses on using RLBench to train a robot arm for setting up a checkerbot. Throughout the development process, we encountered several challenges, made key observations, and refined our approach based on qualitative insights.

1. Environment Setup & Initial Breakthroughs
   
The first major hurdle was setting up the environment on HPC3. First, we lacked sudo privileges, so we could not follow the official installation guide. Due to system constraints, we had to use Ubuntu 18.04 instead of 20.04, as RLBench’s dependencies required GLIBC 2.29, which was not available on Rocky 8.10 (limited to GLIBC 2.28). Additionally, the remote machine had cloning restrictions, forcing us to manually download and install dependencies. Fortunately, we ultimately succeeded with guidance from the TA.

To assist future users, we documented the setup process in "[RLBench Setup for HPC3.md](https://github.com/Xiaoli-Catherine/ChessBots/blob/main/RLBench/RLBench%20Setup%20for%20HPC3.md)", which serves as a detailed guide to configuring RLBench on HPC3 efficiently. Once the environment was fully operational, we successfully ran a test video, validating our setup and marking our first tangible success. The following picture is the screenshot of the RLBench environment test.

<img width="500" alt="Screenshot 2025-02-21 at 2 30 50 PM" src="https://github.com/user-attachments/assets/5bd61a07-b1fa-4502-841c-78729e3b8e04" />

Screenshot of the output of RLBench environment test

2. Training Experience & Observations
   
We selected Proximal Policy Optimization (PPO) as our reinforcement learning model. During training, we experimented with various hyperparameters, observing their effects on performance. While we expected PPO to gradually refine its actions, early results were inconsistent, with the robot arm struggling to complete the task reliably.

Key qualitative observations included:

* Exploration vs. Exploitation Tradeoff: Initial policies led to erratic movements, suggesting inadequate exploration. Adjusting entropy and reward shaping helped improve behavior.
* Task Complexity: The checkerbot setup requires precise control, making it a challenging RLBench task. The robot often struggled with fine motor control, indicating the need for better reward shaping or additional auxiliary tasks.
* Impact of Environment Variability: Minor variations in simulation conditions significantly impacted training consistency. We considered using domain randomization to enhance robustness.
  
3. Challenges & Lessons Learned
   
One of the main challenges was achieving stable and meaningful learning progress. Despite multiple training attempts, we have yet to develop a fully functional model that reliably completes the task. However, this process has provided valuable lessons:

Hyperparameter tuning is non-trivial, and small adjustments can lead to drastically different learning behaviors.
Reinforcement learning for robotic control is highly sensitive to reward shaping and environment design, emphasizing the need for careful engineering of learning conditions.

4. Future Improvements & Next Steps
   
To further enhance model performance, we plan to:

* Try alternative RL algorithms such as Soft Actor-Critic (SAC) or hybrid approaches to improve stability.
* Implement curriculum learning by progressively increasing task complexity.
* Enhance reward shaping to provide better feedback and accelerate learning.
* Although we have not yet achieved a perfect solution, our current progress lays a solid foundation for further improvements, and we remain optimistic about refining the model.

The following image is the screenshot from our training video

<img width="491" alt="Screenshot 2025-03-14 at 2 59 48 PM" src="https://github.com/user-attachments/assets/2abc0409-54ec-4889-9666-658d47772a0c" />


## References
source code:
- [https://github.com/stepjam/RLBench](https://github.com/stepjam/RLBench)
  
Related source:
-  [ https://peract.github.io/](https://peract.github.io/)

## AI Tool Usage
We have used ChatGPT to ask questions and debug, polishing documents, and we also used OpenAI’s default PPO settings for our PPO training model
