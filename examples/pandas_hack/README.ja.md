# pandas_hack

日本語 | [English](./README.md)

ターゲットプロジェクトに依存関係を一切追加することなく、処理の遅いデータ処理スクリプトに可観測性ツール（プログレスバー、タイマー、データ検査）を注入するデモンストレーションです。

## The Target

データエンジニアリングのワークフローによくある典型的なデータ処理スクリプトです。

**可観測性(Observability)が欠如**しており、実行中に **ユーザーへのフィードバックが一切ありません**。

- **Stack:** Pandas, NumPy, Time (標準ライブラリ)
- **Behavior:**
  - `df.apply` ループ内で `time.sleep` を使用し、重い計算処理をシミュレートしています。
  - 実行中は数秒間沈黙したまま応答がなくなり、フリーズしているのか判別できません。
  - 進捗表示やパフォーマンス計測の機能を持っていません。

## The Mod

プロジェクトにその他の依存関係を追加することなく、実行時に可観測性ツールを直接注入します。

- **ネイティブ・プログレスバー (progress_bar.py):**
  - 高階関数(Higher-Order Function)のアプローチを用いて、`df.apply` に渡される関数をラップします。
  - 標準ライブラリと `sys.stdout` のみを使用し、CLIプログレスバーをリアルタイムに描画します。
- **実行時間計測 (check_execution_time.py):**
  - 処理関数の `HEAD` (開始) と `TAIL` (終了) にフックします。
  - 正確な実行時間を計測・表示し、パフォーマンスのボトルネック特定を支援します。
- **実行結果検査 (check_result.py):**
  - 処理終了時のローカル変数スコープ (`locals()`) にアクセスします。
  - 生成された DataFrame を盗み見し、プレビューを表示してデータの整合性を確認します。

## How to Run

### Prerequisite

`uv` がインストールされ、依存関係が同期されていることを確認してください。

### 1. Run Modded (With UML)

ローダーがターゲットにModを注入します。

```bash
cd examples/pandas_hack
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
コンソールに注目してください。プログレスバーが表示されてリアルタイムに進捗が進み、最後に実行時間とデータプレビューが表示されます。沈黙していたスクリプトが可視化される様子を確認してください。

### 2. Run Vanilla (Original)

本来の挙動を確認します。

```bash
cd examples/pandas_hack
uv run main.py
```

**Try this:**  
スクリプトが処理中に沈黙し、開始時と終了時以外は何も表示されないことを確認してください。
