import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from mcp_server.utils.db import Base

# テスト用のデータベースURL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_engine():
    """テスト用のデータベースエンジンを作成"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
        future=True
    )
    
    # テーブルの作成
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # テスト後にテーブルを削除
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # エンジンを閉じる
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    """テスト用のセッションを作成"""
    async_session = sessionmaker(
        db_engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session() as session:
        yield session  # トランザクションの制御はテストに任せる

# 以下のテストデータフィクスチャはそのまま
@pytest.fixture
def test_profile_data() -> dict:
    """テスト用プロファイルデータ"""
    return {
        "goals": ["Pythonプログラミングの習得", "ウェブアプリケーション開発"],
        "skill_level": "初級",
        "available_time": "週10時間",
        "learning_style": "実践的な演習重視"
    }

@pytest.fixture
def test_curriculum_data() -> dict:
    """テスト用カリキュラムデータ"""
    return {
        "modules": [
            {
                "title": "Python基礎",
                "description": "Python言語の基本構文と概念を学びます",
                "duration": "2週間",
                "difficulty": "初級",
                "resources": [
                    {
                        "type": "video",
                        "title": "Python入門講座",
                        "url": "https://example.com/python-intro"
                    }
                ],
                "recommended_order": 1
            }
        ],
        "recommendations": {
            "learning_path": "基礎から応用へ段階的に進む",
            "time_allocation": "1日2時間を目安に進める",
            "focus_areas": ["基本構文", "データ構造"]
        }
    }

@pytest.fixture
def mock_openai_response() -> dict:
    """OpenAI APIのモックレスポンス"""
    return {
        "content": '{"goals": ["Pythonプログラミングの習得"], "skill_level": "初級", "available_time": "週10時間", "learning_style": "実践的"}',
        "role": "assistant",
        "finish_reason": "stop"
    }
