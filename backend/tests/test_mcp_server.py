import pytest
import json
import sys
from unittest.mock import AsyncMock, patch, MagicMock
import uuid

# server.py のインポートをモックする
sys.modules['mcp'] = MagicMock()
sys.modules['mcp'].Server = MagicMock()
sys.modules['mcp'].StdioServerTransport = MagicMock()

# mcp_server のサーバーインポートの前にモックを設定
with patch.dict('sys.modules', {'mcp': sys.modules['mcp']}):
    from mcp_server.server import AILearningServer
from mcp_server.utils.openai_client import OpenAIClient
from mcp_server.utils.db import Database, LearningProfile

class MockOpenAIClient:
    """OpenAIクライアントのモック実装"""
    async def chat_completion(self, *args, **kwargs):
        # モックレスポンスを返す
        return {
            "choices": [{
                "message": {
                    "content": '{"goals": ["Pythonプログラミングの習得"], "skill_level": "初級", "available_time": "週10時間", "learning_style": "実践的"}'
                },
                "finish_reason": "stop"
            }]
        }

@pytest.fixture
async def mock_server(db_session):
    """モック化されたサーバーインスタンスを提供するフィクスチャ"""
    # OpenAIClient をモック化
    mock_openai = MockOpenAIClient()
    
    # Database クラスをモック化
    mock_db = MagicMock(spec=Database)
    # async_session メソッドを設定
    mock_db.async_session = lambda: db_session
    
    # サーバーインスタンスを作成し、モックを注入
    server = AILearningServer()
    server.openai_client = mock_openai
    server.db = mock_db
    
    # 各種ヘルパークラスもモック化
    server.chat_analyzer = AsyncMock()
    server.chat_analyzer.analyze_chat.return_value = {
        "profile": {
            "goals": ["Pythonプログラミングの習得"],
            "skill_level": "初級", 
            "available_time": "週10時間",
            "learning_style": "実践的"
        }
    }
    
    server.curriculum_generator = AsyncMock()
    server.curriculum_generator.generate_curriculum.return_value = {
        "curriculum": {
            "modules": [
                {
                    "title": "Python基礎",
                    "description": "Python言語の基本構文と概念",
                    "duration": "2週間",
                    "difficulty": "初級",
                    "recommended_order": 1
                }
            ]
        }
    }
    
    server.recommendation_updater = AsyncMock()
    server.recommendation_updater.update_recommendations.return_value = {
        "recommendations": {
            "learning_path": "基礎から応用へ",
            "focus_areas": ["データ型", "制御構文"]
        }
    }
    
    return server

@pytest.mark.asyncio
async def test_server_initialization(mock_server):
    """サーバーの初期化テスト"""
    assert mock_server.openai_client is not None
    assert mock_server.db is not None
    assert mock_server.chat_analyzer is not None
    assert mock_server.curriculum_generator is not None
    assert mock_server.recommendation_updater is not None

@pytest.mark.asyncio
async def test_list_tools(mock_server):
    """ツール一覧取得テスト"""
    # リクエストのモック
    request = AsyncMock()
    
    response = await mock_server.list_tools(request)
    
    assert isinstance(response, dict)
    assert "tools" in response
    assert len(response["tools"]) == 3
    
    # 必要なツールが含まれているか確認
    tool_names = [tool["name"] for tool in response["tools"]]
    assert "analyze_chat" in tool_names
    assert "generate_curriculum" in tool_names
    assert "update_recommendations" in tool_names

@pytest.mark.asyncio
async def test_call_tool_analyze_chat(mock_server):
    """チャット分析ツールのテスト"""
    # リクエストのモック
    request = AsyncMock()
    request.params = MagicMock()
    request.params.name = "analyze_chat"
    request.params.arguments = {
        "messages": [
            {"role": "user", "content": "Pythonを学びたいです"}
        ]
    }
    
    response = await mock_server.call_tool(request)
    
    assert isinstance(response, dict)
    assert "profile" in response
    assert "skill_level" in response["profile"]

@pytest.mark.asyncio
async def test_call_tool_generate_curriculum(mock_server, test_profile_data):
    """カリキュラム生成ツールのテスト"""
    # リクエストのモック
    request = AsyncMock()
    request.params = MagicMock()
    request.params.name = "generate_curriculum"
    request.params.arguments = {
        "profile": test_profile_data
    }
    
    response = await mock_server.call_tool(request)
    
    assert isinstance(response, dict)
    assert "curriculum" in response
    assert "modules" in response["curriculum"]

@pytest.mark.asyncio
async def test_call_tool_invalid(mock_server):
    """無効なツール呼び出しのテスト"""
    # リクエストのモック
    request = AsyncMock()
    request.params = MagicMock()
    request.params.name = "invalid_tool"
    request.params.arguments = {}
    
    with pytest.raises(Exception) as exc_info:
        await mock_server.call_tool(request)
    
    assert "Unknown tool" in str(exc_info.value)

@pytest.mark.asyncio
async def test_list_resource_templates(mock_server):
    """リソーステンプレート一覧のテスト"""
    # リクエストのモック
    request = AsyncMock()
    
    response = await mock_server.list_resource_templates(request)
    
    assert isinstance(response, dict)
    assert "resourceTemplates" in response

@pytest.mark.asyncio
async def test_read_resource(mock_server, test_profile_data):
    """リソース読み取りのテスト"""
    # プロファイルIDを生成
    profile_id = str(uuid.uuid4())
    
    # db.get_profile をモック
    mock_server.db.get_profile = AsyncMock()
    mock_server.db.get_profile.return_value = {
        "id": profile_id,
        "goals": test_profile_data["goals"],
        "skill_level": test_profile_data["skill_level"],
        "available_time": test_profile_data["available_time"],
        "learning_style": test_profile_data["learning_style"],
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None
    }
    
    # リクエストのモック
    request = AsyncMock()
    request.params = MagicMock()
    request.params.uri = f"learning://profiles/{profile_id}"
    
    response = await mock_server.read_resource(request)
    
    assert isinstance(response, dict)
    assert "contents" in response
    assert len(response["contents"]) > 0
    assert "text" in response["contents"][0]

@pytest.mark.asyncio
async def test_read_resource_invalid_uri(mock_server):
    """無効なURIでのリソース読み取りテスト"""
    # リクエストのモック
    request = AsyncMock()
    request.params = MagicMock()
    request.params.uri = "invalid://uri"
    
    with pytest.raises(Exception) as exc_info:
        await mock_server.read_resource(request)
    
    assert "Invalid resource URI" in str(exc_info.value)

@pytest.mark.asyncio
async def test_server_lifecycle():
    """サーバーのライフサイクルテスト"""
    server = AILearningServer()
    
    # サーバーの起動をモック
    with patch('mcp_server.server.StdioServerTransport') as mock_transport:
        mock_transport.return_value = AsyncMock()
        
        # 起動処理
        await server.run()
        
        # トランスポートの接続確認
        assert mock_transport.return_value.connect.called
        
        # サーバーの終了
        # Note: server.server が実際に存在する場合のみ実行
        if hasattr(server, 'server') and server.server:
            await server.server.close()
        
        # エラーがないことを確認
        assert True
