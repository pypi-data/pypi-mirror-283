from dataclasses import dataclass


@dataclass
class InteractionV1:
    timestamp: str
    model_output: int
    magnetic: int
    image: str

    @staticmethod
    def create(timestamp, image, **kwargs):
        return InteractionV1(timestamp=timestamp,
                             model_output=kwargs.get('model_output', 0),
                             magnetic=kwargs.get('magnetic', 0),
                             image=image)

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "model_output": self.model_output,
            "magnetic": self.magnetic,
            "image": self.image
        }


@dataclass
class InteractionV2:
    timestamp: str
    model_output: int
    arduino_output: int
    magnetic_status: int
    image: str

    @staticmethod
    def create(timestamp, image, **kwargs):
        return InteractionV2(timestamp=timestamp,
                             model_output=kwargs.get('model_output', 0),
                             arduino_output=kwargs.get('arduino_output', 0),
                             magnetic_status=kwargs.get('magnetic_status', 0),
                             image=image)

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "model_output": self.model_output,
            "arduino_output": self.arduino_output,
            "magnetic_status": self.magnetic_status,
            "image": self.image
        }
