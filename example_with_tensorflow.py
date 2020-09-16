
# 1) import everything
from __future__ import absolute_import, division, print_function

import base64
import imageio
import IPython
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import time
import shutil
from pathlib import Path

import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import policy_saver
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

import custom_openai_frameworks

# 2) define our variables
num_iterations: int = 20000 # how long to train for. I recoment this be greater than eval_interval * 3
initial_collect_steps: int = 1000 
collect_steps_per_iteration: int = 1
replay_buffer_max_length: int = 100000 
batch_size: int = 64 
learning_rate: float = 1e-3
log_interval: int = 200
num_eval_episodes: int = 10
eval_interval: int = 1000
#env_name: str = 'StandInRain-v0'
#env_name: str = 'SimpleCrawler-v1'
env_name: str = 'GolfCardGame-v0'
model_number: str = str(time.time()) # if you want to load a specific model, edit this
#model_number: str = '1588725542.976953'
save_gif_every_x_iterations: int = 100000


Path("output/"+env_name).mkdir(parents=True, exist_ok=True)
    


#def load_saved_model():

#def train_model():
tf.compat.v1.enable_v2_behavior()

train_py_env = suite_gym.load(env_name)
eval_py_env = suite_gym.load(env_name)
train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

fc_layer_params = (100,)

q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=fc_layer_params)

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

train_step_counter = tf.Variable(0)

agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()

eval_policy = agent.policy
collect_policy = agent.collect_policy

random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())

example_environment = tf_py_environment.TFPyEnvironment(
    suite_gym.load(env_name))


time_step = example_environment.reset()

random_policy.action(time_step)


def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):
        t_s = environment.reset()
        episode_return = 0.0
        while not t_s.is_last():
            action_step = policy.action(t_s)
            t_s = environment.step(action_step.action)
            episode_return += t_s.reward
            total_return += episode_return

    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]


# See also the metrics module for standard implementations of different metrics.
# https://github.com/tensorflow/agents/tree/master/tf_agents/metrics


compute_avg_return(eval_env, random_policy, num_eval_episodes)

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_max_length)

#setup model for saving
checkpoint_dir = "output/"+env_name+"/models/"+model_number+"/checkpoint/"
Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)
train_checkpointer = common.Checkpointer(
    ckpt_dir=checkpoint_dir,
    max_to_keep=1,
    agent=agent,
    policy=agent.policy,
    replay_buffer=replay_buffer,
    global_step=train_step_counter
)
policy_dir = "output/"+env_name+"/models/"+model_number+"/policy/"
Path(policy_dir).mkdir(parents=True, exist_ok=True)
tf_policy_saver = policy_saver.PolicySaver(agent.policy)

#load a saved model if it exists
train_checkpointer.initialize_or_restore()
train_step_counter = tf.compat.v1.train.get_global_step()
try:
    saved_policy = tf.compat.v2.saved_model.load(policy_dir)
except:
    pass

def collect_step(environment, policy, buffer):
    t_s = environment.current_time_step()
    action_step = policy.action(t_s)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(t_s, action_step, next_time_step)

    # Add trajectory to the replay buffer
    buffer.add_batch(traj)

def collect_data(env, policy, buffer, steps):
    for _ in range(steps):
        collect_step(env, policy, buffer)

collect_data(train_env, random_policy, replay_buffer, steps=100)

# This loop is so common in RL, that we provide standard implementations. 
# For more details see the drivers module.
# https://github.com/tensorflow/agents/blob/master/tf_agents/docs/python/tf_agents/drivers.md


# For the curious:
# Uncomment to peel one of these off and inspect it.
# iter(replay_buffer.as_dataset()).next()

# Dataset generates trajectories with shape [Bx2x...]
dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, 
    sample_batch_size=batch_size, 
    num_steps=2).prefetch(3)

iterator = iter(dataset)

# (Optional) Optimize by wrapping some of the code in a graph using TF function.
agent.train = common.function(agent.train)

# Reset the train step
agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
returns = [avg_return]

Path("output/"+env_name+"/gifs").mkdir(parents=True, exist_ok=True)
def create_policy_eval_video(policy):
    t_s = eval_env.reset()
    eval_py_env.render()
    while not t_s.is_last():
        action_step = policy.action(t_s)
        t_s = eval_env.step(action_step.action)
        eval_py_env.render()
    eval_py_env.close()
    
for _ in range(num_iterations):

    # Collect a few steps using collect_policy and save to the replay buffer.
    for _ in range(collect_steps_per_iteration):
        collect_step(train_env, agent.collect_policy, replay_buffer)

    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = agent.train(experience).loss

    step = agent.train_step_counter.numpy()

    if step % log_interval == 0:
        print('step = {0}: loss = {1}'.format(step, train_loss))

    if step % eval_interval == 0:
        avg_return = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
        print('step = {0}: Average Return = {1}'.format(step, avg_return))
        returns.append(avg_return)
    
    if step % save_gif_every_x_iterations == 0:
        create_policy_eval_video(agent.policy)
        

create_policy_eval_video(agent.policy)

Path("output/"+env_name+"/graphs").mkdir(parents=True, exist_ok=True)
iterations = range(0, num_iterations + 1, eval_interval)
plt.plot(iterations, returns)
plt.ylabel('Average Return')
plt.xlabel('Iterations')
plt.savefig("output/"+env_name+"/graphs/"+str(time.time())+"-"+'training.png')

    
#def save_model():
Path("output/"+env_name+"/models").mkdir(parents=True, exist_ok=True)
train_checkpointer.save(train_step_counter)
tf_policy_saver.save(policy_dir)



