import gymnasium as gym
from gymnasium import spaces


class PickHigh(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(self, render_mode=None):
        self.observation_space = spaces.Discrete(100)
        self.action_space = spaces.Discrete(2)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _roll(self):
        left = self.np_random.integers(0, 10)
        right = self.np_random.integers(0, 10)
        self.draw = left * 10 + right

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._roll()
        observation = self.draw
        info = {}
        return observation, info

    def step(self, action):
        left = self.draw // 10
        right = self.draw % 10
        card_player = left if action == 0 else right
        card_dealer = right if action == 0 else left

        terminated = bool(card_player != card_dealer)

        observation = self.draw
        reward = 1 if card_player > card_dealer else 0 if card_player == card_dealer else -1
        truncated = False
        info = {}

        if not terminated:
            self._roll()

        return observation, reward, terminated, truncated, info

    def render(self):
        return f"{self.draw // 10} {self.draw % 10}"
