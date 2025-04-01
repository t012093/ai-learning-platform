#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPYTHONPATHに追加
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from mcp_server.utils.db import Base, Database
from mcp_server.config import settings

async def init_database():
    """データベースの初期化とテーブルの作成"""
    print("データベースを初期化しています...")
    
    try:
        # データベースの接続とテーブルの作成
        db = Database(settings.DATABASE_URL)
        await db.init()
        
        print("データベースの初期化が完了しました")
        
        # テストデータの挿入（開発環境のみ）
        if settings.DEBUG_MODE:
            await create_test_data(db)
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

async def create_test_data(db: Database):
    """テストデータの作成"""
    print("テストデータを作成しています...")
    
    try:
        # テスト用学習プロファイル
        test_profile = {
            "goals": ["Pythonプログラミングの習得", "ウェブアプリケーション開発"],
            "skill_level": "初級",
            "available_time": "週10時間",
            "learning_style": "実践的な演習重視"
        }
        profile = await db.create_profile(test_profile)
        
        # テスト用カリキュラム
        test_curriculum = {
            "user_id": profile.id,
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
        curriculum = await db.create_curriculum(test_curriculum)
        
        # テスト用モジュール
        test_module = {
            "curriculum_id": curriculum.id,
            "title": "Python基礎",
            "description": "Python言語の基本構文と概念を学びます",
            "duration": "2週間",
            "difficulty": "初級",
            "recommended_order": 1
        }
        module = await db.create_module(test_module)
        
        # テスト用学習進捗
        test_progress = {
            "user_id": profile.id,
            "module_id": module.id,
            "status": "in_progress",
            "completion_percentage": 30
        }
        await db.create_learning_progress(test_progress)
        
        print("テストデータの作成が完了しました")
        
    except Exception as e:
        print(f"テストデータの作成中にエラーが発生しました: {e}")
        raise

def validate_environment():
    """環境変数とデータベース設定の検証"""
    required_vars = [
        "DATABASE_URL",
        "OPENAI_API_KEY",
        "SECRET_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"必要な環境変数が設定されていません: {', '.join(missing_vars)}")
        print("'.env'ファイルを確認してください")
        sys.exit(1)
        
    if not settings.DATABASE_URL.startswith(("sqlite:///", "postgresql://")):
        print("サポートされていないデータベースURLの形式です")
        sys.exit(1)

if __name__ == "__main__":
    print("データベース初期化スクリプトを実行します")
    
    # 環境変数の検証
    validate_environment()
    
    # データベースの初期化
    asyncio.run(init_database())
    
    print("スクリプトの実行が完了しました")
