# AI Learning Platform

AIを活用したパーソナライズド学習プラットフォーム

## 概要

このプロジェクトは、OpenAI GPT-4o-miniとMCP（Model Context Protocol）を活用して、ユーザーに最適化された学習体験を提供するプラットフォームです。AIとの対話を通じて学習者のニーズを理解し、パーソナライズされたカリキュラムを提供します。

## 機能

- AIとの対話によるパーソナライズドアセスメント
- 動的なカリキュラム生成
- 進捗トラッキング
- リコメンデーション機能

## セットアップ手順

### Dockerを使用する場合（推奨）

1. 必要なツールのインストール
   - Docker
   - Docker Compose

2. 環境変数の設定
```bash
# バックエンド
cp backend/.env.example backend/.env
# 必要な環境変数を編集（特にOPENAI_API_KEY）
```

3. Docker Composeでの起動
```bash
docker-compose up -d
```

アプリケーションにアクセス：
- フロントエンド: http://localhost:3000
- バックエンド: http://localhost:3001
- データベース管理（Adminer）: http://localhost:8080

### 従来の方法でセットアップ

#### バックエンド（Python/FastAPI）

1. Python環境のセットアップ
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: `venv\Scripts\activate`
pip install -r requirements.txt
```

2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集
```

3. データベースの初期化
```bash
python scripts/init_db.py
```

4. サーバーの起動
```bash
python -m mcp_server
```

#### フロントエンド（Next.js）

1. Node.js環境のセットアップ
```bash
cd frontend
npm install
```

2. 開発サーバーの起動
```bash
npm run dev
```

## プロジェクト構造

```
ai-learning-platform/
├── backend/             # バックエンド実装
│   ├── mcp_server/     # MCPサーバー
│   ├── scripts/        # ユーティリティスクリプト
│   └── tests/          # テストコード
├── frontend/           # フロントエンド実装
│   ├── src/           # ソースコード
│   └── public/        # 静的ファイル
├── docs/              # プロジェクトドキュメント
├── docker-compose.yml # Docker構成
└── README.md         # このファイル
```

## 技術スタック

### バックエンド
- Python 3.9+
- FastAPI
- SQLite/PostgreSQL
- OpenAI API
- Model Context Protocol (MCP)

### フロントエンド
- Next.js 14
- TypeScript
- Tailwind CSS

## 開発ガイドライン

詳細なガイドラインは以下のドキュメントを参照してください：

- [アーキテクチャ設計](docs/architecture.md)
- [API仕様](docs/api-spec.md)
- [MCPサーバー仕様](docs/mcp-server-spec.md)
- [データベーススキーマ](docs/database-schema.md)

### コーディング規約
- バックエンド: PEP 8準拠
- フロントエンド: ESLint/Prettierの設定に準拠

### Git運用
- 機能開発: `feature/機能名`
- バグ修正: `fix/問題の概要`
- リファクタリング: `refactor/対象の概要`

## テスト

### バックエンド
```bash
cd backend
pytest
```

### フロントエンド
```bash
cd frontend
npm test
```

## デプロイ

### Docker環境（本番用）
```bash
# 本番環境用の構成でビルド
docker-compose -f docker-compose.prod.yml build

# 起動
docker-compose -f docker-compose.prod.yml up -d
```

### 手動デプロイ
詳細は[デプロイガイド](docs/deployment.md)を参照してください。

## トラブルシューティング

### よくある問題

1. Docker関連
```
エラー: ポートが既に使用されています
解決: 使用中のポートを確認し、必要に応じて停止またはポート番号を変更
```

2. 環境変数
```
エラー: 環境変数が設定されていません
解決: .envファイルの存在と内容を確認
```

3. データベース
```
エラー: データベースに接続できません
解決: DATABASE_URLの設定とデータベースの起動状態を確認
```

## 貢献ガイド

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'feat: Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 連絡先

- 開発者: Your Name
- Email: your.email@example.com

## 謝辞

- OpenAI - GPT-4o-mini API の提供
- Anthropic - Model Context Protocol (MCP)の開発
