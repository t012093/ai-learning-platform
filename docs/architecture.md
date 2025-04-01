# AI Learning Platform アーキテクチャドキュメント

## 概要
AI Learning Platformは、OpenAI GPT-4o-miniを活用したパーソナライズド学習プラットフォームです。MCPサーバーを介してAIとの対話を実現し、ユーザーに最適化された学習カリキュラムを提供します。

## システムアーキテクチャ

```mermaid
graph TB
    subgraph "Frontend (Next.js)"
        UI[Web UI]
        Chat[Chat Interface]
        Learn[Learning Interface]
    end

    subgraph "MCP Server"
        Server[AI Learning MCP Server]
        Tools[Tools]
        Resources[Resources]
    end

    subgraph "External Services"
        OpenAI[OpenAI API]
        DB[(SQLite DB)]
    end

    UI --> Server
    Chat --> Server
    Learn --> Server
    Server --> Tools
    Server --> Resources
    Tools --> OpenAI
    Tools --> DB
```

## コンポーネント構成

### フロントエンド
- Next.js v14を使用
- TypeScriptで実装
- Tailwind CSSでスタイリング

主要コンポーネント：
- ChatInterface: AIとの対話インターフェース
- LearningPage: 学習プログラム表示
- AssessmentPage: 学習アセスメント

### MCPサーバー
- Pythonで実装
- FastAPIをベースに使用
- OpenAI APIとの統合

提供ツール：
1. analyze_chat: チャット分析
2. generate_curriculum: カリキュラム生成
3. update_recommendations: レコメンデーション更新

### データベース
- SQLiteを使用（初期実装）
- 将来的にPostgreSQLへの移行を想定

## データフロー

1. ユーザーインタラクション
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant MCPServer
    participant OpenAI
    
    User->>Frontend: チャットメッセージ入力
    Frontend->>MCPServer: analyze_chat実行
    MCPServer->>OpenAI: チャット分析リクエスト
    OpenAI-->>MCPServer: 分析結果
    MCPServer->>MCPServer: 学習プロファイル生成
    MCPServer-->>Frontend: 分析結果返却
    Frontend->>User: UI更新
```

2. カリキュラム生成
```mermaid
sequenceDiagram
    participant MCPServer
    participant OpenAI
    participant DB
    
    MCPServer->>OpenAI: カリキュラム生成リクエスト
    OpenAI-->>MCPServer: カリキュラムデータ
    MCPServer->>DB: カリキュラム保存
    DB-->>MCPServer: 保存完了
```

## セキュリティ対策

### API認証
- OpenAI APIキーの安全な管理
- 環境変数での機密情報管理

### データ保護
- SQLiteデータベースのアクセス制御
- センシティブデータの暗号化

## スケーラビリティ

### 現状の制限
- ローカルSQLiteデータベース
- 単一サーバーでの運用

### 将来的な拡張計画
- PostgreSQLへの移行
- コンテナ化による水平スケーリング
- キャッシュ層の導入
