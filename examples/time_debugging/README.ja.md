# time_debugging

日本語 | [English](./examples/time_debugging/README.md)

**タイムトラベル・デバッグ** のデモンストレーションです。OSの時計を変更することなく、実行時にシステム時刻をモック（偽装）し、サブスクリプション管理などの時間に依存するロジックにおけるエッジケース（うるう年など）をテストする方法を示します。

## The Target

簡易的なサブスクリプションマネージャークラスです。

「現在」の時刻に基づいて有効期限の計算や有効性のチェックを行います。

- **Stack:** Python標準ライブラリ (`datetime`)
- **Behavior:**
  - `datetime.datetime.now()` を使用して現在の日付を取得します。
  - 特定の日付（例：うるう年の2月29日）において、ロジックの挙動が変わったり、計算ミスが発生したりする可能性があります。
  - 通常、特定の日付のテストを行うには、その日まで待つか、システム時刻を変更する必要があります。

## The Mod

Modは時刻ソースをモックし、アプリケーションに対して「現在はうるう年である」と信じ込ませます。

- **うるう年注入 (leap_year.py):**
  - `datetime.now()` （またはターゲットが使用する時刻取得メソッド）にフックします。
  - 戻り値を強制的にうるう年の特定日（例：2024年2月29日）に固定します。
  - うるう年計算処理を含むロジックの挙動を即座に検証可能にします。

## How to Run

### Prerequisite

`uv` がインストールされ、依存関係が同期されていることを確認してください。

### 1. Run Modded (Time Travel)

モックされた時刻でスクリプトを実行します。

```bash
cd examples/time_debugging
# Run the target via the Universal Modloader
uv run loader.py
```

**Try this:**  
出力される日付を確認してください。現実の時刻に関わらず、Modで定義された特定のうるう年の日付に固定されています。

### 2. Run Vanilla (Real Time)

実際のシステム時刻を使用してスクリプトを実行します。

```bash
cd examples/time_debugging
uv run main.py
```

**Try this:**  
出力が現在の正しい日付と時刻を反映していることを確認してください。
