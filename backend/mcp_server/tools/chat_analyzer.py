from typing import List, Dict, Any
import json
from ..utils.openai_client import OpenAIClient

class ChatAnalyzer:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def analyze(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        チャットメッセージを分析して学習プロファイルを生成する

        Args:
            messages: チャット履歴のリスト
                [
                    {"role": "user", "content": "メッセージ内容"},
                    {"role": "assistant", "content": "応答内容"},
                    ...
                ]

        Returns:
            Dict[str, Any]: 分析結果
                {
                    "goals": List[str],
                    "skill_level": str,
                    "available_time": str,
                    "learning_style": str
                }
        """
        try:
            # OpenAI APIを使用してチャット分析
            response = await self.openai_client.analyze_chat(messages)
            
            # レスポンスからJSONデータを抽出
            try:
                result = json.loads(response["content"])
            except json.JSONDecodeError:
                # JSON形式でない場合は、構造化データに変換を試みる
                result = self._extract_profile_from_text(response["content"])
            
            # 結果の検証
            self._validate_profile(result)
            
            return result
            
        except Exception as e:
            raise ChatAnalysisError(f"チャット分析中にエラーが発生しました: {str(e)}")

    def _validate_profile(self, profile: Dict[str, Any]) -> None:
        """
        プロファイルデータのバリデーション

        Args:
            profile: 分析結果のプロファイルデータ

        Raises:
            ChatAnalysisError: バリデーションエラー時
        """
        required_fields = ["goals", "skill_level", "available_time", "learning_style"]
        
        # 必須フィールドの存在チェック
        for field in required_fields:
            if field not in profile:
                raise ChatAnalysisError(f"必須フィールド '{field}' が欠落しています")
        
        # goalsが空でないことを確認
        if not profile["goals"] or not isinstance(profile["goals"], list):
            raise ChatAnalysisError("目標が設定されていません")
        
        # skill_levelの値が有効であることを確認
        valid_skill_levels = ["初級", "中級", "上級"]
        if profile["skill_level"] not in valid_skill_levels:
            raise ChatAnalysisError(f"無効なスキルレベル: {profile['skill_level']}")

    def _extract_profile_from_text(self, text: str) -> Dict[str, Any]:
        """
        テキストから学習プロファイル情報を抽出する

        Args:
            text: OpenAI APIからの応答テキスト

        Returns:
            Dict[str, Any]: 構造化されたプロファイルデータ
        """
        # デフォルト値の設定
        profile = {
            "goals": [],
            "skill_level": "初級",
            "available_time": "未設定",
            "learning_style": "未設定"
        }
        
        # テキストを行ごとに分析
        lines = text.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # セクションの特定
            if "目標" in line or "Goals" in line:
                current_section = "goals"
            elif "スキルレベル" in line or "Skill Level" in line:
                current_section = "skill_level"
            elif "利用可能時間" in line or "Available Time" in line:
                current_section = "available_time"
            elif "学習スタイル" in line or "Learning Style" in line:
                current_section = "learning_style"
            elif current_section:
                # 現在のセクションに応じてデータを抽出
                if current_section == "goals" and "-" in line:
                    goal = line.split("-", 1)[1].strip()
                    profile["goals"].append(goal)
                elif current_section == "skill_level" and "-" in line:
                    level = line.split("-", 1)[1].strip()
                    if "初級" in level or "beginner" in level.lower():
                        profile["skill_level"] = "初級"
                    elif "中級" in level or "intermediate" in level.lower():
                        profile["skill_level"] = "中級"
                    elif "上級" in level or "advanced" in level.lower():
                        profile["skill_level"] = "上級"
                elif current_section == "available_time" and "-" in line:
                    profile["available_time"] = line.split("-", 1)[1].strip()
                elif current_section == "learning_style" and "-" in line:
                    profile["learning_style"] = line.split("-", 1)[1].strip()
                    
        return profile

class ChatAnalysisError(Exception):
    """チャット分析に関するエラー"""
    pass
