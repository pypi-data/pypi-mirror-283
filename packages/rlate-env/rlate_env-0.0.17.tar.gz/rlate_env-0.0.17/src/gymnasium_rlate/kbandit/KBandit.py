import gymnasium as gym
from gymnasium import spaces
import numpy as np

# Environment for K-Bandit problem
# The environment has 9 arms, each with a different reward distribution
# The goal is to find the arm with the highest expected reward
# Observation: The current state of the environment (the rewards of each arm)
class KBandit(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=1, shape=(9,), dtype=int)
        self.action_space = spaces.Discrete(9)
        self.ranges = [
            [0.20, 0.30],  # Small Range, Low Mean
            [0.45, 0.55],  # Small Range, Medium Mean
            [0.85, 0.95],  # Small Range, High Mean
            [0.10, 0.40],  # Medium Range, Low Mean
            [0.35, 0.65],  # Medium Range, Medium Mean
            [0.60, 0.90],  # Medium Range, High Mean
            [0.00, 0.50],  # Large Range, Low Mean
            [0.25, 0.75],  # Large Range, Medium Mean
            [0.50, 1.00]   # Large Range, High Mean
        ]
        self.state = None

    def _update_state(self):
        self.state = [np.random.uniform(r[0], r[1]) for r in self.ranges]

    def reset(self, seed = None, options = None):
        super().reset(seed=seed)
        self._update_state()
        return self.state, {}

    def step(self, action):
        self._update_state()
        reward = self.state[action]
        terminated = False
        truncated = False
        return self.state, reward, terminated, truncated, {'bandit': action}

    def render(self):
        return self.state
