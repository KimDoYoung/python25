# VS Code 확장 프로그램에 오신 것을 환영합니다

## 📂 폴더 구성

- 이 폴더에는 확장 프로그램에 필요한 모든 파일이 포함되어 있습니다.
- **`package.json`** - 언어 지원을 선언하고, 구문 분석(grammar) 파일의 위치를 정의하는 매니페스트 파일입니다.
- **`syntaxes/kvs.tmLanguage.json`** - 토큰화를 수행하는 TextMate 구문(grammar) 파일입니다.
- **`language-configuration.json`** - 주석 및 괄호 등의 토큰을 정의하는 언어 설정 파일입니다.

## 🚀 바로 실행하기

1. `language-configuration.json`에서 언어 설정이 정확한지 확인하세요.
2. `F5` 키를 눌러 확장 프로그램이 로드된 새 창을 엽니다.
3. 새로운 파일을 생성하고 확장자가 지정한 언어와 일치하는지 확인하세요.
4. 구문 강조(syntax highlighting) 및 언어 설정이 정상적으로 작동하는지 테스트하세요.

## 🔄 변경 사항 적용

- 위의 파일을 수정한 후 디버그 툴바에서 확장 프로그램을 다시 실행할 수 있습니다.
- VS Code 창을 다시 로드(`Ctrl+R` 또는 Mac의 경우 `Cmd+R`)하여 변경 사항을 적용할 수도 있습니다.

## ✨ 추가적인 언어 기능 추가

- IntelliSense, 툴팁(hover), 유효성 검사(validator) 등의 기능을 추가하려면 VS Code 확장 프로그램 개발 문서를 참고하세요.  
  👉 [VS Code 확장 프로그램 문서](https://code.visualstudio.com/docs)

## 📥 확장 프로그램 설치

- 확장 프로그램을 Visual Studio Code에서 사용하려면 `<사용자 홈>/.vscode/extensions` 폴더에 복사한 후, VS Code를 다시 시작하세요.
- 확장 프로그램을 배포하고 공유하는 방법은 [VS Code 확장 프로그램 배포 문서](https://code.visualstudio.com/docs)에서 확인하세요.
