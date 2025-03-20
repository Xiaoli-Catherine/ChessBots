import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback, BaseCallback
from gymnasium.wrappers import TimeLimit
import imageio
import time
import os
import rlbench
import matplotlib.pyplot as plt
import numpy as np

# Wrap the environment in a TimeLimit to reset every 256 steps
base_env = gym.make('rlbench/setup_checkers-vision-v0', render_mode="rgb_array")
env = TimeLimit(base_env, max_episode_steps=256)

# Create a callback to save environment length and reward and generate a plot
class EpisodeStatsCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(EpisodeStatsCallback, self).__init__(verbose)
        self.episode_rewards = []
        self.episode_lengths = []
        self.current_episode_reward = 0
        self.current_episode_length = 0
        self.episode_count = 0
        
    def _on_step(self) -> bool:
        # Update episode tracking
        self.current_episode_length += 1
        self.current_episode_reward += self.locals.get("rewards")[0]
        
        # Check if episode has ended
        done = self.locals.get("dones")[0]
        if done:
            # Save episode stats
            self.episode_rewards.append(self.current_episode_reward)
            self.episode_lengths.append(self.current_episode_length)
            self.episode_count += 1
            
            # Reset for next episode
            self.current_episode_reward = 0
            self.current_episode_length = 0
            
            # Generate and save plot
            self._generate_plot()
            
        return True
    
    def _generate_plot(self):
        # Create directory if it doesn't exist
        os.makedirs("./training_plots", exist_ok=True)
        
        plt.figure(figsize=(12, 5))
        
        # Plot episode rewards
        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(self.episode_rewards) + 1), self.episode_rewards)
        plt.title('Episode Rewards')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.grid(True)
        
        # Plot episode lengths
        plt.subplot(1, 2, 2)
        plt.plot(range(1, len(self.episode_lengths) + 1), self.episode_lengths, color='orange')
        plt.title('Episode Lengths')
        plt.xlabel('Episode')
        plt.ylabel('Steps')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'./training_plots/episode_stats.png')
        plt.close()
        
        # Also save the raw data as numpy array for later use
        np.save('./training_plots/episode_rewards.npy', np.array(self.episode_rewards))
        np.save('./training_plots/episode_lengths.npy', np.array(self.episode_lengths))

# Create the episode stats callback
episode_stats_callback = EpisodeStatsCallback()

model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,  # Already set to 1
    learning_rate=3e-4,
    n_steps=2048, #change 2048 to 1024
    batch_size=512, # change 64 to 128
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2, #change 0.2 to 0.3
    ent_coef=0.05, #change 0.0 to 0.01
    max_grad_norm=0.5,
    
    
)


# Set the log standard deviation manually
# with torch.no_grad():
#     model.policy.log_std[:] = torch.log(torch.tensor(0.6))  # Setting std to 0.6


loaded_model = PPO.load("3ppo_setup_checkers_final")

model.policy.load_state_dict(loaded_model.policy.state_dict())


# Change save_freq to 2048
checkpoint_callback = CheckpointCallback(save_freq=2048*10, save_path="./ppo_checkpoints/", name_prefix="ppo_setup_checkers")

total_timesteps = 2048*32
# Add verbose to model.learn(), though it was already there
model.learn(total_timesteps=total_timesteps, callback=[checkpoint_callback, episode_stats_callback])

model.save("update3e-4ppo_setup_checkers_final")

frames = []
obs, _ = env.reset()
for _ in range(256):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminate, truncated, info = env.step(action)
    frame = env.render()
    frames.append(frame)
    if terminate or truncated:
        obs, _ = env.reset()

output_filename = 'update3e-4ppo_setup_checkers_evaluation.mp4'
fps = 15
extended_frames = []
for frame in frames:
    extended_frames.append(frame)
    
imageio.mimwrite(output_filename, extended_frames, fps=fps)
print(f"Evaluation video saved as {output_filename}")

env.close()
