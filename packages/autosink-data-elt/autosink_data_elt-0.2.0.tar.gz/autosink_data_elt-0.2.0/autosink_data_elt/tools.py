# 내장
import os
import zipfile
from typing import Union, Optional


def unzip(
    directory_path: Union[os.PathLike, str],
    extract_root: Optional[Union[os.PathLike, str]] = None,
):
    """ The function `unzip` takes a directory path as input and likely unzips any compressed files
    within that directory. 이 스크립트는 어떤 파일의 압축이 이미 해제되었는지를 디렉토리 이름을 기준으로 확인하고
    선별적으로 압축을 해제하는 기능을 가지고 있습니다.

    Args:
      directory_path: A string representing the path to a directory containing a zip file
        that you want to unzip.
      extract_root: 압축 해제된 파일들이 저장되는 디렉토리.
    """
    if not extract_root:
        extract_root = os.path.join(directory_path, 'extract')

    # 압축 파일 디렉토리에서 모든 ZIP 파일 찾기
    for file in os.listdir(directory_path):
        if file.endswith('.zip'):
            # 각 ZIP 파일의 전체 경로
            zip_file_path = os.path.join(directory_path, file)
            # 압축 해제될 하위 디렉토리 경로 (ZIP 파일 이름을 기반으로)
            extract_to_path = os.path.join(extract_root, file.rsplit('.', 1)[0])

            # 해당 디렉토리가 이미 존재하지 않으면 압축 해제 수행
            if not os.path.exists(extract_to_path):
                os.makedirs(extract_to_path)  # 디렉토리 생성
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to_path)
                print(f'Extracted {file} to {extract_to_path}')
            else:
                print(f'{file} is already extracted to {extract_to_path}')
    return extract_root


if __name__ == '__main__':
    unzip(
        'volume/data-lake',
        'volume/data-lake/extract',
    )
