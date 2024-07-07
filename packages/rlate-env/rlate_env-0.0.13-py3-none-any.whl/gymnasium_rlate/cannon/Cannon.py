import gymnasium as gym
from gymnasium import spaces
import math


class Cannon(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 1}

    def __init__(self):
        self.shots = 10
        self.distance = 0
        self.observation_space = spaces.Box(10, 100, (1, 1))
        self.action_space = spaces.Box(1, 89)

    def reset(
            self,
            seed=None,
            options=None
    ):
        super().reset(seed=seed)
        self.shots = 10
        self._roll_distance()
        return self.distance, {"shots_left": self.shots}

    def _roll_distance(self):
        self.distance = self.np_random.random() * 90 + 10

    def step(self, action):
        self.shots -= 1
        fired_distance = self._calculate_projectile_distance(action)
        error = abs(fired_distance - self.distance)
        hit = error < 0.2

        terminated = self.shots == 0
        truncated = False

        if not terminated:
            self._roll_distance()

        obs = self.distance
        reward = 1 if hit else 0
        return obs, reward, terminated, truncated, {"shots_left": self.shots}

    def _calculate_projectile_distance(self, angle_degrees, speed=32):
        # Convert angle from degrees to radians
        angle_radians = math.radians(angle_degrees)

        # Gravity (m/s^2)
        g = 9.81

        # Calculate distance using the projectile motion formula
        distance = (speed ** 2) * math.sin(2 * angle_radians) / g

        return distance
