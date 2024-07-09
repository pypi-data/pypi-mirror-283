import re


class CONFIRM:
    def __init__(self):
        # 링크 패턴을 확인하는 정규표현식
        self.link_pattern = re.compile(
            r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')

    def match(self, text: str) -> bool:
        # 입력된 데이터가 링크 패턴과 일치하는지 확인
        return bool(self.link_pattern.match(text))

    def search(self, text: str) -> bool:
        # 입력된 데이터에 링크 패턴이 있는지 확인
        return bool(self.link_pattern.search(text))