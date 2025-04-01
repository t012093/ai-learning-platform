import pytest
from unittest.mock import patch, AsyncMock
import json

from mcp_server.utils.openai_client import OpenAIClient, OpenAIError

@pytest.fixture
def openai_client():
    """OpenAIClientのフィクスチャー"""
    return OpenAIClient(api_key="test-api-key")

@pytest.mark.asyncio
async def test_chat_completion(openai_client, mock_openai_response):
    """チャット補完機能のテスト"""
    with patch.object(openai_client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_obj = type('obj', (object,), {
            'choices': [
                type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': mock_openai_response["content"],
                        'role': mock_openai_response["role"]
                    }),
                    'finish_reason': mock_openai_response["finish_reason"]
                })
            ]
        })
        mock_create.return_value = mock_obj
        
        response = await openai_client.chat_completion(
            "テストプロンプト",
            [{"role": "user", "content": "テストメッセージ"}]
        )
        
        assert isinstance(response, dict)
        assert "content" in response
        assert "role" in response
        assert "finish_reason" in response

@pytest.mark.asyncio
async def test_chat_completion_error(openai_client):
    """チャット補完のエラーハンドリングテスト"""
    with patch.object(openai_client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = Exception("API Error")
        
        with pytest.raises(OpenAIError):
            await openai_client.chat_completion(
                "テストプロンプト",
                [{"role": "user", "content": "テストメッセージ"}]
            )

@pytest.mark.asyncio
async def test_analyze_chat(openai_client, mock_openai_response):
    """チャット分析機能のテスト"""
    with patch.object(openai_client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_obj = type('obj', (object,), {
            'choices': [
                type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': json.dumps({
                            "goals": ["Python学習"],
                            "skill_level": "初級",
                            "available_time": "週10時間",
                            "learning_style": "実践的"
                        }),
                        'role': "assistant"
                    }),
                    'finish_reason': "stop"
                })
            ]
        })
        mock_create.return_value = mock_obj
        
        messages = [{"role": "user", "content": "Pythonを学びたいです"}]
        response = await openai_client.analyze_chat(messages)
        
        assert isinstance(response, dict)
        assert "content" in response
        content_dict = json.loads(response["content"])
        assert "goals" in content_dict
        assert "skill_level" in content_dict

@pytest.mark.asyncio
async def test_generate_curriculum(openai_client, test_profile_data):
    """カリキュラム生成機能のテスト"""
    with patch.object(openai_client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_obj = type('obj', (object,), {
            'choices': [
                type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': json.dumps({
                            "modules": [
                                {
                                    "title": "Python基礎",
                                    "description": "基本を学ぶ",
                                    "duration": "2週間",
                                    "difficulty": "初級",
                                    "resources": [],
                                    "recommended_order": 1
                                }
                            ],
                            "recommendations": {
                                "learning_path": "基礎から",
                                "time_allocation": "毎日2時間",
                                "focus_areas": ["基本構文"]
                            }
                        }),
                        'role': "assistant"
                    }),
                    'finish_reason': "stop"
                })
            ]
        })
        mock_create.return_value = mock_obj
        
        response = await openai_client.generate_curriculum(test_profile_data)
        
        assert isinstance(response, dict)
        assert "content" in response
        content_dict = json.loads(response["content"])
        assert "modules" in content_dict
        assert "recommendations" in content_dict

@pytest.mark.asyncio
async def test_update_recommendations(openai_client, test_profile_data):
    """レコメンデーション更新機能のテスト"""
    progress_data = {
        "completed_modules": ["module1"],
        "assessment_results": {"module1": {"score": 85}}
    }
    
    with patch.object(openai_client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_obj = type('obj', (object,), {
            'choices': [
                type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': json.dumps({
                            "next_modules": ["module2"],
                            "focus_areas": ["データ構造"],
                            "adjusted_difficulty": "中級"
                        }),
                        'role': "assistant"
                    }),
                    'finish_reason': "stop"
                })
            ]
        })
        mock_create.return_value = mock_obj
        
        response = await openai_client.update_recommendations(
            progress_data,
            test_profile_data
        )
        
        assert isinstance(response, dict)
        assert "content" in response
        content_dict = json.loads(response["content"])
        assert "next_modules" in content_dict
        assert "focus_areas" in content_dict

@pytest.mark.asyncio
async def test_temperature_setting(openai_client):
    """温度パラメータの設定テスト"""
    with patch.object(openai_client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_obj = type('obj', (object,), {
            'choices': [
                type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': "テスト応答",
                        'role': "assistant"
                    }),
                    'finish_reason': "stop"
                })
            ]
        })
        mock_create.return_value = mock_obj
        
        # 異なる温度設定でのテスト
        await openai_client.chat_completion(
            "テストプロンプト",
            [{"role": "user", "content": "テスト"}],
            temperature=0.5
        )
        
        # temperatureパラメータが正しく設定されているか確認
        assert mock_create.called
        call_args = mock_create.call_args[1]
        assert call_args.get('temperature') == 0.5
        assert 'model' in call_args
        assert len(call_args.get('messages')) == 2