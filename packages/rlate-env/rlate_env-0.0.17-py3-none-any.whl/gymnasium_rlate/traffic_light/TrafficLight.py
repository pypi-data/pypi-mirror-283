import gymnasium as gym
from gymnasium import spaces


class TrafficLight(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(self):
        self.state = None
        self.observation_space = spaces.Discrete(3)
        self.action_space = spaces.Discrete(3)

    def _get_color(self, state):
        return ["green", "yellow", "red"][state]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Reset the state to green
        self.state = 0
        return self.state, {"color": self._get_color(self.state)}

    # state: 0: green 1: yellow 2: red
    # action: 0: drive 1: slow 2: stop
    def step(self, action):

        reward_structure = {
            0: {0: 1, 1: -1, 2: -1},
            1: {0: -1, 1: 1, 2: -1},
            2: {0: -1, 1: -1, 2: 1}
        }

        # calculate reward
        reward = reward_structure[self.state][action]
        terminated = self.state == 2
        truncated = reward == -1

        # identify the next state
        # generate a random chance to change the state
        roll = self.np_random.random()
        if not terminated and not truncated and roll > 0.7:
            self.state = (self.state + 1) % 3

        return self.state, reward, terminated, truncated, {"color": self._get_color(self.state)}

    def render(self):
        return self._get_color(self.state)
