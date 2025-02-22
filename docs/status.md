---
layout: default
title: Status
---

## Project Summary
Our project aims to explore and analyze the specific performance task of a robot arm setting a chessboard within the RLBench environment. Our approach involves experimenting with existing algorithms in the RLBench environment, tweaking them to improve their performance, and conducting a comparative study to understand the impact of these modifications. For this project, the input will include task specifications and environmental observations, such as RGB, depth, and segmentation masks, while the output will involve the successful completion of the checkerboard setup task. 

## Approach


## Evaluation
#### Quantitative Evaluation
Our project aims to get the robot arm to properly set up the checkerboard. The most obvious criterion is that the robot arm be able to set up the checkerboard. We will start by modifying the number of pieces to be set up to create different levels of difficulty. Starting from small pieces, in case we can not complete the task.
If we are able to set up the checkerboard, then the next metric would be the speed at which it is able to do so. Another quantitative metric to use that amalgamates all of the above in a less human-understandable way is just the expected reward of the agent.

#### Qualitative Evaluation
We will observe if our modifications in the algorithm improve the system’s adaptability and efficiency, particularly in precision placement and reduced execution time. For now, we just completed the RLBench environment setup. The output shows the RLBench environment works well. Meanwhile, we want to make sure we have to make logical decisions and choices along the way. We make educated guesses about what could work, try it, see the result, and use that to continue making guesses. The key idea here is to make sure that we have learned something during the project.
<img width="500" alt="Screenshot 2025-02-21 at 2 30 50 PM" src="https://github.com/user-attachments/assets/5bd61a07-b1fa-4502-841c-78729e3b8e04" />
RLBench environment test

## Remaining Goals and Challenges

## Resources Used
source code:
- [https://github.com/stepjam/RLBench](https://github.com/stepjam/RLBench)
  
Related source:
-  [ https://peract.github.io/](https://peract.github.io/)
  
Environment setup:

We have set up a test RLBench environment that looks like

<img width="500" alt="Screenshot 2025-02-21 at 2 30 50 PM" src="https://github.com/user-attachments/assets/5bd61a07-b1fa-4502-841c-78729e3b8e04" />


