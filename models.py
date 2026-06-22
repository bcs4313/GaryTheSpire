import numpy as np
import os
import torch as T
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical  # probability distribution over a fixed # of classes

class PPOMemory:
    def __init__(self, batch_size):
        self.states = []  # states for each step
        self.actions = []  # actions taken
        self.probs = []  # log probability of action
        self.vals = []  # antcipated reward values from critic
        self.rewards = []  # actual rewards received
        self.dones = []  # terminal flags that end episodes

        self.batch_size = batch_size


        # for more extensive and thorough training, we train in individual batches
        # rather than just an entire episode of decisions
        def generate_batches(self):
            n_states = len(self.states)  # number of states
            batch_start = np.arange(0, n_states, self.batch_size)  # array of start indices
            indices = np.arange(n_states, dtype=np.int64)

            # shuffle decisions to make step correlation more loose
            np.random.shuffle(indices)

            # take all batch starting points and expand outwards to batch size,
            # then put that batch in as its own singular element in a list
            # (each element in batches is now its own list of states)
            batches = [indices[i:i+self.batch_size] for i in batch_start]

            # return the batches with random indice arrays + all PPOMemory data
            # access relevant data using those indices
            return np.array(self.states),\
                np.array(self.actions),\
                np.array(self.probs),\
                np.array(self.vals),\
                np.array(self.rewards),\
                np.array(self.drones),\
                batches

        # simply add a fully formed memory to the class
        def store_memory(state, action, probs, vals, reward, done):
            self.states.append(state)
            self.actions.append(action)
            self.probs.append(probs)
            self.vals.append(vals)
            self.rewards.append(reward)
            self.dones.append(done)

        # MIND WIPE (Like men in black) *flash
        def clear_memory(self):
            self.states = []
            self.actions = []
            self.probs = []
            self.vals = []
            self.rewards = []
            self.dones = []
