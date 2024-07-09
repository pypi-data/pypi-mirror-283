import os
import urllib.request
from pathlib import Path

import h5py
import torch
from tqdm import tqdm

from .d4rl_infos import DATASETS_URLS


def filepath_from_url(dataset_url: str):
    D4RL_DATASET_DIR = Path(
        os.environ.setdefault("D4RL_DATASET_DIR", "~/.d4rl/datasets")
    ).expanduser()
    D4RL_DATASET_DIR.mkdir(parents=True, exist_ok=True)
    dataset_filepath = D4RL_DATASET_DIR / dataset_url.split("/")[-1]
    return dataset_filepath


def download_dataset_from_url(dataset_url):
    dataset_filepath = filepath_from_url(dataset_url)
    if not dataset_filepath.exists():
        print("Downloading dataset:", dataset_url, "to", dataset_filepath)
        urllib.request.urlretrieve(dataset_url, dataset_filepath)
    if not dataset_filepath.exists():
        raise IOError("Failed to download dataset from %s" % dataset_url)
    return dataset_filepath


def get_keys(h5file):
    keys = []

    def visitor(name, item):
        if isinstance(item, h5py.Dataset):
            keys.append(name)

    h5file.visititems(visitor)
    return keys


def get_dataset(dataset_id: str, env=None):
    dataset_url = DATASETS_URLS[dataset_id]
    h5path = download_dataset_from_url(dataset_url)
    data_dict = {}
    with h5py.File(h5path, "r") as dataset_file:
        for k in tqdm(get_keys(dataset_file), desc="load datafile"):
            try:  # first try loading as an array
                data_dict[k] = dataset_file[k][:]
            except ValueError as e:  # try loading as a scalar
                data_dict[k] = dataset_file[k][()]

    if env is not None:
        validate_data(data_dict, env)

    return data_dict, h5path


def validate_data(data_dict, env):
    for key in ["observations", "actions", "rewards", "terminals"]:
        assert key in data_dict, f"Dataset is missing key {key}"

    N_samples = data_dict["observations"].shape[0]

    if env.observation_space.shape is not None:
        assert (
            data_dict["observations"].shape[1:] == env.observation_space.shape
        ), f"Observation shape does not match env: {data_dict['observations'].shape[1:]} vs {env.observation_space.shape}"

    assert (
        data_dict["actions"].shape[1:] == env.action_space.shape
    ), f"Action shape does not match env: {data_dict['actions'].shape[1:]} vs {env.action_space.shape}"

    if data_dict["rewards"].shape == (N_samples, 1):
        data_dict["rewards"] = data_dict["rewards"][:, 0]
    assert data_dict["rewards"].shape == (
        N_samples,
    ), f"Reward has wrong shape: {data_dict['rewards'].shape}"

    if data_dict["terminals"].shape == (N_samples, 1):
        data_dict["terminals"] = data_dict["terminals"][:, 0]
    assert data_dict["terminals"].shape == (
        N_samples,
    ), f"Terminals has wrong shape: {data_dict['terminals'].shape}"


def d4rl_offline_dataset(dataset_id: str, env=None):
    assert (
        dataset_id in DATASETS_URLS
    ), f"Dataset {dataset_id} not found in D4RL, available datasets: {list(DATASETS_URLS.keys())}"
    data_dict, file_path = get_dataset(dataset_id, env=env)
    print(f"Dataset loaded and saved at: {file_path}")
    return data_dict


class D4RLDataset(torch.utils.data.Dataset):
    def __init__(self, data_dict):
        self.observations = torch.tensor(data_dict["observations"], dtype=torch.float32)
        self.actions = torch.tensor(data_dict["actions"], dtype=torch.float32)
        self.rewards = torch.tensor(data_dict["rewards"], dtype=torch.float32)
        self.next_observations = torch.tensor(
            data_dict["next_observations"], dtype=torch.float32
        )
        self.terminals = torch.tensor(data_dict["terminals"], dtype=torch.bool)
        self.timeouts = torch.tensor(data_dict["timeouts"], dtype=torch.bool)

        # Optional data
        if "infos/action_log_probs" in data_dict:
            self.action_log_probs = torch.tensor(
                data_dict["infos/action_log_probs"], dtype=torch.float32
            )
        if "infos/qpos" in data_dict:
            self.qpos = torch.tensor(data_dict["infos/qpos"], dtype=torch.float32)
        if "infos/qvel" in data_dict:
            self.qvel = torch.tensor(data_dict["infos/qvel"], dtype=torch.float32)

    def __len__(self):
        return len(self.observations)

    def __getitem__(self, idx):
        sample = {
            "observation": self.observations[idx],
            "action": self.actions[idx],
            "reward": self.rewards[idx],
            "next_observation": self.next_observations[idx],
            "terminal": self.terminals[idx],
            "timeout": self.timeouts[idx],
        }

        # Add optional data if available
        if hasattr(self, "action_log_probs"):
            sample["action_log_prob"] = self.action_log_probs[idx]
        if hasattr(self, "qpos"):
            sample["qpos"] = self.qpos[idx]
        if hasattr(self, "qvel"):
            sample["qvel"] = self.qvel[idx]

        return sample
