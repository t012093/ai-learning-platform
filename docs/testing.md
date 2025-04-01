# テスト手順書

## 1. テスト環境のセットアップ

### 1.1 テスト用の依存関係インストール
```bash
cd backend
pip install pytest pytest-asyncio pytest-cov httpx
```

### 1.2 テスト用の環境変数設定
```bash
# .env.testファイルを作成
cp .env.example .env.test

# テスト用の設定に編集
DATABASE_URL=sqlite:///./test.db
OPENAI_API_KEY=your-test-api-key
DEBUG_MODE=true
```

## 2. テストの実行

### 2.1 全てのテストを実行
```bash
# バックエンドディレクトリで実行
cd backend
pytest

# カバレッジレポート付きで実行
pytest --cov=mcp_server --cov-report=html
```

### 2.2 特定のテストを実行
```bash
# 特定のモジュールのテスト
pytest tests/test_chat_analyzer.py

# 特定のテストケース
pytest tests/test_chat_analyzer.py::test_analyze_valid_input
```

## 3. テストの種類

### 3.1 ユニットテスト
- `test_chat_analyzer.py`: チャット分析機能のテスト
- `test_curriculum_generator.py`: カリキュラム生成機能のテスト
- `test_recommendation_updater.py`: レコメンデーション更新機能のテスト

### 3.2 統合テスト
- `test_mcp_server.py`: MCPサーバー全体の統合テスト
- `test_database.py`: データベース操作の統合テスト

### 3.3 E2Eテスト
- `test_api_endpoints.py`: APIエンドポイントのE2Eテスト

## 4. テストデータ

### 4.1 フィクスチャー
`conftest.py`に以下のフィクスチャーが定義されています：
- `db_session`: テスト用DBセッション
- `test_profile_data`: テスト用プロファイルデータ
- `test_curriculum_data`: テスト用カリキュラムデータ
- `mock_openai_response`: OpenAI APIのモックレスポンス

### 4.2 モックの使用
```python
# OpenAI APIのモック例
@pytest.mark.asyncio
async def test_analyze_chat(mock_openai_response):
    mock_client = AsyncMock(spec=OpenAIClient)
    mock_client.analyze_chat.return_value = mock_openai_response
    # テストコード
```

## 5. テストケース

### 5.1 チャット分析テスト
- 正常な入力での分析
- 不正なレスポンスの処理
- APIエラーのハンドリング
- テキストからのプロファイル抽出

### 5.2 カリキュラム生成テスト
- 正常なプロファイルからの生成
- カリキュラムの最適化
- バリデーション
- エラーハンドリング

### 5.3 レコメンデーションテスト
- 進捗データに基づく更新
- 学習パターンの分析
- 最適化ロジック

## 6. CI/CDでのテスト実行

### 6.1 GitHub Actionsでの設定
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov=mcp_server
```

## 7. テストレポート

### 7.1 カバレッジレポートの生成
```bash
pytest --cov=mcp_server --cov-report=html --cov-report=term-missing
```

### 7.2 レポートの確認
- `htmlcov/index.html`: HTMLカバレッジレポート
- コンソール出力: 詳細なテスト結果

## 8. テストのデバッグ

### 8.1 詳細なログ出力
```bash
pytest -v --log-cli-level=DEBUG
```

### 8.2 特定の失敗テストの詳細
```bash
pytest -v -l --tb=long
```

## 9. テスト環境のメンテナンス

### 9.1 テストデータベースのクリーンアップ
```bash
# テスト実行前に自動的にクリーンアップ
@pytest.fixture(autouse=True)
async def cleanup_database():
    yield
    # テスト後のクリーンアップ処理
```

### 9.2 テストの依存関係管理
```bash
# requirements-test.txtの作成
pip freeze > requirements-test.txt
