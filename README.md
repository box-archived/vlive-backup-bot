# vlive-backup
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/box-archived/vlive-backup)](https://github.com/box-archived/vlive-backup/releases)

Auto backup bot for vlive

VLIVE의 게시판의 게시물을 모두 다운로드 할 수 있는 봇입니다.

## 설치 및 실행
3.7 이상의 파이썬이 필요합니다.
파이썬은 [python.org](https://www.python.org/downloads/) 에서 다운받을 수 있으며, 
설치 방법은 [해당 링크](https://wikidocs.net/8) 의 방법을 따라 주시길 바랍니다.

### Windows 7, 8, 10
다운로드 한 소스코드의 압축을 풀고 __run.bat__ 파일을 실행합니다.

SmartScreen 보호 알림이 표시되었다면, <u>추가 정보</u> 버튼을 클릭하여 실행 버튼을 표시할 수 있습니다.
실행 버튼을 표시한 뒤 클릭하여 실행 해 주세요.

명령 프롬프트를 이용하여 실행 가능합니다.
명령 프롬프트를 열고 __run.bat__ 파일을 드래그 하여 실행할 수 있습니다.
```console
C:\> path\to\vlive-backup-bot\run.bat
```

### Other OS
리눅스, macOS 등의 운영체제에서는 Shell 스크립트를 이용해 실행 가능합니다.
sh 명령어로 __run.sh__ 파일을 실행합니다.
```console
$ sh path/to/vlive-backup-bot/run.sh
```

## 사용법
조작은 키보드와 마우스 모두 사용 가능합니다.

항목간 이동은 `방향키`, 메뉴간 이동은 `Tab` 키를 사용합니다.
마우스 스크롤은 지원하지 않으니 `PageUp`, `PageDown` 키를 이용 해 주세요.

다운로드 된 파일은 __downloaded__ 폴더 내에 `채널코드_게시판코드` 폴더로 분류되어 저장됩니다.

### 이메일 계정
VLIVE 백업 봇에서는 멤버십 포스트 저장을 위해 사용자의 이메일 계정을 필요로 합니다. 
이 정보는 사용자의 PC에 저장되며 VLIVE 웹사이트 로그인 이외의 용도로는 사용/전송되지 않습니다.

소셜 로그인 계정은 [프로필 설정 페이지](https://www.vlive.tv/my/profile) 에서 이메일과 비밀번호를 등록해야 합니다. 
로그인에는 해당 이메일과 비밀번호를 사용합니다.

로그인 정보는 __vlive-backup-bot.session__ 파일로 보관되며 더이상 사용하지 않을 시 안전하게 삭제하여 주세요.

### 간편모드
간편모드에서는 해당 게시판의 모든 게시물을 다운로드 합니다.
게시판의 주소를 입력하고 멤버십 여부를 선택하면 바로 다운로드가 진행됩니다.

### 고급모드
고급모드에서는 여러가지 설정을 이용하여 다운로드 할 수 있습니다. 사용 가능한 설정은 아래와 같습니다.

- 공식 비디오 다운로드: VLIVE VOD/영상 등을 저장합니다
- 포스트 다운로드: 공식 비디오가 아닌 일반 게시물을 저장합니다.
- 다운로드 개수: 게시판으로부터 가져올 항목의 수를 입력합니다. 0을 입력할 시 모든 항목을 가져오며, 
    0 이외의 숫자를 입력할 시 최근 영상으로 부터 해당 수 만큼의 항목을 가져옵니다.
- 게시물 선택: 로드 된 게시물 목록에서 다운로드 할 게시물을 선택합니다. 전체선택 버튼을 이용해 전체를 다운받을 수 있습니다.
