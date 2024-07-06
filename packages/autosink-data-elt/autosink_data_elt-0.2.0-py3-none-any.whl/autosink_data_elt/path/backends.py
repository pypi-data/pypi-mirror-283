""" 경로 관리자들에서 사용할 수 있는 백엔드 상수들을 담고 있는 모듈
"""
import os
from typing import Union, Dict, Type
from abc import ABC

GDRIVE_BACKEND = 'GDrive'
LOCAL_BACKEND = 'Local'


class MountingSystemBackendsI(ABC):
    """ 만약 `/A/B/` 디렉토리에 `VolumeC` 가 마운팅된다면, `mount_dir` 은 `/A/B/` 이고 `/A/B/VolumeC` 는 드라이브 루트입니다.
    """

    name = ''

    def __init__(
        self,
        mount_dir: Union[os.PathLike, str],
        volume_name: str,
    ) -> None:
        self.volume_name = volume_name
        self.mount_dir = mount_dir

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if not cls.name:
            raise ValueError(f'Invalid name: {cls.name}')

    @property
    def drive_dir(self):
        return os.path.join(self.mount_dir, self.volume_name)


class GDriveSystem(MountingSystemBackendsI):

    name = GDRIVE_BACKEND

    def __init__(
        self,
        mount_dir: Union[os.PathLike, str] = os.path.join('/', 'content', 'mnt'),
        volume_name: str = 'MyDrive',
    ) -> None:
        super().__init__(mount_dir, volume_name)


class LocalFileSystem(MountingSystemBackendsI):
    """ /A/B/volume/dataset/interest 에서 내가 관심있는 디렉토리가 interest 이라면
    `mount_dir` 은 `/A/B`, `volume_name` 은 `volume`, `interest_root` 은 `dataset/interest` 입니다.
    """

    name = LOCAL_BACKEND

    def __init__(
        self,
        mount_dir: Union[os.PathLike, str] = '',
        volume_name: str = 'volume',
    ) -> None:
        super().__init__(mount_dir, volume_name)


ALLOWED_BACKENDS: Dict[str, Type[MountingSystemBackendsI]] = {
    GDRIVE_BACKEND: GDriveSystem,
    LOCAL_BACKEND: LocalFileSystem,
}
