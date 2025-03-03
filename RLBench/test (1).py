import gymnasium as gym
from gymnasium.utils.performance import benchmark_step
import rlbench

import imageio
import time

from rlbench.gym import RLBenchEnv

# Create RLBench environment for the task
env = gym.make('rlbench/setup_checkers-vision-v0', render_mode="rgb_array")

fps_env = benchmark_step(env, target_duration=10)
print(f"Environment FPS: {fps_env:.2f}")

frames = []
  
start = time.perf_counter()
# increase training steps from 120 to 240 
training_steps = 240
episode_length = 40
for i in range(training_steps):
    if i % episode_length == 0:
        print(f'Reset Episode, Time: {time.perf_counter() - start:.5f}s')
        obs, _ = env.reset()
    obs, reward, terminate, truncated, info = env.step(env.action_space.sample())

    frame = env.render()
    frames.append(frame)
    if terminate or truncated:
        obs, _ = new.reset()
print('Done')

output_filename = 'robot_simulation1.mp4'
# lower fps from 30 to 15
fps = 15
# duplicate each frame before writing the video to make it smoother and slower
extended_frames = []
for frame in frames:
    extended_frames.append(frame)
    extended_frames.append(frame)
    
imageio.mimwrite(output_filename, extended_frames, fps=fps)
print(f"Video saved as {output_filename}")

env.close()