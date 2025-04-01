#!/usr/bin/env python3
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
import json

from mcp import Server, StdioServerTransport
from mcp.types import (
    ListToolsRequestSchema,
    ListResourceTemplatesRequestSchema,
    CallToolRequestSchema,
    ReadResourceRequestSchema,
    McpError,
    ErrorCode
)

import openai
from sqlalchemy.ext.asyncio import AsyncSession
from .utils.openai_client import OpenAIClient
from .utils.db import Database
from .tools.chat_analyzer import ChatAnalyzer
from .tools.curriculum_generator import CurriculumGenerator
from .tools.recommendation_updater import RecommendationUpdater
from .config import Settings

@dataclass
class LearningProfile:
    id: str
    goals: List[str]
    skill_level: str
    available_time: str
    learning_style: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Curriculum:
    id: str
    user_id: str
    modules: List[Dict]
    recommendations: Dict
    created_at: datetime
    updated_at: datetime

class AILearningServer:
    def __init__(self):
        self.settings = Settings()
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
        self.openai_client = OpenAIClient(self.settings.OPENAI_API_KEY)
        self.db = Database(self.settings.DATABASE_URL)
        self.chat_analyzer = ChatAnalyzer(self.openai_client)
        self.curriculum_generator = CurriculumGenerator(self.openai_client)
        self.recommendation_updater = RecommendationUpdater(self.openai_client)
        
        self._setup_tools()
        self._setup_resources()
        
    def _setup_tools(self):
        """ツールの設定"""
        self.server.set_request_handler(
            ListToolsRequestSchema,
            self.list_tools
        )
        self.server.set_request_handler(
            CallToolRequestSchema,
            self.call_tool
        )
        
    def _setup_resources(self):
        """リソーステンプレートの設定"""
        self.server.set_request_handler(
            ListResourceTemplatesRequestSchema,
            self.list_resource_templates
        )
        self.server.set_request_handler(
            ReadResourceRequestSchema,
            self.read_resource
        )
        
    async def list_tools(self, request):
        """利用可能なツールの一覧を返す"""
        return {
            "tools": [
                {
                    "name": "analyze_chat",
                    "description": "チャットメッセージを分析して学習プロファイルを生成",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "messages": {
                                "type": "array",
                                "items": {"type": "object"}
                            }
                        }
                    }
                },
                {
                    "name": "generate_curriculum",
                    "description": "学習プロファイルに基づいてカリキュラムを生成",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "profile": {"type": "object"}
                        }
                    }
                },
                {
                    "name": "update_recommendations",
                    "description": "学習進捗に基づいてレコメンデーションを更新",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "progress": {"type": "object"}
                        }
                    }
                }
            ]
        }
        
    async def call_tool(self, request):
        """ツールを実行"""
        tool_name = request.params.name
        arguments = request.params.arguments
        
        try:
            if tool_name == "analyze_chat":
                result = await self.chat_analyzer.analyze(arguments["messages"])
                return {"profile": result}
                
            elif tool_name == "generate_curriculum":
                result = await self.curriculum_generator.generate(arguments["profile"])
                return {"curriculum": result}
                
            elif tool_name == "update_recommendations":
                result = await self.recommendation_updater.update(arguments["progress"])
                return {"recommendations": result}
                
            else:
                raise McpError(
                    ErrorCode.MethodNotFound,
                    f"Unknown tool: {tool_name}"
                )
                
        except Exception as e:
            raise McpError(
                ErrorCode.InternalError,
                str(e)
            )
            
    async def list_resource_templates(self, request):
        """利用可能なリソーステンプレートの一覧を返す"""
        return {
            "resourceTemplates": [
                {
                    "uriTemplate": "learning://profiles/{user_id}",
                    "name": "学習プロファイル",
                    "mimeType": "application/json"
                },
                {
                    "uriTemplate": "learning://curriculum/{user_id}",
                    "name": "カリキュラム",
                    "mimeType": "application/json"
                }
            ]
        }
        
    async def read_resource(self, request):
        """リソースの読み取り"""
        uri = request.params.uri
        
        try:
            if uri.startswith("learning://profiles/"):
                user_id = uri.split("/")[-1]
                profile = await self.db.get_profile(user_id)
                return {
                    "contents": [{
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(profile, default=str)
                    }]
                }
                
            elif uri.startswith("learning://curriculum/"):
                user_id = uri.split("/")[-1]
                curriculum = await self.db.get_curriculum(user_id)
                return {
                    "contents": [{
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(curriculum, default=str)
                    }]
                }
                
            else:
                raise McpError(
                    ErrorCode.InvalidRequest,
                    f"Invalid resource URI: {uri}"
                )
                
        except Exception as e:
            raise McpError(
                ErrorCode.InternalError,
                str(e)
            )
            
    async def run(self):
        """サーバーの起動"""
        # データベースの初期化
        await self.db.init()
        
        # サーバーの起動
        transport = StdioServerTransport()
        await self.server.connect(transport)
        print("AI Learning MCP Server running on stdio", file=sys.stderr)
        
        try:
            await self.server.serve_forever()
        except KeyboardInterrupt:
            await self.server.close()
            
if __name__ == "__main__":
    import asyncio
    import sys
    
    server = AILearningServer()
    asyncio.run(server.run())
