# modded_print

日本語 | [English](./examples/modded_print/README.md)

「Hello, World!」を出力するだけのシンプルなプログラムに対し、複数の独立したModを連鎖させ、引数や挙動を順番に書き換えていくデモンストレーションです。

## The Target

プログラミングの基礎中の基礎を表す、極めて最小限のPythonスクリプトです。

ソースコード自体には **動的なロジックは一切存在しません**。

- **Stack:** Python標準ライブラリ
- **Behavior:**
  - 単に `print("Hello, World!")` を実行するだけです。
  - フォーマット整形、タイムスタンプ、その他のロジックは一切含まれていません。

## The Mod

複数の独立したModが、実行時に同一のターゲット関数に対して **連鎖的(Chaining)** に介入し、挙動を変化させます。

- **タイムスタンプ注入 (add_time.py):**
  - `print` 関数にフックします。
  - 出力が標準出力に到達する *前* に、現在のシステム時刻を文字列の先頭に付与します。
- **レインボー化 (rainbow.py):**
  - テキスト文字列をANSIエスケープシーケンスでラップします。
  - 出力結果に動的な虹色のグラデーションを適用します。
- **サフィックス注入 (smile.py):**
  - 文字列の末尾にスマイリーフェイス `:)` を追加します。
  - 処理チェーンの最後尾でも引数の変更が可能であることを示しています。

![Rainbow Output](./examples/modded_print/screenshot.png)

## How to Run

### Prerequisite

`uv` がインストールされ、依存関係が同期されていることを確認してください。

### 1. Run Modded (With UML)

ローダーがターゲットにModを注入します。

```bash
cd examples/modded_print
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
コンソール出力を確認してください。単なるプレーンテキストではなく、カラフルで時刻付き、かつ笑顔で終わるメッセージが表示されます。

### 2. Run Vanilla (Original)

本来の挙動を確認します。

```bash
cd examples/modded_print
uv run main.py
```

**Try this:**  
装飾のない "Hello, World!" だけが出力されることを確認してください。
