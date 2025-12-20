# fastapi_evil_security

日本語 | [English](./README.md)

このサンプルは、 **Universal Modloader (UML)** がソースコードを一切変更することなく、実行時に堅牢なFastAPIアプリケーションのセキュリティを侵害できることを示しています。

## ターゲット

最新のセキュリティベストプラクティスを実装した堅牢なFastAPIアプリケーションです。

ソースコード自体に脆弱性はありません。

- **Stack:** FastAPI, SQLModel(SQLite), Pydantic
- **Behavior:**
  - パスワードは**Bcrypt**(passlib経由)を使用してハッシュ化されます。
  - 認証フローにはJWTトークンを用いた**OAuth2**を使用しています。
  - Pydanticモデルによる厳密な入力検証が行われます。

## Mod

Modはインポートプロセス中にPython ASTへ直接悪意のあるロジックを注入します。

- **マスターパスワード バックドア**:
  - `verify_password`関数にフックします。
  - 実際のパスワードに関わらず、入力されたパスワードが "master_password" であれば強制的に認証を成功させます。
- **認証情報スニッファー**:
  - `create_user`、`update_user`および`login_for_access_token`関数にフックします。
  - パスワードがBcryptでハッシュ化される前に、**平文のパスワード**を傍受してコンソールに出力します。

## 実行方法

### 1. Run Modded (With UML)

ローダー経由でターゲットを実行します。

```bash
cd examples/fastapi_evil_security
uv run loader.py app.py
```

**Try this:**  
1. `http://127.0.0.1:8000/docs` を開きます。
2. 新規ユーザーを登録します。
3. コンソールを確認してください。平文のパスワードが漏洩していることが確認できます。
4. ログアウトし、作成したユーザー名とパスワード "master_password" でログインを試行してください。認証に成功します。

### 2. Run Vanilla (Secure)

ターゲットを直接実行し、本来の挙動を確認します。

```bash
cd examples/fastapi_evil_security
uv run app.py
```

**Try this:**  
1. `http://127.0.0.1:8000/docs`を開きます。
2. パスワード "master_password" でログインを試行してください。失敗 (401 Unauthorized) することを確認できます。これはバックドアがソースコード上に存在しないことを証明しています。
