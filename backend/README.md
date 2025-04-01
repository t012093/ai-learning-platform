# AI Learning Platform Backend

バックエンドサーバーの実装です。OpenAI GPT-4とMCP（Model Context Protocol）を使用して、パーソナライズされた学習体験を提供します。

## 技術スタック

- Python 3.9+
- FastAPI
- SQLite/PostgreSQL
- OpenAI API (GPT-4o-mini)
- Model Context Protocol (MCP)

## セットアップ手順

1. 仮想環境の作成
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集し、必要な値を設定
```

4. データベースの初期化
```bash
python scripts/init_db.py
```

5. サーバーの起動
```bash
python -m mcp_server
```

## テストの実行

### Unixシステム（Linux/macOS）での実行

```bash
# テスト実行スクリプトの権限設定
chmod +x scripts/run_tests.sh

# テストの実行
./scripts/run_tests.sh
```

### Windowsでの実行

```powershell
# テストの実行
.\scripts\run_tests.ps1
```

### 個別のテスト実行

```bash
# 特定のテストファイルを実行
pytest tests/test_openai_client.py -v

# 特定のテスト関数を実行
pytest tests/test_chat_analyzer.py::test_analyze_valid_input -v

# カバレッジレポート付きで実行
pytest --cov=mcp_server --cov-report=html
```

## テストの種類

### 1. ユニットテスト
- OpenAI APIクライアントのテスト
- チャット分析機能のテスト
- カリキュラム生成機能のテスト

### 2. 統合テスト
- データベース操作のテスト
- MCPサーバー全体のテスト

### 3. セキュリティテスト
- Banditによるセキュリティチェック
- 依存関係のセキュリティチェック

### 4. リンターとフォーマッター
- Flake8によるコードチェック
- Blackによるコードフォーマット
- MyPyによる型チェック

## テスト環境のカスタマイズ

### テストデータベースの設定
```bash
# SQLiteを使用する場合
export DATABASE_URL=sqlite:///./test.db

# PostgreSQLを使用する場合
export DATABASE_URL=postgresql://user:password@localhost:5432/test_db
```

### OpenAI APIのモック
```bash
# テスト用の設定
export TEST_MODE=true
export MOCK_OPENAI_RESPONSES=true
```

## 継続的インテグレーション

GitHub Actionsを使用して、以下のチェックを自動実行：

1. ユニットテストとカバレッジ
2. コードスタイルチェック
3. セキュリティスキャン
4. Dockerイメージのビルドテスト

## トラブルシューティング

### よくある問題

1. テストデータベースの接続エラー
```
解決: DATABASE_URLの設定を確認
```

2. 仮想環境の問題
```
解決: venv を削除して再作成
rm -rf venv
python -m venv venv
```

3. 依存関係のコンフリクト
```
解決: requirements.txtを最新化
pip freeze > requirements.txt
```

## 開発ガイドライン

### コーディング規約
- PEP 8に準拠
- 型ヒントを使用
- Docstringでドキュメント化

### テスト作成のガイドライン
- テストケースは独立していること
- モックを適切に使用
- エッジケースをカバー

### プルリクエスト前のチェックリスト
1. すべてのテストが通過
2. カバレッジが80%以上
3. リンターのエラーなし
4. セキュリティチェックのパス

## 貢献ガイド

1. 開発用ブランチの作成
2. テストの作成/更新
3. コードレビューの依頼
4. マージ後の確認

## ヘルプとサポート

- Issue Trackerの利用
- 開発者チームへの連絡
- ドキュメントの参照
