# コントリビューションガイド

バグの報告、新機能の提案、プルリクエスト等は大歓迎です！

## 環境構築

PromptGenの開発ではPython 3.8以上を使用します。

### Poetryのインストール

https://python-poetry.org/docs/#installation

### リポジトリのクローンと依存パッケージのインストール

```bash
$ git clone https://github.com/zawakin/promptgen.git
$ cd promptgen
$ poetry env use 3.8 # 仮想環境の作成
$ poetry install --with docs
```

### テストの実行

```bash
$ ./scripts/test.sh
```

## ドキュメントのビルド

```bash
$ poetry run python ./scripts/docs.py build-all
```

## ドキュメントのプレビュー

```bash
$ poetry run python ./scripts/docs.py live <lang>
```

`<lang>` には `ja` または `en` を指定します。
