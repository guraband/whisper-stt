import Levenshtein
import re

def calculate_similarity(sentence1: str, sentence2: str) -> float:
    """
    두 문장의 Levenshtein 유사도를 계산하여 반환 (0 ~ 1 범위)
    """
    sentence1 = remove_special_characters(sentence1.lower())
    sentence2 = remove_special_characters(sentence2.lower())

    distance = Levenshtein.distance(sentence1, sentence2)
    max_len = max(len(sentence1), len(sentence2))

    if max_len == 0:
        return 1.0  # 두 문장이 모두 비어있다면 100% 일치

    similarity = 1 - (distance / max_len)
    return round(similarity, 4)

# 문장에서 특수문자를 제거하고 알파벳과 숫자만 남김
def remove_special_characters(sentence: str) -> str:
    # 공백이 두 개 이상인 경우 하나로 줄임
    sentence = re.sub(r'\s+', ' ', sentence)
    return re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
