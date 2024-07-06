import logging


def get_logger(
    name: str,
    level=logging.DEBUG,
    fmt='%(levelname)s - (%(filename)s:%(lineno)d) %(message)s',
):
    """ 로거 생성 단순화를 위한 간단한 유틸 함수. 로거에 핸들러가 이미 부착되어 있는 경우
    이 함수가 여러 번 호출되더라도 핸들러를 변경하지 않습니다. 즉, `level` 과 `fmt` 인자가
    사용되지 않고 무시됩니다.
    """
    logger_ = logging.getLogger(name)
    if logger_.handlers:
        print(logger_.info('이미 로거에 핸들러가 있습니다. 로거 레벨과 포맷 스타일을 변경하지 않습니다.'))
        return logger_

    logger_.setLevel(level)
    handler_ = logging.StreamHandler()  # 콘솔에 로그 출력
    formatter_ = logging.Formatter(fmt)  # 로그 메시지 포맷
    handler_.setFormatter(formatter_)
    logger_.addHandler(handler_)
    logger_.debug('로거 `%s`을 생성했습니다.', name)
    return logger_
