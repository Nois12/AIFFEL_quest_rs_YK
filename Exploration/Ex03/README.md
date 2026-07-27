# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 조영근
- 리뷰어 : 강지수


# PRT(Peer Review Template)
- [ ]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - **부분적으로 충족되었습니다.**
    - `BasicBlock`, `BottleneckBlock`, 공통 `ResNet` 클래스와
      `build_resnet34`, `build_resnet50`을 구현하고,
      `torchinfo.summary()`를 통해 ResNet-34와 ResNet-50의
      출력 구조를 확인했습니다.
    - CIFAR-10 데이터셋을 이용해 ResNet-34와 ResNet-50을 학습하고,
      epoch별 loss 및 validation accuracy를 기록한 결과도 제출되었습니다.
    - 15, 20, 30, 40 epoch 결과를 표로 정리하고 학습 loss와
      validation accuracy 그래프를 작성하여 결과 확인이 가능합니다.
    - 다만 직접 구현한 `build_resnet34()`와 `build_resnet50()`은
      구조 확인에 사용되었고, 실제 학습에서는 아래와 같이
      `torchvision.models`의 사전학습 모델을 새로 불러와 사용했습니다.

      ```python
      resnet34 = torchvision.models.resnet34(
          weights=torchvision.models.ResNet34_Weights.DEFAULT
      )

      resnet50 = torchvision.models.resnet50(
          weights=torchvision.models.ResNet50_Weights.DEFAULT
      )
      ```![Uploading 스크린샷 2026-07-27 오후 5.46.25.png…]()
<img width="1459" height="300" alt="스크린샷 2026-07-27 오후 5 45 36" src="https://github.com/user-attachments/assets/3e54d19e-cca8-4932-b684-7c754c686120" />
<img width="902" height="193" alt="스크린샷 2026-07-27 오후 5 45 24" src="https://github.com/user-attachments/assets/da72efcd-f516-429d-8169-8c7ef3c8143e" />

    
- [X]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 이번 프로젝트에서 가장 핵심적인 부분은
      `BasicBlock`, `BottleneckBlock`과 `_make_layer()` 구현이라고 생각합니다.
    - `BasicBlock`에서 입력값을 `identity`로 보관하고,
      convolution 연산 결과와 더하는 residual connection의 흐름이
      코드와 주석으로 명확하게 작성되어 있습니다.
      <img width="1174" height="486" alt="스크린샷 2026-07-27 오후 5 46 48" src="https://github.com/user-attachments/assets/00b6411b-ae9f-4782-9dfb-2b63a21f0a0c" />

        
        
- [X]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 단일 학습 결과만 제시하지 않고,
      15·20·30·40 epoch에서 모델별 성능을 비교하는
      추가 실험을 수행했습니다.
    <img width="516" height="603" alt="스크린샷 2026-07-27 오후 5 47 54" src="https://github.com/user-attachments/assets/9b867cc8-e124-4b0b-908d-249570056ef0" />


- [ ]  **4. 회고를 잘 작성했나요?**

- [ ]  **5. 코드가 간결하고 효율적인가요?**
    - `BasicBlock`, `BottleneckBlock`, `ResNet`을 각각 클래스로 분리하고,
      `_make_layer()`를 이용해 반복되는 블록 생성을 공통화한 부분은
      간결하고 확장 가능한 구조로 작성되었습니다.
    - 반면 ResNet-34와 ResNet-50의 학습 코드는 거의 같은 내용이
      두 번 반복되고 있습니다.


# 회고(참고 링크 및 코드 개선)
```
영근님의 코드는 BasicBlock과 BottleneckBlock을 직접 구성하고
`_make_layer()`로 전체 모델을 조립하여 ResNet의 구조를 이해하는 데
좋은 참고가 되었습니다. 특히 downsample을 통해 identity와 주 경로의
shape을 맞춘 뒤 더하는 흐름이 명확했습니다.

다만 residual connection의 효과를 확인하기 위한 Ablation Study에서는
VGG와 ResNet처럼 전체 구조가 다른 모델을 비교하기보다,
동일한 주 경로에서 residual connection만 켜고 끈 모델을 비교해야
성능 차이를 residual connection의 영향으로 더 명확히 해석할 수 있습니다.
```
