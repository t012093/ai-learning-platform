# テスト実行スクリプト（Windows用）

# 色の定義
$Green = "`e[32m"
$Red = "`e[31m"
$Blue = "`e[34m"
$Reset = "`e[0m"

Write-Host "${Blue}AI Learning Platform テストを実行します${Reset}"
Write-Host "=================================="

# 現在のディレクトリを確認
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "${Red}エラー: backendディレクトリで実行してください${Reset}"
    exit 1
}

# 環境変数の設定
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
$env:TEST_MODE = "true"

# .env.testファイルから環境変数を読み込む
Get-Content .env.test | ForEach-Object {
    if ($_ -match '^([^#].*?)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "env:$name" -Value $value
    }
}

# 仮想環境の確認と依存関係のインストール
if (-not (Test-Path "venv")) {
    Write-Host "${Blue}仮想環境をセットアップします...${Reset}"
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}
else {
    .\venv\Scripts\Activate.ps1
}

# フォーマッターとリンターの実行
Write-Host "`n${Blue}1. コードフォーマットをチェックしています...${Reset}"
black --check mcp_server tests
if ($LASTEXITCODE -ne 0) {
    Write-Host "${Red}コードフォーマットが正しくありません。'black'を実行してください。${Reset}"
    exit 1
}

Write-Host "`n${Blue}2. リンターを実行しています...${Reset}"
flake8 mcp_server tests
if ($LASTEXITCODE -ne 0) {
    Write-Host "${Red}リンターチェックが失敗しました。${Reset}"
    exit 1
}

Write-Host "`n${Blue}3. 型チェックを実行しています...${Reset}"
mypy mcp_server
if ($LASTEXITCODE -ne 0) {
    Write-Host "${Red}型チェックが失敗しました。${Reset}"
    exit 1
}

# テストデータベースの準備
Write-Host "`n${Blue}4. テストデータベースを準備しています...${Reset}"
if (Test-Path "test.db") {
    Remove-Item "test.db"
}

# テストの実行
Write-Host "`n${Blue}5. テストを実行しています...${Reset}"

# 個別のテストを順番に実行
Write-Host "`n${Blue}5.1 OpenAIクライアントのテスト${Reset}"
pytest tests/test_openai_client.py -v

Write-Host "`n${Blue}5.2 データベースのテスト${Reset}"
pytest tests/test_database.py -v

Write-Host "`n${Blue}5.3 MCPサーバーのテスト${Reset}"
pytest tests/test_mcp_server.py -v

# カバレッジレポートの生成
Write-Host "`n${Blue}6. カバレッジレポートを生成しています...${Reset}"
pytest --cov=mcp_server --cov-report=html --cov-report=term-missing

# テスト結果の確認
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n${Green}✓ すべてのテストが成功しました${Reset}"
    Write-Host "カバレッジレポート: htmlcov/index.html"
}
else {
    Write-Host "`n${Red}✗ テストが失敗しました${Reset}"
    exit 1
}

# クリーンアップ
deactivate
