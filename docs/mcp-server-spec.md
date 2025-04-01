# MCP Server 実装仕様書

## 1. プロジェクト構造

```
ai-learning-platform/
├── backend/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py          # MCPサーバーメインクラス
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── chat_analyzer.py
│   │   │   ├── curriculum_generator.py
│   │   │   └── recommendation_updater.py
│   │   ├── resources/
│   │   │   ├── __init__.py
│   │   │   ├── profile_resource.py
│   │   │   └── curriculum_resource.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── profile.py
│   │   │   └── curriculum.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── openai_client.py
│   │       └── db.py
│   ├── requirements.txt
│   └── config.py              # 設定ファイル
```

## 2. 主要クラスと依存関係

### 2.1 AILearningServer

```python
class AILearningServer:
    def __init__(self):
        self.server = Server(
            {
                "name": "ai-learning-server",
                "version": "1.0.0"
            },
            {
                "capabilities": {
                    "tools": {},
                    "resources": {}
                }
            }
        )
        self.openai_client = OpenAIClient()
        self.db = Database()
```

### 2.2 ChatAnalyzer

```python
class ChatAnalyzer:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        
    async def analyze(self, messages: List[Dict]) -> LearningProfile:
        """メッセージを分析して学習プロファイルを生成"""
        pass
```

### 2.3 CurriculumGenerator

```python
class CurriculumGenerator:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        
    async def generate(self, profile: LearningProfile) -> Curriculum:
        """学習プロファイルからカリキュラムを生成"""
        pass
```

## 3. データモデル

### 3.1 LearningProfile

```python
@dataclass
class LearningProfile:
    id: str
    goals: List[str]
    skill_level: str
    available_time: str
    learning_style: str
    created_at: datetime
    updated_at: datetime
```

### 3.2 Curriculum

```python
@dataclass
class Curriculum:
    id: str
    user_id: str
    modules: List[Module]
    recommendations: Recommendations
    created_at: datetime
    updated_at: datetime

@dataclass
class Module:
    id: str
    title: str
    description: str
    duration: str
    difficulty: str
    resources: List[Resource]
    recommended_order: int

@dataclass
class Resource:
    type: str
    title: str
    url: str
```

## 4. OpenAI統合

### 4.1 システムプロンプト

#### プロファイル分析
```python
PROFILE_ANALYSIS_PROMPT = """
あなたは教育AIアシスタントです。
ユーザーとの会話から以下の情報を抽出してください：

1. 学習目標（具体的なスキルや資格）
2. 現在のスキルレベル
3. 利用可能な学習時間
4. 好みの学習スタイル

レスポンスは以下のJSON形式で返してください：
{
    "goals": ["目標1", "目標2"],
    "skill_level": "初級/中級/上級",
    "available_time": "週あたりの時間",
    "learning_style": "学習スタイルの特徴"
}
"""
```

#### カリキュラム生成
```python
CURRICULUM_GENERATION_PROMPT = """
以下の学習プロファイルに基づいて、
最適な学習カリキュラムを生成してください：

プロファイル情報：
- 目標: {goals}
- スキルレベル: {skill_level}
- 利用可能時間: {available_time}
- 学習スタイル: {learning_style}

以下の形式でカリキュラムを生成してください：
{
    "modules": [
        {
            "title": "モジュール名",
            "description": "説明",
            "duration": "所要時間",
            "difficulty": "難易度",
            "resources": [
                {
                    "type": "ビデオ/記事",
                    "title": "リソース名",
                    "url": "URL"
                }
            ],
            "recommended_order": 1
        }
    ],
    "recommendations": {
        "learning_path": "学習パス説明",
        "time_allocation": "時間配分指針",
        "focus_areas": ["重点分野1", "重点分野2"]
    }
}
"""
```

## 5. データベース連携

### 5.1 Database クラス

```python
class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    async def init(self):
        """データベースの初期化とテーブル作成"""
        pass
        
    async def create_profile(self, profile: LearningProfile):
        """学習プロファイルの保存"""
        pass
        
    async def get_profile(self, user_id: str) -> LearningProfile:
        """学習プロファイルの取得"""
        pass
        
    async def create_curriculum(self, curriculum: Curriculum):
        """カリキュラムの保存"""
        pass
        
    async def get_curriculum(self, user_id: str) -> Curriculum:
        """カリキュラムの取得"""
        pass
```

## 6. エラーハンドリング

```python
class MCPServerError(Exception):
    """MCPサーバーの基本エラークラス"""
    def __init__(self, code: str, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

class InvalidRequestError(MCPServerError):
    """無効なリクエストエラー"""
    pass

class ProcessingError(MCPServerError):
    """処理中のエラー"""
    pass

class OpenAIError(MCPServerError):
    """OpenAI API関連のエラー"""
    pass

class DatabaseError(MCPServerError):
    """データベース操作のエラー"""
    pass
```

## 7. 設定管理

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # OpenAI設定
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # データベース設定
    DATABASE_URL: str = "sqlite:///./learning.db"
    
    # サーバー設定
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 3001
    
    # レート制限設定
    RATE_LIMIT_ANALYZE: int = 60  # 回/時間
    RATE_LIMIT_GENERATE: int = 30  # 回/時間
    RATE_LIMIT_UPDATE: int = 120   # 回/時間
    
    class Config:
        env_file = ".env"
