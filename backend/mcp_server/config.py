import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_engine():
    # Use the correct async SQLite URL format with aiosqlite driver
    engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db", 
        echo=True, 
        future=True
    )
    
    # Create all tables here or in your init code
    # await create_tables(engine)
    
    yield engine
    
    # Dispose of the engine at the end
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    """Creates a new database session for testing."""
    async_session = sessionmaker(
        db_engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session() as session:
        yield session
        # Roll back at the end of each test
        await session.rollback()

@pytest.fixture
def test_profile_data():
    """テスト用の学習プロファイルデータ"""
    return {
        "goals": "Pythonのウェブ開発マスター",
        "skill_level": "中級",
        "available_time": "週10時間",
        "learning_style": "プロジェクトベース",
        "preferences": "動画学習",
        "email": "test@example.com"
    }

@pytest.fixture
def test_curriculum_data():
    """テスト用のカリキュラムデータ"""
    return {
        "title": "Pythonウェブ開発カリキュラム",
        "description": "Pythonを使用してウェブアプリケーションを構築する方法を学びます",
        "estimated_duration": "3ヶ月",
        "skill_level": "中級",
        "modules": [
            {
                "title": "Python基礎",
                "description": "Python言語の基本構文と概念を学びます",
                "duration": "2週間",
                "difficulty": "初級",
                "recommended_order": 1,
                "resources": [
                    {
                        "title": "Python公式チュートリアル",
                        "url": "https://docs.python.org/ja/3/tutorial/",
                        "type": "document"
                    }
                ]
            }
        ]
    }