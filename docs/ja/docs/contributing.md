# コントリビューションガイド

バグの報告、新機能の提案、プルリクエスト等は大歓迎です！

## 環境構築

PromptoGenの開発ではPython 3.8以上を使用します。

### Poetryのインストール

https://python-poetry.org/docs/#installation

### リポジトリのクローンと依存パッケージのインストール

```bash
$ git clone https://github.com/zawakin/promptogen.git
$ cd promptogen
$ poetry install --with docs
```

すると、リポジトリのルートディレクトリに `.venv` が作成されます。

Poetryによって作成された仮想環境を使用することをおすすめします。
仮想環境をアクティブにするには、以下のコマンドを実行してください：

```bash
$ poetry shell
```

詳細については、https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment を参照してください。

### テストの実行

```bash
$ ./scripts/test.sh
```

### カバレッジ付きでのテスト実行

```bash
$ ./scripts/coverage.sh
```

### Lintの実行

```bash
$ ./scripts/lint.sh
```

### 自動修正付きでのLintの実行

```bash
$ ./scripts/lint.sh --fix
```

## ドキュメントのプレビュー

```bash
$ poetry run python ./scripts/docs.py live <lang>
```

`<lang>`には `ja`（日本語）または `en`（英語）を指定してください。

## ドキュメントのビルド（メンテナ向け）

```bash
$ poetry run python ./scripts/docs.py build-all
```

## ドキュメントのサーバー起動（メンテナ向け）

```bash
$ poetry run python ./scripts/docs.py serve
```
