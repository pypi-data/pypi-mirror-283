import gymnasium as gym
import numpy as np
from gymnasium import spaces


class PickLow(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(self, render_mode=None):
        self.observation_space = spaces.Box(0, 9, (2,), dtype=np.int8)
        self.action_space = spaces.Discrete(2)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _roll(self):
        left = self.np_random.integers(0, 10)
        right = self.np_random.integers(0, 10)
        self.draw = [left, right]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._roll()
        observation = np.array(self.draw, dtype=np.int8)
        info = {}
        return observation, info

    def step(self, action):
        left = self.draw[0]
        right = self.draw[1]
        card_player = left if action == 0 else right
        card_dealer = right if action == 0 else left

        terminated = bool(card_player != card_dealer)

        observation = np.array(self.draw, dtype=np.int8)
        reward = 1 if card_player < card_dealer else 0 if card_player == card_dealer else -1
        truncated = False
        info = {}

        if not terminated:
            self._roll()

        return observation, reward, terminated, truncated, info

    def render(self):
        return f"{self.draw[0]} {self.draw[1]}"
