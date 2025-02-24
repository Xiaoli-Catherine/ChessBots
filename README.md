# ChessBots
# CS 175: Projectin AI

# RLBench Setup for HPC3
We translate the following github commands to be HPC3 compatible.
* https://github.com/stepjam/RLBench/tree/master?tab=readme-ov-file#install

1. We have to use the Ubuntu18_04 version of CoppeliaSim since 20_04 requires GLIBC=2.29 (for pyrep) and Rocky 8.10 Green Obsidian only has GLIBC=2.28.
2. Our remote machine can't git clone for some reason so manually download the compressed repository and then pip install directly.
3. Run headless using pyvirtualdisplay instead of the following sudo commands.
	1. https://github.com/stepjam/PyRep?tab=readme-ov-file#running-headless

#### Create Venv

```sh
mkdir project
cd project
python -m venv venv
```

#### Install CoppeliaSim

```sh
export COPPELIASIM_ROOT=${HOME}/CoppeliaSim
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$COPPELIASIM_ROOT
export QT_QPA_PLATFORM_PLUGIN_PATH=$COPPELIASIM_ROOT

wget https://downloads.coppeliarobotics.com/V4_1_0/CoppeliaSim_Edu_V4_1_0_Ubuntu18_04.tar.xz
mkdir -p $COPPELIASIM_ROOT && tar -xf CoppeliaSim_Edu_V4_1_0_Ubuntu18_04.tar.xz -C $COPPELIASIM_ROOT --strip-components 1
rm -rf CoppeliaSim_Edu_V4_1_0_Ubuntu18_04.tar.xz
```

#### Manually install PyRep and RLBench

Install PyRep

```sh
wget https://github.com/stepjam/PyRep/archive/refs/heads/master.zip
unzip master.zip
cd PyRep-master
pip install .
cd ..
```

Change only the pyrep requirement in

```sh
vim RLBench-master/setup.py
```
to
```python
core_requirements = [
    "pyrep",
	...
```

Install RLBench

```sh
wget https://github.com/stepjam/RLBench/archive/refs/heads/master.zip
unzip master.zip
cd RLBench-master
pip install .
cd ..
```

Cleanup

```sh
rm -rf PyRep-master RLBench-master master.zip
```

#### Install Packages

```sh
pip install gym
pip install gymnasium
pip install pyvirtualdisplay
pip install imageio[ffmpeg]
```

#### Environment Variables (Optional)

Insert the environment variable definitions to `~/.bashrc` so it is setup on start.

```sh
export COPPELIASIM_ROOT=${HOME}/CoppeliaSim
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$COPPELIASIM_ROOT
export QT_QPA_PLATFORM_PLUGIN_PATH=$COPPELIASIM_ROOT
```

#### Test Script

Create a `test.py`

```python
from pyvirtualdisplay import Display
import imageio

display = Display(visible=0, size=(1400, 900))
display.start()

import gymnasium as gym
from gymnasium.utils.performance import benchmark_step
import rlbench

env = gym.make('rlbench/reach_target-vision-v0', render_mode='rgb_array')

frames = []

training_steps = 120
episode_length = 40
for i in range(training_steps):
    if i % episode_length == 0:
        print('Reset Episode')
        obs = env.reset()
    obs, reward, terminate, _, _ = env.step(env.action_space.sample())

    frame = env.render()
    frames.append(frame)

print('Done')

output_filename = 'robot_simulation.mp4'
fps = 30

imageio.mimwrite(output_filename, frames, fps=fps)

print(f"Video saved as {output_filename}")

fps_env = benchmark_step(env, target_duration=10)
print(f"Environment FPS: {fps_env:.2f}")

env.close()
display.stop()
```

Create a corresponding `submit_test.sh`

```
#!/bin/bash
#SBATCH -A cs175_class_gpu    ## Account to charge
#SBATCH --time=04:00:00       ## Maximum running time of program
#SBATCH --nodes=1             ## Number of nodes.
                              ## Set to 1 if you are using GPU.
#SBATCH --partition=gpu       ## Partition name
#SBATCH --mem=30GB            ## Allocated Memory
#SBATCH --cpus-per-task 8    ## Number of CPU cores
#SBATCH --gres=gpu:V100:1     ## Type and the number of GPUs

python test.py
```

Run the script

```sh
sbatch submit_test.sh
```
