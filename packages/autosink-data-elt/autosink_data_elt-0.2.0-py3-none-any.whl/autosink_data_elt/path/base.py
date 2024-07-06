""" 경로 관리자 베이스 모듈
"""
import os
from typing import Union, Optional

from autosink_data_elt.path.backends import (
    MountingSystemBackendsI,
    ALLOWED_BACKENDS,
)


class BasePath:
    """ 구글 드라이브 등 데이터 스토리지의 경로들을 정책에 맞게 관리하기 위해 사용되는 경로 관리자 클래스의 베이스
    """

    def __init__(
        self,
        backend: Union[MountingSystemBackendsI, str],
        mount_dir: Optional[Union[str, os.PathLike]] = None,
    ) -> None:
        self.__mount_dir = mount_dir
        self._backend: MountingSystemBackendsI = None

        self.backend = backend

    @property
    def backend(self):
        """ 백엔드 정보
        """
        return self._backend

    @backend.setter
    def backend(self, v: Union[MountingSystemBackendsI, str]):
        """ 사용자의 편의를 위해 `str` 타입과 `MountingSystemBackendsI` 타입 모두로 `self.backend` 를
        초기화할 수 있는데, 이때 적절하게 인자를 파싱해서 `self.backend` 를 할당하기 위한 세터입니다.
        """
        if isinstance(v, str):
            assert v in ALLOWED_BACKENDS, f'백엔드 `{v}`는 허용되지 않는 백엔드입니다.'
            if self.__mount_dir is not None:
                v = ALLOWED_BACKENDS[v](mount_dir=self.__mount_dir)
            else:
                v = ALLOWED_BACKENDS[v]()
        self._backend = v

    @property
    def mount_dir(self) -> Union[str, os.PathLike]:
        return self.backend.mount_dir

    @property
    def drive_dir(self) -> Union[str, os.PathLike]:
        """ 드라이브 루트 경로
        """
        return self.backend.drive_dir
