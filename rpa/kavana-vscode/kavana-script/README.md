# kavana-vscode

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
code --list-extensions
code --uninstall-extension my-extension
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