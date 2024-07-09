import os
import urllib.request
from pathlib import Path

import h5py
from tqdm import tqdm

from .d4rl_infos import DATASETS_URLS


def filepath_from_url(dataset_url: str):
    D4RL_DATASET_DIR = Path(
        os.environ.setdefault("D4RL_DATASET_DIR", "~/.d4rl/datasets")
    )
    D4RL_DATASET_DIR.mkdir(parents=True, exist_ok=True)

    dataset_filepath = D4RL_DATASET_DIR / dataset_url.split("/")[-1]
    return dataset_filepath


def download_dataset_from_url(dataset_url):
    dataset_filepath = Path(filepath_from_url(dataset_url))
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

    if env is None:
        return data_dict

    # Run a few quick sanity checks
    for key in ["observations", "actions", "rewards", "terminals"]:
        assert key in data_dict, "Dataset is missing key %s" % key
    N_samples = data_dict["observations"].shape[0]
    if env.observation_space.shape is not None:
        assert (
            data_dict["observations"].shape[1:] == env.observation_space.shape
        ), "Observation shape does not match env: %s vs %s" % (
            str(data_dict["observations"].shape[1:]),
            str(env.observation_space.shape),
        )
    assert (
        data_dict["actions"].shape[1:] == env.action_space.shape
    ), "Action shape does not match env: %s vs %s" % (
        str(data_dict["actions"].shape[1:]),
        str(env.action_space.shape),
    )
    if data_dict["rewards"].shape == (N_samples, 1):
        data_dict["rewards"] = data_dict["rewards"][:, 0]
    assert data_dict["rewards"].shape == (N_samples,), "Reward has wrong shape: %s" % (
        str(data_dict["rewards"].shape)
    )
    if data_dict["terminals"].shape == (N_samples, 1):
        data_dict["terminals"] = data_dict["terminals"][:, 0]
    assert data_dict["terminals"].shape == (
        N_samples,
    ), "Terminals has wrong shape: %s" % (str(data_dict["rewards"].shape))
    return data_dict


def d4rl_offline_dataset(dataset_id: str, env=None):
    assert (
        dataset_id in DATASETS_URLS
    ), f"Dataset {dataset_id} not found in D4RL, available datasets: {list(DATASETS_URLS.keys())}"
    return get_dataset(dataset_id, env=env)
