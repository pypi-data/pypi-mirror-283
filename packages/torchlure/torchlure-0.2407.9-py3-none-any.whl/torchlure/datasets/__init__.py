import gymnasium as gym
import minari
import numpy as np
import torch
from tensordict import TensorDict
from torch.utils.data import Dataset
from tqdm import tqdm


# %%
class MinariEpisodeDataset(Dataset):
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name

        try:
            dataset = minari.load_dataset(dataset_name)
            self.dataset = dataset
            return
        except:
            self.dataset = None

    def exists(self):
        return self.dataset is not None

    def create(self, env, n_episodes: int, exist_ok=False):
        match (self.exists(), exist_ok):
            case (True, True):
                pass
            case (True, False):
                raise ValueError(f"Dataset '{self.dataset_name}' already exists.")
            case (False, _):
                self._create(env, n_episodes)

    def _create(self, env, n_episodes: int):
        if not isinstance(env, minari.DataCollector):
            env = minari.DataCollector(env)

        for _ in tqdm(range(n_episodes), total=n_episodes, desc="Collecting episodes"):
            env.reset()
            done = False
            while not done:
                action = env.action_space.sample()  # <- use your policy here
                obs, rew, terminated, truncated, info = env.step(action)
                done = terminated or truncated
        dataset = env.create_dataset(self.dataset_name)
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int) -> minari.EpisodeData:
        return self.dataset[idx]

    def __iter__(self):
        return iter(self.dataset)

    def info(self):
        print(f"Observation space: {self.dataset.observation_space}")
        print(f"Action space: {self.dataset.action_space}")
        print(f"Total episodes: {self.dataset.total_episodes:,}")
        print(f"Total steps: {self.dataset.total_steps:,}")


class MinariTrajectoryDataset(Dataset):
    def __init__(self, minari_dataset: MinariEpisodeDataset, traj_len: int):
        self.minari_dataset = minari_dataset
        self.traj_len = traj_len
        self.book = self.build_book(self.minari_dataset, self.traj_len)

    @staticmethod
    def build_book(minari_dataset: MinariEpisodeDataset, traj_len: int):
        book = {}
        traj_id = 0

        for ep in minari_dataset:
            if ep.total_timesteps < traj_len:
                continue

            for start_idx in range(ep.total_timesteps - traj_len):
                book[traj_id] = (ep.id, start_idx, start_idx + traj_len)
                traj_id += 1

        return book

    def __len__(self) -> int:
        return len(self.book)

    def __getitem__(self, index: int | list[int]) -> dict:
        match index:
            case int():
                return self._get_by_idx(index).to_dict()
            case list():
                return torch.stack([self._get_by_idx(i) for i in index]).to_dict()
            case slice():
                index = list(range(*index.indices(len(self))))
                return self[index]
            case np.ndarray():
                index = index.tolist()
                return self[index]
            case torch.Tensor():
                index = index.tolist()
                return self[index]
            case _:
                raise ValueError(f"Invalid index type: {type(index)}")

    def _get_by_idx(self, index: int) -> TensorDict:
        ep_id, start_idx, end_idx = self.book[index]
        ep = self.minari_dataset[ep_id]
        observations = ep.observations[start_idx:end_idx]
        actions = ep.actions[start_idx:end_idx]
        rewards = ep.rewards[start_idx:end_idx]
        terminations = ep.terminations[start_idx:end_idx]
        truncations = ep.truncations[start_idx:end_idx]
        timesteps = torch.arange(start_idx, end_idx)

        return TensorDict(
            {
                "observations": torch.tensor(observations),
                "actions": torch.tensor(actions),
                "rewards": torch.tensor(rewards),
                "terminated": torch.tensor(terminations),
                "truncated": torch.tensor(truncations),
                "timesteps": timesteps,
            },
            batch_size=[],
        )

    def sample(self, n: int) -> TensorDict:
        # index = torch.randperm(len(self))[:n]
        index = torch.randint(0, len(self), (n,))
        return self[index]
