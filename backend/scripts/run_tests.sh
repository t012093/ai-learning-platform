#!/bin/bash

# 色の定義
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AI Learning Platform テストを実行します${NC}"
echo "=================================="

# 現在のディレクトリを確認
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}エラー: backendディレクトリで実行してください${NC}"
    exit 1
fi

# 環境変数の設定
export PYTHONPATH=$PYTHONPATH:$(pwd)
export TEST_MODE=true
export $(cat .env.test | grep -v '^#' | xargs)

# 仮想環境の確認と依存関係のインストール
if [ ! -d "venv" ]; then
    echo -e "${BLUE}仮想環境をセットアップします...${NC}"
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# フォーマッターとリンターの実行
echo -e "\n${BLUE}1. コードフォーマットをチェックしています...${NC}"
black --check mcp_server tests
if [ $? -ne 0 ]; then
    echo -e "${RED}コードフォーマットが正しくありません。'black'を実行してください。${NC}"
    exit 1
fi

echo -e "\n${BLUE}2. リンターを実行しています...${NC}"
flake8 mcp_server tests
if [ $? -ne 0 ]; then
    echo -e "${RED}リンターチェックが失敗しました。${NC}"
    exit 1
fi

echo -e "\n${BLUE}3. 型チェックを実行しています...${NC}"
mypy mcp_server
if [ $? -ne 0 ]; then
    echo -e "${RED}型チェックが失敗しました。${NC}"
    exit 1
fi

# テストデータベースの準備
echo -e "\n${BLUE}4. テストデータベースを準備しています...${NC}"
if [ -f "test.db" ]; then
    rm test.db
fi

# テストの実行
echo -e "\n${BLUE}5. テストを実行しています...${NC}"

# 個別のテストを順番に実行
echo -e "\n${BLUE}5.1 OpenAIクライアントのテスト${NC}"
pytest tests/test_openai_client.py -v

echo -e "\n${BLUE}5.2 データベースのテスト${NC}"
pytest tests/test_database.py -v

echo -e "\n${BLUE}5.3 MCPサーバーのテスト${NC}"
pytest tests/test_mcp_server.py -v

# カバレッジレポートの生成
echo -e "\n${BLUE}6. カバレッジレポートを生成しています...${NC}"
pytest --cov=mcp_server --cov-report=html --cov-report=term-missing

# テスト結果の確認
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ すべてのテストが成功しました${NC}"
    echo -e "カバレッジレポート: htmlcov/index.html"
else
    echo -e "\n${RED}✗ テストが失敗しました${NC}"
    exit 1
fi

# クリーンアップ
deactivate
