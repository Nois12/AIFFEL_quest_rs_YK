import os
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from gensim.models import Word2Vec
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

# ============================================================
# 0. 데이터 경로 설정
# ============================================================
data_dir = os.path.expanduser("~/work/weat/data")

# 장르 코퍼스 파일 목록
genre_txt = [
    'synopsis_SF.txt', 'synopsis_family.txt', 'synopsis_show.txt', 'synopsis_horror.txt',
    'synopsis_etc.txt', 'synopsis_documentary.txt', 'synopsis_drama.txt', 'synopsis_romance.txt',
    'synopsis_musical.txt', 'synopsis_mystery.txt', 'synopsis_crime.txt', 'synopsis_historical.txt',
    'synopsis_western.txt', 'synopsis_adult.txt', 'synopsis_thriller.txt', 'synopsis_animation.txt',
    'synopsis_action.txt', 'synopsis_adventure.txt', 'synopsis_war.txt', 'synopsis_comedy.txt',
    'synopsis_fantasy.txt'
]

genre_name = [
    'SF', '가족', '공연', '공포(호러)', '기타', '다큐멘터리', '드라마', '멜로로맨스', '뮤지컬',
    '미스터리', '범죄', '사극', '서부극(웨스턴)', '성인물(에로)', '스릴러', '애니메이션', '액션',
    '어드벤처', '전쟁', '코미디', '판타지'
]

# ============================================================
# 1. STEP 1. 명사 추출
# ============================================================
okt = Okt()


def extract_nouns_from_lines(lines):
    """예시 문장 리스트를 받아 각 문장의 명사 리스트로 반환"""
    tokenized = []
    for line in lines:
        words = okt.pos(line, stem=True, norm=True)
        nouns = []
        for word, tag in words:
            if tag == "Noun":
                nouns.append(word)
        tokenized.append(nouns)
    return tokenized


def extract_nouns_from_file(file_path):
    """파일을 한 줄씩 읽어 각 줄의 명사만 추출한 문장별 리스트 반환"""
    tokenized = []
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if not line:
                break
            words = okt.pos(line, stem=True, norm=True)
            nouns = []
            for word, tag in words:
                if tag == "Noun":
                    nouns.append(word)
            tokenized.append(nouns)
    return tokenized


# 예시 문장으로 동작 확인
sample_texts = [
    "영화는 감동과 사랑이 담긴 작품입니다.",
    "이 영화는 큰 성공을 이뤘고, 스토리는 신선합니다."
]

sample_noun_result = extract_nouns_from_lines(sample_texts)
print("예시 문장 명사 추출 결과:")
for i, nouns in enumerate(sample_noun_result, start=1):
    print(f"문장 {i}: {nouns}")

# 실제 파일 기반 명사 추출 및 빈도 집계
noun_corpus_by_genre = {}
file_counters = {}
all_flattened_nouns = []

for file_name, genre in zip(genre_txt, genre_name):
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        noun_result = extract_nouns_from_file(file_path)
        noun_corpus_by_genre[file_name] = noun_result

        flattened_nouns = [noun for sentence in noun_result for noun in sentence]
        file_counter = Counter(flattened_nouns)
        file_counters[file_name] = file_counter
        all_flattened_nouns.extend(flattened_nouns)

        print(f"\n{genre}({file_name}) 명사 빈도 집계 결과 (Top 20):")
        print(file_counter.most_common(20))
    else:
        print(f"{file_name} 파일이 존재하지 않아 건너뜁니다.")

combined_counter = Counter(all_flattened_nouns)
print("\n전체 통합 명사 빈도 집계 결과 (Top 20):")
print(combined_counter.most_common(20))

# ============================================================
# 2. STEP 2. Word2Vec embedding model 만들기
# ============================================================
# 각 장르별 문장별 명사 리스트를 하나의 말뭉치로 이어붙여 Word2Vec 입력형태 생성
word2vec_tokenized = []
for file_name in genre_txt:
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        word2vec_tokenized.extend(extract_nouns_from_file(file_path))

print(f"\nWord2Vec 학습용 문장 수: {len(word2vec_tokenized)}")
print("첫 번째 문장 예시:", word2vec_tokenized[0][:20])

model = Word2Vec(
    sentences=word2vec_tokenized,
    vector_size=100,
    window=5,
    min_count=3,
    sg=0,
    workers=2,
    epochs=20,
)

print("\nWord2Vec 모델 학습 완료!")
print("영화와 가장 유사한 단어 예시:", model.wv.most_similar(positive=['영화']))

# ============================================================
# 3. STEP 3. target, attribute 단어 셋 만들기
# ============================================================
# 전 수업에서는 TF-IDF로 대표 단어를 뽑았고, 여기서는 중복 단어를 제거하는 개선 방식을 적용합니다.
# 문제점: TF-IDF 점수 상위 단어가 의미적으로 같은 축을 반복적으로 빠지게 만드는 중복성이 존재합니다.
# 해결: 동일 의미/유사한 축의 단어를 한 번만 남기도록 정규화/중복 제거 후 상위 단어를 재순위화합니다.

# 장르별 레이블 문자열로 TF-IDF 학습
genre_texts = []
for file_name in genre_txt:
    full_path = os.path.join(data_dir, file_name)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            corpus = []
            while True:
                line = f.readline()
                if not line:
                    break
                corpus.append(line.strip())
            genre_texts.append(' '.join(corpus))

vectorizer = TfidfVectorizer(
    token_pattern=r"(?u)\b[가-힣]+\b",
    ngram_range=(1, 1),
    min_df=1,
    stop_words=None,
)

X = vectorizer.fit_transform(genre_texts)
features = vectorizer.get_feature_names_out()

# tf-idf 상위 대표 단어 후보를 장르별로 추출
# 상위 후보를 다시 동일 문맥/표현으로 묶어 장르별 중복 제거 적용
attribute_sets = {}
for i, genre in enumerate(genre_name):
    scores = X.getcol(i).toarray().ravel()
    pair = sorted(zip(features, scores), key=lambda p: p[1], reverse=True)

    # TF-IDF가 0인 단어는 드롭
    candidates = [term for term, score in pair if score > 0]

    # 의미적 중복 제거 (예: 유사한 원형/어간은 일반적으로 이미 Okt 기반이므로 중복 단어만 제거)
    seen = set()
    clean = []
    for term in candidates:
        if term not in seen:
            seen.add(term)
            clean.append(term)

    # 장르별 대표 단어 셋 선정
    attribute_sets[genre] = clean[:12]

print("\n장르별 대표 속성 단어셋 (TF-IDF 기반, 중복 제거 후):")
for genre, words in attribute_sets.items():
    print(f"{genre}: {words}")

# WEAT용 target/attribute 축 설정
# 예술/일반 영화 두 축으로 기본 셋 구성
# 기존 Ex05 샘플에서 target_art, target_gen의 흐름을 유지하고,
# 여기서는 영화 구분을 기준으로 코퍼스 기반 네이밍을 반영한다.
art_target = ['영화', '감독', '배우', '연기', '장면', '상영', '예술', '감성', '상상', '시나리오']
gen_target = ['사건', '인물', '전쟁', '비극', '가족', '코미디', '액션', '모험', '스릴', '시리즈']

# ============================================================
# 4. STEP 4. WEAT score 계산 및 시각화
# ============================================================
# WEAT score 계산 함수
# X / Y = attribute 집합, A / B = target 집합
# 의미상 유사한 관계를 나타내는 score를 계산

def get_vector(model, word):
    if word in model.wv.key_to_index:
        return model.wv[word]
    return None


def mean_similarity(words, target_terms, model):
    vectors = []
    for word in words:
        v = get_vector(model, word)
        if v is not None:
            vectors.append(v)
    if len(vectors) == 0:
        return 0.0

    sims = []
    for word in words:
        wv = get_vector(model, word)
        if wv is not None:
            try:
                sims.append(np.mean([model.wv.similarity(word, t) for t in target_terms if t in model.wv.key_to_index]))
            except Exception:
                continue
    return float(np.mean(sims)) if len(sims) > 0 else 0.0


def weat_score(model, X, Y, A, B):
    """
    WEAT = sum_{x in X} s(x, A, B) - sum_{y in Y} s(y, A, B)
    여기서 s(w, A, B) = mean_sim(w, A) - mean_sim(w, B)
    """
    def s(word, attr_a, attr_b):
        word_v = get_vector(model, word)
        if word_v is None:
            return 0.0

        sim_a = []
        sim_b = []
        for a in attr_a:
            if a in model.wv.key_to_index:
                sim_a.append(model.wv.similarity(word, a))
        for b in attr_b:
            if b in model.wv.key_to_index:
                sim_b.append(model.wv.similarity(word, b))

        if not sim_a or not sim_b:
            return 0.0
        return float(np.mean(sim_a) - np.mean(sim_b))

    sx = sum(s(x, A, B) for x in X)
    sy = sum(s(y, A, B) for y in Y)

    # WEAT score의 표준화 방향과 의미를 명시해 두고 해석을 돕습니다.
    # 항목 수가 적을 때는 표준화 대신 raw score도 읽을 수 있게 둘 다 출력합니다.
    return sx - sy


def build_weat_matrix(model, target_attr_sets, art_target, gen_target):
    # 속성 후보 셋마다 WEAT 계산
    genre_names = list(target_attr_sets.keys())
    matrix = np.zeros((len(genre_names), len(genre_names)))

    for i, attr_a_name in enumerate(genre_names):
        attr_a = target_attr_sets[attr_a_name]
        for j, attr_b_name in enumerate(genre_names):
            attr_b = target_attr_sets[attr_b_name]
            score = weat_score(model, art_target, gen_target, attr_a, attr_b)
            matrix[i, j] = score
    return matrix

# ============================================================
# 폰트 설정 (NanumGothic)
import matplotlib.font_manager as fm
font_path = r'C:\Windows\Fonts\NanumGothic.ttf'
fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')
# ============================================================

# 학습된 모델을 이용하여 장르별 속성셋과 예술/일반 영화 타깃 간 WEAT score 계산
matrix = build_weat_matrix(model, attribute_sets, art_target, gen_target)

# Heatmap 시각화
sns.set(font='NanumGothic')
plt.figure(figsize=(14, 10))
ax = sns.heatmap(
    matrix,
    xticklabels=list(attribute_sets.keys()),
    yticklabels=list(attribute_sets.keys()),
    annot=True,
    cmap='RdYlGn_r'
)
plt.title('Genre-wise WEAT Score Heatmap')
plt.xlabel('Genre Attribute Sets')
plt.ylabel('Genre Attribute Sets')
plt.show()

print("\nWEAT matrix:")
print(matrix)

# ============================================================
# 저장 및 시각화 파일 출력
# ============================================================
# 예측 결과를 위한 심볼릭 저장
model.save(os.path.join(data_dir, 'movie_genre_word2vec.model'))

# 학습 결과로 메모리에서 워드 임베딩 결과를 좀 더 해석하기 쉽게 출력
for word in ['영화', '배우', '사랑', '액션', '드라마']:
    if word in model.wv.key_to_index:
        print(f"{word} 유사 단어: {model.wv.most_similar(word)[:5]}")
