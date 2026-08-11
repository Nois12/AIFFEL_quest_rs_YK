# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 조영근
- 리뷰어 : 박희지


# PRT(Peer Review Template)
- [ ]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 워드 임베딩의 most_similar() 결과가 의미상 정상적으로 출력되었다.
      <img width="2407" height="163" alt="image" src="https://github.com/user-attachments/assets/443cc65b-de4c-4c85-8a80-c635f2bb7575" />
    - target, attribute set이 정상적으로 얻어지지 않았다.

      STEP 3의 출력이 `SF: ['가감없이', '가', '가건', '가가시의', '가거나', '가가멜의', ...]`, `가족: ['가가린이라는', '가가멜']`처럼 장르를 전혀 대표하지 못하는 단어로 채워져 있다. `X`의 shape은 `(21, V)` = (장르 문서 21개, 어휘 V개)로 **행이 장르, 열이 단어**다. `getcol(i)`는 i번째 단어의 문서별 점수(길이 21)를 가져오므로, 길이 V인 `features`와 zip하면 짧은 쪽에 맞춰 **앞 21개 단어만** 남는다. `get_feature_names_out()`은 사전순 정렬이라 그 21개가 `가, 가가멜, 가가멜과, 가감, 가감없이...`가 되었다.
      -> `scores = X[i].toarray().ravel()` (또는 `X.getrow(i)`)로 수정하면 해결된다.
      <img width="887" height="767" alt="image" src="https://github.com/user-attachments/assets/cb73444e-24bb-4789-beab-00c2f7330fdb" />
    - 21×21 = 441개 셀 중 대부분이 0.0이다. 히트맵도 SF 행/열을 제외하면 전부 0으로 채워져 있어 장르별 편향성을 읽어낼 수 없다.
     
      attribute set이 사전순 잡음 단어가 들어가 OOV 문제가 발생하였고 이를 0.0으로 반환한 것이 문제이다.
      <img width="1099" height="890" alt="image" src="https://github.com/user-attachments/assets/f03e748d-51a7-4d83-aa9f-ce2d9493c74d" />

    
- [x]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 각 STEP마다 코드 셀 직전에 마크다운 셀을 배치해 해당 단계의 목적을 한 문장으로 요약해두었다. STEP 3에는 "TF-IDF를 사용해 단어 셋을 만들면 중복된 단어가 많이 발생하는 문제를 볼 수 있음 → 중복 단어와 의미적으로 중복되는 표현을 정리 → 의미 축을 더 잘 대표하는 셋을 구성"이라고 적어, **왜** 그 처리를 하는지 적어두었다. 코드만 봐서는 알기 어려운 설계 의도를 파악하는 데 실제로 도움이 되었다.
      <img width="734" height="120" alt="image" src="https://github.com/user-attachments/assets/2990a8c0-9cbc-4293-b875-d9134265b3f6" />

        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 루브릭에 없는 자체 검증 셀을 추가했다.
      
      STEP 1에서 전체 코퍼스에 형태소 분석기를 돌리기 전에, 예시 문장 2개로 명사 추출이 의도대로 동작하는지 먼저 확인하는 셀을 따로 만들어두었다. 68,856문장짜리 코퍼스를 돌리기 전에 소규모로 동작을 검증하는 것은 좋은 실험 설계라고 생각한다. 결과도 `['영화','감동','사랑','작품']`으로 정확하게 나왔다.
      <img width="487" height="265" alt="image" src="https://github.com/user-attachments/assets/829a7967-ce24-4bd4-8cc6-6a173c623691" />
    - 장르별 명사 빈도 EDA를 추가로 수행했다.
      
      21개 장르 각각에 대해 명사 빈도 Top 20을 집계하고 전체 통합 빈도까지 함께 출력했다. 그 결과 전쟁 장르에서 `전쟁·전투·작전·독일군·부대`, 서부극에서 `서부·보안관·카우보이`, 성인물에서 `남편·관계·몸`처럼 장르 고유 어휘가 실제로 잡히는 것을 데이터로 확인할 수 있었다. 코퍼스 특성을 먼저 파악하고 넘어간 점이 좋았다.
      <img width="1096" height="1020" alt="image" src="https://github.com/user-attachments/assets/7832563b-3fd8-495d-8b35-ef754635cc3c" />


        
- [ ]  **4. 회고를 잘 작성했나요?**
    - 회고는 작성되어 있지 않다. 출력된 Heatmap을 해석한 부분이 있었으면 좋았을 것 같다.
        
- [x]  **5. 코드가 간결하고 효율적인가요?**
    - WEAT score를 계산하는 코드를 함수로 묶어서 작성하여 코드가 깔끔하다. 또한, 자주 사용되는 토큰화도 함수로 작성하여 효율적이다.
      <img width="630" height="502" alt="image" src="https://github.com/user-attachments/assets/76544824-11b1-462b-82ff-1a5f88e3af2c" />
      <img width="585" height="462" alt="image" src="https://github.com/user-attachments/assets/884bcf0d-6661-470a-af13-8bde482b8c94" />



# 회고(참고 링크 및 코드 개선)
코드를 깔끔하게 함수로 정리하고 초반에 STEP을 작성하셔서 구성을 이해하기 편했습니다.
아래는 개선한 코드입니다.
**1) STEP 3 — 행/열 수정**

```python
# 기존
scores = X.getcol(i).toarray().ravel()

# 수정
scores = X.getrow(i).toarray().ravel()
```
**2) STEP 3 — TF-IDF 입력을 명사 토큰으로**

현재 `genre_texts`는 원문 그대로라 `token_pattern=r"\b[가-힣]+\b"`가 어절 단위로 잘라 `가가린이라는`처럼 조사가 붙은 토큰이 나온다. Word2Vec은 명사로 학습했으므로 어휘가 어긋난다. STEP 1의 `noun_corpus_by_genre`를 재사용하면 Okt 재실행도 없어진다.

```python
# 기존
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

# 수정 — STEP 1의 명사 추출 결과를 재사용
genre_texts = []
for file_name in genre_txt:
    if file_name in noun_corpus_by_genre:
        nouns = [w for sent in noun_corpus_by_genre[file_name] for w in sent]
        genre_texts.append(' '.join(nouns))
```
