# kavana-vscode

kavana script를 위한 syntax 색상 제공

## vscode kavana-script extension

1. npm -v, node -v
2. npm install -g yo generator-code
3. mkdir kavana-vscode
4. cd kavana-vscode
5. yo code ( cmd + r 에서 작업)
6. kvs.tmLanguage.json, language-configuration.json 편집
7. npm install -g vsce
   vsce package
8. kavana-script-0.0.1.vsix 만들어진다.

## vsix를 설치하는 방법

1. code gui에서 설치 : ctrl+shift+P -> Extensions: Install from VSIX. -> vsix선택
2. bash :  code --install-extension my-extension.vsix -> vscode 재시작
3. ctrl+shift+x ->  ... -> install from VSIX

### vsix관련 명령어

```bash
code --list-extensions --show-versions
code --uninstall-extension my-extension
```

### make.sh

- package.json의 버젼을 올리고
- vscode에서 기존에 설치된 것 제거 하고
- 새로운 것을 올린다.

```text
현재 나의 custom script language를 위한 vscode 확장 프로그램을 만드는데.
vsce package 라고 bash console에서 빌드하고 있어.
이것을 make.sh로 만들어 줄 수 있어.

1. package.json 에 있는 "version": "0.0.3",의 마지막 번호를 1증가 즉 package.json자체의 version을 증가 시켜서 버젼을 조정
2. vsce package 실행
3. 기존 code에 이미 설치되어 있는 kavana-script 확장 제거
4. 새로 만들어진 것 설치
```

## package.json

```json
{
  "name": "kavana-script",
  "displayName": "kavana-script",
  "description": "kavana script syntax highlighting for VSCode",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.98.0"
  },
  "categories": [
    "Programming Languages"
  ],
  "contributes": {
    "languages": [{
      "id": "kvs",
      "aliases": ["kavana", "kavana-script"],
      "extensions": ["kvs"],
      "configuration": "./language-configuration.json"
    }],
    "grammars": [{
      "language": "kvs",
      "scopeName": "source.kvs",
      "path": "./syntaxes/kvs.tmLanguage.json"
    }]
  }
}
```
