# Data Extract-Load-Transform for Autosink Project

[🇬🇧](README.md) | [🇰🇷](README.kr.md) | [🇨🇳](README.zh-CN.md)

이 저장소에는 feature store, data lake 등 각종 데이터 저장소의 경로를 관리한다. data lake 에 저장되는 원시데이터 형식인 json 파일을 잘 읽고 쓰기 위한 데이터타입과 연산들이 정의되어 있다. 라즈베리파이에서 추출(Extracted)된 데이터가 데이터레이크에 저장되었다고 할 때, 데이터를 불러오고(Load) 레이블링하여 변형(Transform)된 형태로 feature store 에 저장하기 때문에 ELT라고 이름을 붙였다.
