import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random


class Shuffler(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 1}

    def __init__(self):
        self.state = None
        self.observation_space = spaces.Box(
            low=0,
            high=5,
            shape=(6,),
            dtype=np.int8
        )
        self.action_space = spaces.Discrete(6)

    def _get_random_state(self):
        state = [i for i in range(6)]
        random.shuffle(state)
        return np.array(state, dtype=np.int8)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = self._get_random_state()
        return self.state, {}

    def step(self, action):
        space = np.where(self.state == 5)
        self.state[action], self.state[space] = self.state[space].item(), self.state[action].item()
        obs = self.state
        is_complete = np.array_equal(self.state, np.array([i for i in range(6)]))
        reward = 1 if is_complete else 0
        terminated = is_complete
        truncated = False
        return obs, reward, terminated, truncated, {}

    def render(self):
        return ' '.join(self.state)
