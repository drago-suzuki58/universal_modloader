# Universal Modloader (UML)

[![Status](https://img.shields.io/badge/status-Alpha-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![DeepWiki](https://img.shields.io/badge/DeepWiki-drago--suzuki58%2Funiversal__modloader-blue.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==)](https://deepwiki.com/drago-suzuki58/universal_modloader)

日本語 | [English](README.md)

**AST注入を使用した、Mixin/HarmonyスタイルのPython用Modフレームワーク**

Universal Modloader は、単なるプラグインローダーではありません。

実行時に対象のアプリケーション（およびそのライブラリ）のソースコードを解析し、抽象構文木(AST)に直接コードを注入して再構築しています。

これにより、元のファイルを編集することなく、直感的なデコレータを使って関数のロジックを変更したり、関数内部のローカル変数を書き換えたりすることが可能になります。

> [!WARNING]
> **Alpha版 / 実験的テクニカルプレビュー**
>
> このプロジェクトは現在 **Alpha版** です。Pythonの動的性質の限界を探る **概念実証(PoC)** として機能します。
>
> 設計上、このツールは **実行時ASTインジェクション** を利用して、標準的な安全機構(スコープや不変性など)をバイパスし、「通常は不可能」な改造を可能にします。
>
> **本番環境での使用を意図していません。**
>
> このツールは、安全性や安定性よりも **パワーと柔軟性** を優先しています。APIや内部構造は予告なく変更される可能性があります。標準的なライブラリとしてではなく、研究用ツールやModdingフレームワークとして扱ってください。

## 特徴

- **実行時AST注入:**  
  `.py` ファイルを直接書き換える必要はありません。すべての変更はメモリ上で行われます。
- **ローカル変数の操作:**  
  `ctx` オブジェクトを通じて、関数内部のローカル変数にアクセス・変更が可能。
- **デコレータベースのAPI:**  
  JavaのMixinやC#のHarmony(Unity)にインスパイアされた、シンプルで強力な構文。
- **高い汎用性:**  
  メインスクリプトだけでなく、`import` されたライブラリ（標準ライブラリやサードパーティ製パッケージ）にもフック可能。

## 使用例

### HEAD

関数の**先頭**にコードを注入します。
メインのロジックが走る前に、引数やローカル変数を書き換えるのに最適です。

**ターゲットのコード (`main.py`)**

```python
def take_damage(amount):
    print(f"ぐわっ！ {amount} のダメージ！")
```

**Mod側のコード (`mods/my_mod.py` または `mods/my_mod/__init__.py`)**

```python
@uml.Inject("main", "take_damage", at=uml.At.HEAD())
def on_take_damage(ctx):
    # 変数 'amount' が使われる前に書き換える
    print("[Mod] ダメージを無効化します！")
    ctx["amount"] = 0
```

### TAIL

関数の**末尾**（returnの直前）にコードを注入します。
処理完了後のログ出力や、最終的な変数の状態を確認するのに便利です。

**ターゲットのコード (`main.py`)**

```python
def heal_player():
    hp = 100
    print("プレイヤーは回復した。")
```

**Mod側のコード (`mods/my_mod.py` または `mods/my_mod/__init__.py`)**

```python
@uml.Inject("main", "heal_player", at=uml.At.TAIL())
def on_heal_player(ctx):
    # ローカル変数 'hp' を読み取る
    current_hp = ctx["hp"]
    print(f"[Mod] 現在のHP: {current_hp}")
```

### RETURN

戻り値を強制的に書き換えます。

**ターゲットのコード (`main.py`)**

```python
def calculate_damage():
    return random.randint(5, 15)
```

**Mod側のコード (`mods/my_mod.py` または `mods/my_mod/__init__.py`)**

```python
import universal_modloader as uml

@uml.Inject("main", "calculate_damage", at=uml.At.RETURN())
def on_calculate_damage(ctx):
    print("[Mod] System: ダメージ計算を上書きしました！")
    # "__return__" に値をセットすると、元の戻り値の代わりにその値が返されます
    ctx["__return__"] = 0
```

この場合、`0` が返されます。

### INVOKE

ターゲット関数の中で行われている、特定の **関数呼び出し** に割り込みます。
関数が実行される **前** に引数を書き換えたり、実行された **後** に戻り値を書き換えたりするのに非常に強力です。

**ターゲットコード (`main.py`)**

```python
def main():
    # Modでこの "Hero" という名前を変えたい場合
    player = Player("Hero")
    print(f"ようこそ、 {player.name}！")
```

**Mod側のコード (`mods/my_mod.py` または `mods/my_mod/__init__.py`)**

```python
CUSTOM_NAME = "ModdedHero"

# 'main' 関数の中で呼ばれている 'Player(...)' という呼び出しをフックする
@uml.Inject("main", "main", at=uml.At.INVOKE("Player"))
def on_create_player(ctx):
    # ctx['args'] は Player() に渡される位置引数のリスト
    original_name = ctx['args'][0]
    
    # 引数を書き換える
    ctx['args'][0] = CUSTOM_NAME
    print(f"[Mod] プレイヤー名を '{original_name}' から '{CUSTOM_NAME}' に変更しました")
```

デフォルトでは、`INVOKE` は関数が呼ばれる **直前 (BEFORE)** に発動し、引数の変更が可能です。

`shift=uml.Shift.AFTER` を指定することで、関数が呼ばれた **直後** に発動し、戻り値を変更することもできます。

## インストールと使い方

Modを導入したいゲームまたはアプリのフォルダに、このリポジトリの `mods` フォルダと `loader.py` をコピーしてください。

その後、Pythonで `loader.py` を実行します。

### 基本的な使い方

何も指定しない場合、デフォルトで `main.py` を読み込んで起動します。

```bash
python loader.py
```

### 高度な使い方

起動するスクリプトを指定したり、ゲーム本体にコマンドライン引数を渡したりすることができます。

**構文:**

```bash
python loader.py [スクリプト名] [ゲーム用引数...]
```

**例:**
- **特定のスクリプトを起動する:**
    ```bash
    python loader.py my_game.py
    ```
    *注意: `my_game.py` を読み込んだ場合、Mod側の `@Inject` で指定するターゲット名は `"main"` ではなく `"my_game"` になります。*

- **ゲームに引数を渡して起動する:**
    ```bash
    python loader.py main.py --debug --windowed
    ```
    *(`--debug --windowed` はそのまま `main.py` に渡されます)*

## examplesの動かし方

`examples` フォルダ内のアプリは、リポジトリクローン時にはまだModがインストールされていません。

先述の方法でインストールするか、以下の初期化スクリプトを実行すると、自動的にすべてのサンプルにModがインストールされます。

- **Windows:** `initialize.bat`
- **Linux/Mac:** `initialize.sh`

## Q&A

### `unittest.mock`との違いは？

`unittest.mock`は主にテスト目的で使用されるモジュールであり、関数やオブジェクトの振る舞いを一時的に置き換えるためのものです。  
それに対してUniversal Modloaderは、実行時にコードを動的に変更するためのフレームワークであり、プログラムのModdingやカスタマイズを目的としています。

`unittest.mock`はテストにしか使用されないのに対し、Universal Modloaderは実際に使用するときの動作を変更するために使用されます。

### どのような場合に`unittest.mock`よりもUniversal Modloaderを使うべき？

例えばこのようなケースが挙げられます
- **第三者のPypiパッケージの関数の動作を変更したい場合:**  
  通常、ライブラリの動作を変更するには関数のオーバーライドやラップ、またはライブラリの直接的な書き換えが必要ですが、Universal Modloaderは外部から動作を変更できます。
- **権利があるコードを含めずに、パッチ部分のみを配布したい場合:**  
  権利が別にあり、再公開が法的に制限されているコードを含むことなく、パッチ部分のみを配布可能です。
- **複数のパッチを非破壊で適用したい場合:**  
  単純な上書きだと、複数のパッチが競合する可能性がありますが、Universal Modloaderは非破壊的に複数の変更を適用できます。
- **自身のアプリケーションにおいて追加のプラグインAPIを別途作成せずに、Modderが自由にコードを変更できるようにしたい場合:**  
  アプリケーションにプラグインAPIを追加することは、リファクタリングを必要とし、広範囲の変更を伴うことがあります。Universal Modloaderを使用すると、これだけでModderが自由にコードを変更できるようになるため、開発者の負担が軽減されます。
- **テスト以外の目的で、動作を変更したい場合:**  
  テスト以外の目的(プラグイン、チート、改造)でコードの動作を変更したい場合、Universal Modloaderはより適しています。

### `unittest.mock`で十分では？

確かに、`unittest.mock`はテストケースの記述という面では非常に強力です。しかし、それは主にテスト目的に特化しています。  
テスト以外の目的でコードの動作を変更したい場合、`unittest.mock`は設計上の制約があり、柔軟性に欠けることがあります。

また、`unittest.mock`は一時的な置き換えを目的としており、永続的な変更や複雑なModdingには向いていません。  
Universal Modloaderは、実行時にコードを動的に変更するためのフレームワークであり、Moddingやカスタマイズに特化しています。

### 本番環境では使えますか？

使用はできますが、推奨されません。
Universal Modloaderは現在Alpha版であり、安定性や安全性よりもパワーと柔軟性を優先しています。

また、そもそもAST注入自体がPythonの動的性質を利用しているため、予期せぬ動作やセキュリティリスクが存在します。  
Cheat Engineなどのツールをを使用するのと同様のリスクがあると考えてください。

### 対応しているPythonのバージョンは？

現在 Python 3.12 のみ検証済みです。  
ASTの特性上、Pythonのバージョンが変わるとASTの構造も変わる可能性があるため、他のバージョンでの動作は保証されません。

## ロードマップ / TODO

### コア機能 (Modding システム)

- [x] **注入ポイント(Injection Points)**
  - [x] `HEAD` (関数の先頭)
  - [x] `TAIL` (関数の末尾)
  - [x] `RETURN` (戻り値の書き換え)
  - [x] `INVOKE` (特定の関数呼び出しの前後)
- [ ] **Modメタデータ (マニフェスト)**: `__manifest__` 辞書または `manifest.json` をサポートし、名前・バージョン・作者・説明文を定義可能にする
- [ ] **Mod読み込み順序 / 優先度**: Modが適用される順序を制御する機能 (例: 整数の優先度設定や`load_after` 指定など)
- [ ] **依存関係管理**: 前提となるModを定義し、それらが確実に先に読み込まれるようにする
- [ ] **ライブラリ管理**: Modが必要とするPyPIパッケージを自動インストールする機能 (例: Modごとの`requirements.txt`や`pyproject.toml`対応)
- [ ] **競合検出**: 複数のModが同じ関数や変数を、互いに矛盾する形で書き換えようとした際に警告を出す

### 開発者エクスペリエンス (DX)

- [ ] **設定 (Config) API**: ユーザーがコードを直接編集しなくて済むよう、Modの設定(JSON/TOML/INI)を保存・読み込みする標準機能
- [ ] **ライフサイクルフック**: `on_load`、`on_ready`、`on_shutdown`などのイベントフック
- [ ] **ホットリロード**: ターゲットアプリを再起動することなくModを再読み込みする機能

### 安定性と安全性

- [ ] **エラー隔離**: 1つのModがクラッシュしてもアプリ全体が落ちないようにする(セーフモード)
- [ ] **バージョン互換性**: Modが対象アプリケーションまたはローダーの現在のバージョンと互換性があるかどうかを確認
