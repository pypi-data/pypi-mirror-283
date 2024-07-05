# RL Enviros

RL Enviros is a collection of custom environments compatible with Gymnasium, designed to simulate various games and scenarios for reinforcement learning experiments. This project aims to provide a variety of environments to help researchers and enthusiasts develop and test reinforcement learning algorithms.

## Table of Contents

- [Installation](#installation)
- [Environments](#environments)
  - [PickHigh](#pickhigh)
  - [AnotherEnv](#anotherenv)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

### PyPi

You can install the `rl-enviros-rlate` package directly from PyPi:

```bash
pip install rl-enviros-rlate
```

### From Source

To install the `rl-enviros-rlate` package from the source, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/RLate-Space/RL-Enviros.git
    cd RL-Enviros
    ```

2. Install the package using `pip`:
    ```bash
    pip install -e .
    ```

## Environments

### PickHigh

PickHigh is a simple game where the player picks between two cards, aiming to select the higher card. This environment is useful for testing basic reinforcement learning algorithms.

- **Observation Space**: Discrete space of size 100, representing two cards (e.g., 34 for left card 3 and right card 4).
- **Action Space**: Discrete space of size 2. Action 0 selects the left card, and action 1 selects the right card.
- **Reward**:
    - +1 if the chosen card is higher.
    - 0 if both cards are the same.
    - -1 if the chosen card is lower.
- **Episode Termination**: The episode terminates when the player picks a card that is different from the dealer's card.

[Detailed Documentation for PickHigh](src/gymnasium/pick_high/README.md)

## Usage

Here is an example of how to use the `PickHigh` environment:

```python
import gymnasium as gym
from gym_examples.envs.pick_high import PickHigh

# Create the environment
env = PickHigh()

# Reset the environment to get the initial observation
observation, info = env.reset(seed=42)

# Print the initial observation
print(f"Initial observation: {observation}")

# Take a random action
action = env.action_space.sample()
observation, reward, terminated, truncated, info = env.step(action)

# Print the results of the action
print(f"Action taken: {action}")
print(f"New observation: {observation}")
print(f"Reward: {reward}")
print(f"Terminated: {terminated}")
print(f"Truncated: {truncated}")
print(f"Info: {info}")

# Render the environment
print(env.render())

# Close the environment
env.close()
```

## Contributing

Contributions are welcome! If you have an environment you'd like to add or an improvement to suggest, please open an issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Repository

GitHub Repository: [https://github.com/RLate-Space/RL-Enviros](https://github.com/RLate-Space/RL-Enviros)