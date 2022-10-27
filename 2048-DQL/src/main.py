import random
import pygame
import numpy as np
import environment as e
import deep_q_learning as dql
from pygame.locals import *
import constants as const

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from keras.optimizers import Adam


pygame.init()
pygame.display.set_caption("2048")


def get_random_action():
    return random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
    

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=4, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, 
        nb_steps_warmup=10000, target_model_update=1e-2, enable_double_dqn=True)
    return dqn

def append_to_file(filename, data):
    f = open(filename, "a")
    f.write(data)
    f.close()

env = e.TwentyFortyEightEnv()
states = env.observation_space.shape
print(f"states: {states[0]}")
actions = env.action_space.n

model = dql.build_model((1,states[0]), actions)
model.summary()

dqn = build_agent(model, actions)
dqn.compile(Adam(learning_rate=0.05), metrics=['mae'])
history = dqn.fit(env, nb_steps=300000, visualize=False, verbose=1)
print(np.mean(history.history['episode_reward']))
append_to_file("highest_tile.txt", f"\n new, ")
