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