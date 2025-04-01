from typing import List, Dict, Any
import openai
from openai import AsyncOpenAI

class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def chat_completion(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        model: str = "gpt-4o-mini"
    ) -> Dict[str, Any]:
        """OpenAI ChatCompletion APIを使用してチャット応答を生成"""
        try:
            formatted_messages = [
                {"role": "system", "content": system_prompt}
            ]
            formatted_messages.extend(messages)
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "content": response.choices[0].message.content,
                "role": response.choices[0].message.role,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            raise OpenAIError(f"OpenAI API error: {str(e)}")
            
    async def analyze_chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """チャット履歴を分析して学習プロファイルを生成"""
        system_prompt = """
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
        
        response = await self.chat_completion(system_prompt, messages)
        return response
        
    async def generate_curriculum(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """学習プロファイルに基づいてカリキュラムを生成"""
        system_prompt = f"""
        以下の学習プロファイルに基づいて、
        最適な学習カリキュラムを生成してください：

        プロファイル情報：
        - 目標: {profile['goals']}
        - スキルレベル: {profile['skill_level']}
        - 利用可能時間: {profile['available_time']}
        - 学習スタイル: {profile['learning_style']}

        以下の形式でカリキュラムを生成してください：
        {{
            "modules": [
                {{
                    "title": "モジュール名",
                    "description": "説明",
                    "duration": "所要時間",
                    "difficulty": "難易度",
                    "resources": [
                        {{
                            "type": "ビデオ/記事",
                            "title": "リソース名",
                            "url": "URL"
                        }}
                    ],
                    "recommended_order": 1
                }}
            ],
            "recommendations": {{
                "learning_path": "学習パス説明",
                "time_allocation": "時間配分指針",
                "focus_areas": ["重点分野1", "重点分野2"]
            }}
        }}
        """
        
        response = await self.chat_completion(
            system_prompt,
            [{"role": "user", "content": "カリキュラムを生成してください"}]
        )
        return response
        
    async def update_recommendations(
        self,
        progress: Dict[str, Any],
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """学習進捗に基づいてレコメンデーションを更新"""
        system_prompt = f"""
        以下の情報に基づいて、学習レコメンデーションを更新してください：

        学習プロファイル：
        - 目標: {profile['goals']}
        - スキルレベル: {profile['skill_level']}
        - 利用可能時間: {profile['available_time']}
        - 学習スタイル: {profile['learning_style']}

        進捗状況：
        - 完了したモジュール: {progress['completed_modules']}
        - 評価結果: {progress['assessment_results']}

        以下の形式でレコメンデーションを生成してください：
        {{
            "next_modules": ["次に学ぶべきモジュール1", "モジュール2"],
            "focus_areas": ["重点的に学ぶべき分野1", "分野2"],
            "adjusted_difficulty": "調整後の難易度レベル"
        }}
        """
        
        response = await self.chat_completion(
            system_prompt,
            [{"role": "user", "content": "レコメンデーションを更新してください"}]
        )
        return response


class OpenAIError(Exception):
    """OpenAI API関連のエラー"""
    pass
