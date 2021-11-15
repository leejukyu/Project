## 프로젝트명 : 주가 데이터 분석 및 예측 모델 구현
#### 개발기간 : 3개월, 인원 : 3명 
#### 사용언어 : <img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a> 프레임워크 : <img src="https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white"/></a> DB : <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/></a>
#### 역할 : 데이터 가공, 모델링, 웹
-----------------------------------------------------------------
### 개발 목적
- 코로나19 확산으로 거세진 개인 주식 투자 열풍
- 한국리서치의 조사 결과 절반 이상이 투자지식이 낮고 불안감을 느낌  

🚩 개인 투자자의 위험률 회피와 수익 극대화를 위한 보조프로그램을 개발
### 개발 과정
- 기획(약 2달)  
  - 주식에 영향을 주는 많은 요소가 있지만 사람들이 가장 많이 쓰는 차트를 보는 방식을 이용하기로 함
  - 지지선과 저항선에서 벗어나는 차트, 임의의 추세선을 그어 추세선의 각도 계산, 패턴 분석을 위한 yolo 등 다양한 방법을 시도
  - 반전형 데이터인 골든크로스, 데드크로스 구간을 이용
- 데이터 수집
  - 키움API : 1분봉
  - FinanceDataReader : 일봉
  - KRX : kospi 기업명과 기업코드
- 데이터 가공
  - 
  - 
- 모델 : CNN, loss : categorical_crossentropy
- 웹 : 원하는 기업명을 선택하면 DB에 저장되어 있는 행당 기업의 데이터 중 최신 20분 안에 반전형 
### 기술의 특장점
- 주식 전문가들이 실제로 사용하는 볼린저 밴드와 캔들 차트로 기술적 분석 방식을 이용한 매매, 매수 타이밍을 보여줌
- 급격한 변동이 발생할 때 빠르게 대응하기 위해 1분봉을 사용하였고 실시간으로 상승, 하락, 보합의 각각 확률을 보여주어 이용자의 판단을 도움  
<p align="center"><img src="https://user-images.githubusercontent.com/82499513/141749957-bde7c902-f13a-49f6-85dd-5a062f77e537.PNG"  width="300" height="400"/></img></p>

-----------------------------------------------------------------
#### 파일 설명
- Invester폴더 : 계속 쓰이는 함수 파일 넣어 놓음
  - DBUpdater : 기본 DB생성 및 키움 1분 데이터
  - func : 반전형을 찾기 위한 함수들
  - graph : 시각화 함수들
  - Login : 키움API에 들어가기 위한 로그인 함수
- try폴더 : 기획 단계에서 지나온 데이터 
- add_data : 일봉 데이터 등록(웹실행시 자동실행)
- app : 웹
- daily_data : 실시간 일분봉 데이터 가져오기
- final_cnn : 학습데이터 모델링한 파일
- img_cnn.h5 : 최적 모델 저장
- img_data.npy : 학습 이미지를 numpy 배열로 저장(final_cnn에서 실행한것)
- train : 반전형 데이터 확인 및 학습데이터 생성
#### 주의사항
- 키움API는 python 32bit에서만 실행됨
- tensorflow 등은 python 64bit에서 실행
- 실시간 데이터 받고 싶으면 daily_data python 32bit에서 실행 후 daily_modeling를 64bit에서 같이 실행, 2분 뒤부터 확인 가능
![(최종)오프콘_전시판넬_혁신성장사업_page-0001](https://user-images.githubusercontent.com/82499513/138584725-170d2b12-cdcb-4135-9234-d7b19de168ae.jpg)
