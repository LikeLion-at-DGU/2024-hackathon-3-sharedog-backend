<div align="center" style="font-size: 1.5em;">
     <strong>&#x1F64B; 멋쟁이사자처럼 중앙 해커톤 '나눠주개' 백엔드 레포지토리 입니다. &#x1F64B;</strong>
</div>
<br>

## 👋 팀원 소개 - Backend Team

| 이름   | 전공           |
| ------ | -------------- |
| 김진우 | 산업시스템공학과 |
| 황채현 | 전자전기공학부   |

## 💻 프로젝트 설정& 가상환경 실행 방법

```
# 가상환경 만들기(처음에만)
python -m venv venv
# mac
#python3 -m venv venv
```
```
#가상환경 실행(파일 열 때마다)
source venv/Scripts/activate
# mac
# source venv/bin/activate
```
```
#가상환경 킨 후
pip install django

# 서비스에 설치되 패키지 다운 받는 법
pip install -r requirements.txt
```
```
# 가상환경 종료시키기
deactivate
```

## 🎯 Commit Convention

"태그:제목"의 형태이며, : 뒤에만 space가 있음에 유의합니다. ex) Feat: 메인페이지 추가
- `Feat`: 새로운 기능을 추가할 경우
- `Fix`: 버그를 고친 경우
- `Design`: CSS 등 사용자 UI 디자인 변경
- `Docs`: 문서 수정
- `!BREAKING CHANGE`: 커다란 API 변경의 경우 (ex API의 arguments, return 값의 변경, DB 테이블 변경, 급하게 치명적인 버그를 고쳐야 하는 경우)
- `!HOTFIX`: 급하게 치명적인 버그를 고쳐야하는 경우
- `Style`: 코드 포맷 변경, 세미 콜론 누락, 코드 수정이 없는 경우
- `Refactor`: 프로덕션 코드 리팩토링, 새로운 기능이나 버그 수정없이 현재 구현을 개선한 경우
- `Comment`: 필요한 주석 추가 및 변경
- `Test`: 테스트 추가, 테스트 리팩토링(프로덕션 코드 변경 X)
- `Chore`: 빌드 태스트 업데이트, 패키지 매니저를 설정하는 경우(프로덕션 코드 변경 X)
- `Rename`: 파일 혹은 폴더명을 수정하거나 옮기는 작업만인 경우
- `Remove`: 파일을 삭제하는 작업만 수행한 경우


## 💡 PR Convetion
ex) 💄 Design: 가로스크롤 개선 

| 아이콘 | 코드                       | 설명                     |
| ------ | -------------------------- | ------------------------ |
| 🎨     | :art                       | 코드의 구조/형태 개선    |
| ⚡️    | :zap                       | 성능 개선                |
| 🔥     | :fire                      | 코드/파일 삭제           |
| 🐛     | :bug                       | 버그 수정                |
| 🚑     | :ambulance                 | 긴급 수정                |
| ✨     | :sparkles                  | 새 기능                  |
| 💄     | :lipstick                  | UI/스타일 파일 추가/수정 |
| ⏪     | :rewind                    | 변경 내용 되돌리기       |
| 🔀     | :twisted_rightwards_arrows | 브랜치 합병              |
| 💡     | :bulb                      | 주석 추가/수정           |
| 🗃      | :card_file_box             | 데이버베이스 관련 수정   |

## 🛠️ 사용 언어
<div>
  <img src="https://img.shields.io/badge/html5-E34F26?style=flat&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/javascript-F7DF1E?style=flat&logo=javascript&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=React&logoColor=white" />
</div>
