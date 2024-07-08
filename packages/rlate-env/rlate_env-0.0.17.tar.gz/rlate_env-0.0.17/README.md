# RL Enviros

RL Enviros is a collection of custom environments compatible with Gymnasium, designed to simulate various games and
scenarios for reinforcement learning experiments. This project aims to provide a variety of environments to help
researchers and enthusiasts develop and test reinforcement learning algorithms.

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
- Published on [PyPi](https://pypi.org/project/rlate-env/)
- You can install the `rlate-env` package directly from PyPi:

```bash
pip install rlate-env
```

## Environments

**Shuffler**
Arrange a shuffled list of numbers in ascending order by swapping with the number 5.

**PickHigh**
Choose the higher-valued card from two randomly drawn cards.

**PickLow**
Choose the lower-valued card from two randomly drawn cards.

**Cannon**
Hit a target at a random distance by adjusting the firing angle of a cannon.

**Traffic Light**
Decide to drive, slow down, or stop based on the current traffic light color.

**K-Bandit**
Find and exploit the arm with the highest expected reward in a multi-armed bandit setup.

## Usage

Here is an example of how to use the `Cannon` environment:

```python
import gymnasium_rlate as rlate

# Create the Canon environment
env = rlate.Cannon()

# Reset the environment
obs, info = env.reset()
print(obs)

# Make a step in the environment
obs, reward, terminated, truncated, _ = env.step(23.5)
print(obs, reward, terminated)

# Render the environment
print(env.render())

# Close the environment
env.close()
```

## Contributing

Contributions are welcome! If you have an environment you'd like to add or an improvement to suggest, please open an
issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Repository

GitHub Repository: [https://github.com/RLate-Space/RL-Enviros](https://github.com/RLate-Space/RL-Enviros)