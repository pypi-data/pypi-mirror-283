# just-d4rl

Easy-to-use D4RL offline dataset loader


## Installation
- [PyPI](https://pypi.org/project/just-d4rl/)

```sh
pip install just-d4rl
```

## Usage

```python
from just_d4rl import D4RLDataset, d4rl_offline_dataset

dataset = d4rl_offline_dataset("hopper-medium-v2")
dataset = d4rl_offline_dataset("walker2d-random-v2")
dataset = d4rl_offline_dataset("halfcheetah-medium-expert-v2")
dataset = d4rl_offline_dataset("antmaze-umaze-v2")

dataset = d4rl_offline_dataset("hopper-medium-v2")
dataset['observations'].shape, dataset['actions'].shape, dataset['rewards'].shape, dataset['next_observations'].shape, dataset['terminals'].shape
# ((1000000, 11),
#  (1000000, 11),
#  (1000000, 3),
#  (1000000,),
#  (1000000,))


dataset = d4rl_offline_dataset("hopper-medium-v2")
dataset = D4RLDataset(d4rl_dataset)

batch = dataset[-16:]
batch["observation"].shape, batch["action"].shape, batch["reward"].shape, batch["next_observation"].shape, batch["terminal"].shape
# (torch.Size([16, 11]),
#  torch.Size([16, 3]),
#  torch.Size([16]),
#  torch.Size([16, 11]),
#  torch.Size([16]),
#  torch.Size([16]))
```
