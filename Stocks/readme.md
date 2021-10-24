## 프로젝트명 : 주가 데이터 분석 및 예측 모델 구현
#### 사용언어 : Python, 프레임워크 : Flask, DB : MySQL
#### 역할 : 데이터 가공, 모델링, 웹
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
