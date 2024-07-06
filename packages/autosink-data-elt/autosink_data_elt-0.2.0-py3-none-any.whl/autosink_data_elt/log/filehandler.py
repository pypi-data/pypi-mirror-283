# 내장
import os
import json
import hashlib
import pytz
from datetime import datetime
from collections import deque

# 프로젝트
from autosink_data_elt.log.utils import get_logger
from autosink_data_elt.log.template.dishwashing import *

logger = get_logger('filehandler')


class JSONFileHandler:

    def __init__(self, user_id, timezone='Asia/Seoul'):
        self.user_id = user_id
        self.timezone = pytz.timezone(timezone)
        self.image_counter = 0
        self.dishwashing_id = self._generate_dishwashing_id()
        self.folder_name = self.dishwashing_id
        self.filename = os.path.join(self.folder_name, 'interactions.json')
        os.makedirs(self.folder_name, exist_ok=True)
        logger.info(
            'Initialized JSONFileHandler with '
            f'folder {self.folder_name} and file {self.filename}'
        )

    def _generate_dishwashing_id(self):
        hash_input = (self.user_id + str(datetime.now())).encode('utf-8')
        return hashlib.sha1(hash_input).hexdigest()[:10]

    @classmethod
    def read_file(cls, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            d = json.load(file)
            version = d.get('version', 1)
            if version == 1:
                return DishwashingDataV1(**d)
            elif version == 2:
                return DishwashingDataV2(**d)
            else:
                raise ValueError(f'Unsupported version: {version}')

    def write_file(self, data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data.to_dict(), file, indent=4)
        self.image_counter = 0  # Reset the image counter after writing to file
        logger.info(f'Wrote data to {self.filename} and reset image counter')

    def create_default_data(self, dishwashing_start=None, version=2, deque_size=10):
        if dishwashing_start is None:
            dishwashing_start = datetime.now(self.timezone).isoformat(timespec='seconds')

        if version == 1:
            return DishwashingDataV1(
                version=1,
                user_id=self.user_id,
                dishwashing_id=self.dishwashing_id,
                dishwashing_start=dishwashing_start
            )
        elif version == 2:
            return DishwashingDataV2(
                version=2,
                user_id=self.user_id,
                dishwashing_id=self.dishwashing_id,
                dishwashing_start=dishwashing_start,
                interactions=deque(maxlen=deque_size)
            )
        else:
            raise ValueError(f'Unsupported version: {version}')

    def add_interaction(self, data, **kwargs):
        timestamp = datetime.now().isoformat(timespec='seconds')

        if data.version == 1:
            interaction = InteractionV1.create(timestamp, kwargs.pop('image'), **kwargs)
        elif data.version == 2:
            interaction = InteractionV2.create(timestamp, kwargs.pop('image'), **kwargs)
        else:
            raise ValueError(f'Unsupported version: {data.version}')

        data.interactions.append(interaction)
        # logger.info(f'Added interaction: {interaction}')
        return data


if __name__ == '__main__':
    user_id = 'user1234'
    file_handler = JSONFileHandler(user_id)

    # 기본 데이터 생성 (버전 2)
    dishwashing_start = '2024-10-04T14:30:00'
    data = file_handler.create_default_data(dishwashing_start, version=2)

    # 상호작용 객체 생성 및 추가
    data = file_handler.add_interaction(data, model_output=0, arduino_output=0, magnetic_status=0)
    data = file_handler.add_interaction(data, model_output=0, arduino_output=0, magnetic_status=0)
    data = file_handler.add_interaction(data, model_output=0, arduino_output=1, magnetic_status=1)

    # 파일에 쓰기
    file_handler.write_file(data)

    # 파일에서 읽기
    read_data = JSONFileHandler.read_file(
        'volume/data-lake/extract/20240615_180539/interactions.json'
    )
    print(read_data)
