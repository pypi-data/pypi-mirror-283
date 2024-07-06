# 서드파티
from datasets import DatasetDict, load_dataset

# 프로젝트
from autosink_data_elt.dataset.base import BaseDataset


class AutosinkDataset(BaseDataset):

    def __init__(self, dir) -> None:
        self._dataset: DatasetDict = load_dataset('imagefolder', data_dir=dir)
