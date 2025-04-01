import pytest
import json
import sys
import types
from unittest.mock import AsyncMock, patch, MagicMock

import uuid

# mcp モジュールとその型をモック化
sys.modules['mcp'] = MagicMock()
sys.modules['mcp'].Server = MagicMock()
sys.modules['mcp'].StdioServerTransport = MagicMock()

# mcp.types モジュールをモック化
mcp_types_mock = MagicMock()
mcp_types_mock.ListToolsRequestSchema = MagicMock()
mcp_types_mock.ListResourceTemplatesRequestSchema = MagicMock()
mcp_types_mock.CallToolRequestSchema = MagicMock()
mcp_types_mock.ReadResourceRequestSchema = MagicMock()
mcp_types_mock.McpError = type('McpError', (Exception,), {})
mcp_types_mock.ErrorCode = MagicMock()
mcp_types_mock.ErrorCode.MethodNotFound = "METHOD_NOT_FOUND"
mcp_types_mock.ErrorCode.InvalidRequest = "INVALID_REQUEST"
mcp_types_mock.ErrorCode.InternalError = "INTERNAL_ERROR"

sys.modules['mcp.types'] = mcp_types_mock

# Settings クラスをモック化
class MockSettings:
    OPENAI_API_KEY = "test-api-key"
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# config モジュールをモック化
config_mock = types.ModuleType('config')
config_mock.Settings = MockSettings
sys.modules['mcp_server.config'] = config_mock

# ここでサーバーをインポート
with patch('mcp_server.server.Settings', MockSettings):
    from mcp_server.server import AILearningServer
from unittest import mock

# OpenAIClientのモック
class MockOpenAIClient:
    async def chat_completion(self, *args, **kwargs):
        return {
            "choices": [{
                "message": {
                    "content": '{"goals": ["Pythonプログラミングの習得"], "skill_level": "初級", "available_time": "週10時間", "learning_style": "実践的"}'
                },
                "finish_reason": "stop"
            }]
        }

# ChatAnalyzerのモック
class MockChatAnalyzer:
    async def analyze(self, messages):
        return {
            "goals": ["Pythonプログラミングの習得"],
            "skill_level": "初級", 
            "available_time": "週10時間",
            "learning_style": "実践的"
        }

# CurriculumGeneratorのモック
class MockCurriculumGenerator:
    async def generate(self, profile):
        return {
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

# RecommendationUpdaterのモック
class MockRecommendationUpdater:
    async def update(self, progress):
        return {
            "learning_path": "基礎から応用へ",
            "focus_areas": ["データ型", "制御構文"]
        }

# Databaseのモック
class MockDatabase:
    async def init(self):
        pass
    
    async def get_profile(self, user_id):
        return {
            "id": user_id,
            "goals": ["Pythonプログラミングの習得"],
            "skill_level": "初級",
            "available_time": "週10時間",
            "learning_style": "実践的",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": None
        }
    
    async def get_curriculum(self, user_id):
        return {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "modules": [
                {
                    "title": "Python基礎",
                    "description": "基本構文とデータ型",
                    "duration": "2週間",
                    "difficulty": "初級",
                    "recommended_order": 1
                }
            ],
            "recommendations": {
                "learning_path": "基礎から応用へ",
                "focus_areas": ["データ型", "制御構文"]
            },
            "created_at": "2023-01-01T00:00:00",
            "updated_at": None
        }

@pytest.fixture
def mock_server():
    """モック化されたサーバーインスタンスを提供するフィクスチャ"""
    with mock.patch('mcp_server.server.OpenAIClient', return_value=MockOpenAIClient()), \
         mock.patch('mcp_server.server.Database', return_value=MockDatabase()), \
         mock.patch('mcp_server.server.ChatAnalyzer', return_value=MockChatAnalyzer()), \
         mock.patch('mcp_server.server.CurriculumGenerator', return_value=MockCurriculumGenerator()), \
         mock.patch('mcp_server.server.RecommendationUpdater', return_value=MockRecommendationUpdater()):
        
        server = AILearningServer()
        yield server

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
    class RequestParams:
        name = "analyze_chat"
        arguments = {
            "messages": [
                {"role": "user", "content": "Pythonを学びたいです"}
            ]
        }
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    response = await mock_server.call_tool(request)
    
    assert isinstance(response, dict)
    assert "profile" in response
    assert "skill_level" in response["profile"]

@pytest.mark.asyncio
async def test_call_tool_generate_curriculum(mock_server):
    """カリキュラム生成ツールのテスト"""
    # リクエストのモック
    class RequestParams:
        name = "generate_curriculum"
        arguments = {
            "profile": {
                "goals": ["Pythonプログラミングの習得"],
                "skill_level": "初級",
                "available_time": "週10時間",
                "learning_style": "実践的"
            }
        }
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    response = await mock_server.call_tool(request)
    
    assert isinstance(response, dict)
    assert "curriculum" in response
    assert "modules" in response["curriculum"]

@pytest.mark.asyncio
async def test_call_tool_update_recommendations(mock_server):
    """レコメンデーション更新ツールのテスト"""
    # リクエストのモック
    class RequestParams:
        name = "update_recommendations"
        arguments = {
            "progress": {
                "user_id": "test-user",
                "module_id": "test-module",
                "status": "in_progress",
                "completion_percentage": 50
            }
        }
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    response = await mock_server.call_tool(request)
    
    assert isinstance(response, dict)
    assert "recommendations" in response
    assert "learning_path" in response["recommendations"]

@pytest.mark.asyncio
async def test_call_tool_invalid(mock_server):
    """無効なツール呼び出しのテスト"""
    # リクエストのモック
    class RequestParams:
        name = "invalid_tool"
        arguments = {}
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    with pytest.raises(Exception) as exc_info:
        await mock_server.call_tool(request)
    
    assert "Unknown tool" in str(exc_info.value)

@pytest.mark.asyncio
async def test_list_resource_templates(mock_server):
    """リソーステンプレート一覧のテスト"""
    # リクエストのモック
    request = MagicMock()
    
    response = await mock_server.list_resource_templates(request)
    
    assert isinstance(response, dict)
    assert "resourceTemplates" in response
    assert len(response["resourceTemplates"]) == 2

@pytest.mark.asyncio
async def test_read_resource_profile(mock_server):
    """プロファイルリソース読み取りのテスト"""
    # リクエストのモック
    class RequestParams:
        uri = "learning://profiles/test-user-id"
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    response = await mock_server.read_resource(request)
    
    assert isinstance(response, dict)
    assert "contents" in response
    assert len(response["contents"]) == 1
    assert "text" in response["contents"][0]
    assert "test-user-id" in response["contents"][0]["text"]

@pytest.mark.asyncio
async def test_read_resource_curriculum(mock_server):
    """カリキュラムリソース読み取りのテスト"""
    # リクエストのモック
    class RequestParams:
        uri = "learning://curriculum/test-user-id"
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    response = await mock_server.read_resource(request)
    
    assert isinstance(response, dict)
    assert "contents" in response
    assert len(response["contents"]) == 1
    assert "text" in response["contents"][0]
    assert "Python基礎" in response["contents"][0]["text"]

@pytest.mark.asyncio
async def test_read_resource_invalid_uri(mock_server):
    """無効なURIでのリソース読み取りテスト"""
    # リクエストのモック
    class RequestParams:
        uri = "invalid://uri"
    
    class Request:
        params = RequestParams()
    
    request = Request()
    
    with pytest.raises(Exception) as exc_info:
        await mock_server.read_resource(request)
    
    assert "Invalid resource URI" in str(exc_info.value)