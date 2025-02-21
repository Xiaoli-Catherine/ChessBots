---
layout: default
title: Status
---

## Project Summary
Our project aims to explore and analyze the specific performance task of a robot arm setting a chessboard. Our approach involves experimenting with existing algorithms in the RLBench environment, tweaking them to improve their performance, and conducting a comparative study to understand the impact of these modifications. For this project, the input will include task specifications and environmental observations, such as RGB, depth, and segmentation masks, while the output will involve the successful completion of the checkerboard setup task. 

## Approach


## Evaluation
#### Quantitative Evaluation
Our project aims to get the robot arm to properly set up the checkerboard. The most obvious criterion is that the robot arm be able to set up the checkerboard. In case we can not complete the task, we 
If we are able to set up the checkerboard, then the next metric would be the speed at which it is able to do so. Another quantitative metric to use that amalgamates all of the above in a less human-understandable way is just the expected reward of the agent.

#### Qualitative Evaluation
More subjective metrics that are important are of course the humans training the model itself! We want to make sure we have to make logical decisions and choices along the way. In other words, make educated guesses about what could work, try it, see the result, and use that to continue making guesses (wow a meta RL algo?). I think the key idea here is making sure we learn and aren’t just copy-pasting mindlessly. This is hard to measure, but since we are naturally curious, if we are having fun along the way that means we are answering those questions through true understanding. “Have fun” could be more than a cliche but a metric in this case!

## Remaining Goals and Challenges

## Resources Used
source code:
- [https://github.com/stepjam/RLBench](https://github.com/stepjam/RLBench)
Related source:
-[ https://peract.github.io/](https://peract.github.io/)
  



