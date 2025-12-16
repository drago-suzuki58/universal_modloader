# Universal Modloader (UML)

[![Status](https://img.shields.io/badge/status-Alpha-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

日本語 | [English](README.md)

**AST注入を使用した、Mixin/HarmonyスタイルのPython用Modフレームワーク**

Universal Modloader は、単なるプラグインローダーではありません。

実行時に対象のアプリケーション（およびそのライブラリ）のソースコードを解析し、抽象構文木(AST)に直接コードを注入して再構築しています。

これにより、元のファイルを編集することなく、直感的なデコレータを使って関数のロジックを変更したり、関数内部のローカル変数を書き換えたりすることが可能になります。

> [!WARNING]
> **Alpha Version / Experimental**
> 
> このプロジェクトは現在PoC(概念実証)段階のアルファ版です。APIや内部構造は予告なく変更される可能性があります。
> 
> 本番コードでは使用しないでください。

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

## Universal Modloaderのインストール

Modを導入したいゲームまたはアプリのフォルダに、このリポジトリの `mods` フォルダと `loader.py` をコピーしてください。

その後 `main.py` の代わりに `loader.py` を実行するだけです。

```bash
python loader.py
```

## examplesの動かし方

`examples` フォルダ内のアプリは、リポジトリクローン時にはまだModがインストールされていません。

先述の方法でインストールするか、以下の初期化スクリプトを実行すると、自動的にすべてのサンプルにModがインストールされます。

- **Windows:** `initialize.bat`
- **Linux/Mac:** `initialize.sh`

## ロードマップ / TODO

- [x] **注入ポイント (Injection Points)**
  - [x] `HEAD` (関数の先頭)
  - [x] `TAIL` (関数の末尾)
  - [x] `RETURN` (戻り値の書き換え)
  - [ ] `INVOKE` (特定の関数呼び出しの前後)
- [ ] その他様々な追加機能
