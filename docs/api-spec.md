# API仕様書

## MCPサーバーAPI

### 1. ツール (Tools)

#### 1.1 analyze_chat
チャットメッセージを分析して学習プロファイルを生成します。

**リクエスト**
```json
{
    "messages": [
        {
            "role": "user",
            "content": "string"
        }
    ]
}
```

**レスポンス**
```json
{
    "profile": {
        "goals": ["string"],
        "skill_level": "string",
        "available_time": "string",
        "learning_style": "string"
    }
}
```

#### 1.2 generate_curriculum
学習プロファイルに基づいてカリキュラムを生成します。

**リクエスト**
```json
{
    "profile": {
        "goals": ["string"],
        "skill_level": "string",
        "available_time": "string",
        "learning_style": "string"
    }
}
```

**レスポンス**
```json
{
    "curriculum": {
        "modules": [
            {
                "id": "string",
                "title": "string",
                "description": "string",
                "duration": "string",
                "difficulty": "string",
                "resources": [
                    {
                        "type": "string",
                        "title": "string",
                        "url": "string"
                    }
                ],
                "recommended_order": "number"
            }
        ],
        "recommendations": {
            "learning_path": "string",
            "time_allocation": "string",
            "focus_areas": ["string"]
        }
    }
}
```

#### 1.3 update_recommendations
学習進捗に基づいてレコメンデーションを更新します。

**リクエスト**
```json
{
    "progress": {
        "user_id": "string",
        "completed_modules": ["string"],
        "assessment_results": {
            "module_id": "string",
            "score": "number"
        }
    }
}
```

**レスポンス**
```json
{
    "recommendations": {
        "next_modules": ["string"],
        "focus_areas": ["string"],
        "adjusted_difficulty": "string"
    }
}
```

### 2. リソース (Resources)

#### 2.1 学習プロファイル
```
URI Template: learning://profiles/{user_id}
Method: GET
```

**レスポンス**
```json
{
    "user_id": "string",
    "profile": {
        "goals": ["string"],
        "skill_level": "string",
        "available_time": "string",
        "learning_style": "string"
    },
    "created_at": "string",
    "updated_at": "string"
}
```

#### 2.2 カリキュラム
```
URI Template: learning://curriculum/{user_id}
Method: GET
```

**レスポンス**
```json
{
    "user_id": "string",
    "curriculum": {
        "modules": [...],
        "recommendations": {...}
    },
    "last_updated": "string"
}
```

## エラーレスポンス

すべてのエンドポイントで共通のエラーレスポンス形式を使用します：

```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    }
}
```

### エラーコード
- `INVALID_REQUEST`: リクエストパラメータが不正
- `PROCESSING_ERROR`: 処理中のエラー
- `OPENAI_ERROR`: OpenAI API関連のエラー
- `DATABASE_ERROR`: データベース操作のエラー
- `NOT_FOUND`: リソースが見つからない
- `UNAUTHORIZED`: 認証エラー

## レート制限

- OpenAI APIの制限に準拠
- ユーザーごとの制限：
  - analyze_chat: 60回/時間
  - generate_curriculum: 30回/時間
  - update_recommendations: 120回/時間
