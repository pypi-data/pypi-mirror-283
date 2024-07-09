# just-d4rl

Easy-to-use D4RL offline dataset loader


## Installation
```sh
pip install just-d4rl
```

## Usage

```python
from just_d4rl import d4rl_offline_dataset

dataset = d4rl_offline_dataset("hopper-medium-v2")
dataset = d4rl_offline_dataset("walker2d-random-v2")
dataset = d4rl_offline_dataset("halfcheetah-medium-expert-v2")
dataset = d4rl_offline_dataset("antmaze-umaze-v2")

dataset = d4rl_offline_dataset("hopper-medium-v2")
dataset['observations'].shape, dataset['actions'].shape, dataset['rewards'].shape, dataset['terminals'].shape, dataset['timeouts'].shape
# ((1000000, 11), (1000000, 3), (1000000,), (1000000,), (1000000,))
```