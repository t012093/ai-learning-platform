from typing import List, Dict, Any
import json
from datetime import datetime
import uuid

from ..utils.openai_client import OpenAIClient
from ..utils.db import Database

class CurriculumGenerator:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def generate(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        学習プロファイルに基づいてカリキュラムを生成する

        Args:
            profile: 学習プロファイル
                {
                    "goals": List[str],
                    "skill_level": str,
                    "available_time": str,
                    "learning_style": str
                }

        Returns:
            Dict[str, Any]: 生成されたカリキュラム
                {
                    "modules": List[Dict],
                    "recommendations": Dict
                }
        """
        try:
            # OpenAI APIを使用してカリキュラムを生成
            response = await self.openai_client.generate_curriculum(profile)
            
            # レスポンスからJSONデータを抽出
            try:
                result = json.loads(response["content"])
            except json.JSONDecodeError:
                # JSON形式でない場合は、構造化データに変換を試みる
                result = self._extract_curriculum_from_text(response["content"])
            
            # カリキュラムの検証と最適化
            result = self._optimize_curriculum(result, profile)
            
            # 結果の検証
            self._validate_curriculum(result)
            
            return result
            
        except Exception as e:
            raise CurriculumGenerationError(f"カリキュラム生成中にエラーが発生しました: {str(e)}")

    def _validate_curriculum(self, curriculum: Dict[str, Any]) -> None:
        """
        生成されたカリキュラムデータのバリデーション

        Args:
            curriculum: カリキュラムデータ

        Raises:
            CurriculumGenerationError: バリデーションエラー時
        """
        if "modules" not in curriculum:
            raise CurriculumGenerationError("モジュール情報が欠落しています")
            
        if not isinstance(curriculum["modules"], list):
            raise CurriculumGenerationError("モジュールはリスト形式である必要があります")
            
        if "recommendations" not in curriculum:
            raise CurriculumGenerationError("レコメンデーション情報が欠落しています")
            
        # 各モジュールの必須フィールドを確認
        required_module_fields = [
            "title", "description", "duration",
            "difficulty", "resources", "recommended_order"
        ]
        
        for module in curriculum["modules"]:
            for field in required_module_fields:
                if field not in module:
                    raise CurriculumGenerationError(f"モジュールの必須フィールド '{field}' が欠落しています")
                    
            # リソースのバリデーション
            if not isinstance(module["resources"], list):
                raise CurriculumGenerationError("リソースはリスト形式である必要があります")
                
            for resource in module["resources"]:
                if "type" not in resource or "title" not in resource or "url" not in resource:
                    raise CurriculumGenerationError("リソースの必須フィールドが欠落しています")

    def _optimize_curriculum(
        self,
        curriculum: Dict[str, Any],
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        カリキュラムを学習者のプロファイルに基づいて最適化

        Args:
            curriculum: 生成されたカリキュラム
            profile: 学習プロファイル

        Returns:
            Dict[str, Any]: 最適化されたカリキュラム
        """
        # 利用可能時間に基づいてモジュールの期間を調整
        available_time = self._parse_available_time(profile["available_time"])
        modules = curriculum["modules"]
        
        # モジュールの合計時間を計算
        total_duration = sum(
            self._parse_duration(module["duration"])
            for module in modules
        )
        
        # 時間調整が必要な場合
        if total_duration > available_time:
            # モジュールの期間を比例配分で調整
            ratio = available_time / total_duration
            for module in modules:
                duration_hours = self._parse_duration(module["duration"])
                adjusted_hours = duration_hours * ratio
                module["duration"] = f"{adjusted_hours:.1f}時間"
                
        # 学習スタイルに基づいてリソースを最適化
        learning_style = profile["learning_style"]
        for module in modules:
            module["resources"] = self._optimize_resources(
                module["resources"],
                learning_style
            )
            
        # スキルレベルに基づいて難易度を調整
        skill_level = profile["skill_level"]
        modules = self._adjust_difficulty(modules, skill_level)
        
        curriculum["modules"] = modules
        return curriculum

    def _parse_available_time(self, time_str: str) -> float:
        """
        利用可能時間の文字列を時間数に変換

        Args:
            time_str: 時間を表す文字列（例: "週10時間"）

        Returns:
            float: 週あたりの時間数
        """
        try:
            # 数値を抽出
            num = float(''.join(filter(str.isdigit, time_str)))
            
            # 単位に基づいて調整
            if "日" in time_str:
                return num * 7  # 週あたりに換算
            elif "月" in time_str:
                return num / 4  # 週あたりに換算
            else:
                return num  # すでに週単位と仮定
                
        except ValueError:
            return 10.0  # デフォルト値

    def _parse_duration(self, duration_str: str) -> float:
        """
        期間の文字列を時間数に変換

        Args:
            duration_str: 期間を表す文字列（例: "2時間"）

        Returns:
            float: 時間数
        """
        try:
            return float(''.join(filter(str.isdigit, duration_str)))
        except ValueError:
            return 1.0  # デフォルト値

    def _optimize_resources(
        self,
        resources: List[Dict[str, str]],
        learning_style: str
    ) -> List[Dict[str, str]]:
        """
        学習スタイルに基づいてリソースを最適化

        Args:
            resources: リソースのリスト
            learning_style: 学習スタイル

        Returns:
            List[Dict[str, str]]: 最適化されたリソースのリスト
        """
        # 学習スタイルに基づいてリソースを並び替え
        if "視覚的" in learning_style or "ビジュアル" in learning_style:
            # 動画リソースを優先
            return sorted(
                resources,
                key=lambda x: 0 if x["type"] == "video" else 1
            )
        elif "読書" in learning_style or "テキスト" in learning_style:
            # 記事リソースを優先
            return sorted(
                resources,
                key=lambda x: 0 if x["type"] == "article" else 1
            )
            
        return resources

    def _adjust_difficulty(
        self,
        modules: List[Dict[str, Any]],
        skill_level: str
    ) -> List[Dict[str, Any]]:
        """
        スキルレベルに基づいてモジュールの難易度を調整

        Args:
            modules: モジュールのリスト
            skill_level: スキルレベル

        Returns:
            List[Dict[str, Any]]: 調整されたモジュールのリスト
        """
        difficulty_map = {
            "初級": ["入門", "基礎", "初級"],
            "中級": ["基礎", "初級", "中級"],
            "上級": ["中級", "上級", "発展"]
        }
        
        target_difficulties = difficulty_map.get(skill_level, ["初級"])
        
        # 各モジュールの難易度を適切なレベルに調整
        adjusted_modules = modules.copy()
        for i, module in enumerate(adjusted_modules):
            # モジュールの順序に基づいて難易度を段階的に上げる
            difficulty_index = min(i // 2, len(target_difficulties) - 1)
            module["difficulty"] = target_difficulties[difficulty_index]
            
        return adjusted_modules

    def _extract_curriculum_from_text(self, text: str) -> Dict[str, Any]:
        """
        テキストからカリキュラム情報を抽出する

        Args:
            text: OpenAI APIからの応答テキスト

        Returns:
            Dict[str, Any]: 構造化されたカリキュラムデータ
        """
        curriculum = {
            "modules": [],
            "recommendations": {
                "learning_path": "",
                "time_allocation": "",
                "focus_areas": []
            }
        }
        
        current_module = None
        current_section = None
        
        # テキストを行ごとに分析
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # モジュールの開始を検出
            if "モジュール" in line or "Module" in line:
                if current_module:
                    curriculum["modules"].append(current_module)
                current_module = {
                    "title": line.split(":", 1)[1].strip() if ":" in line else line,
                    "description": "",
                    "duration": "1時間",
                    "difficulty": "初級",
                    "resources": [],
                    "recommended_order": len(curriculum["modules"]) + 1
                }
                current_section = "description"
                
            # セクションの特定
            elif current_module:
                if "説明" in line or "Description" in line:
                    current_section = "description"
                elif "所要時間" in line or "Duration" in line:
                    current_section = "duration"
                elif "難易度" in line or "Difficulty" in line:
                    current_section = "difficulty"
                elif "リソース" in line or "Resources" in line:
                    current_section = "resources"
                elif current_section and ":" in line:
                    key, value = line.split(":", 1)
                    value = value.strip()
                    
                    if current_section == "description":
                        current_module["description"] = value
                    elif current_section == "duration":
                        current_module["duration"] = value
                    elif current_section == "difficulty":
                        current_module["difficulty"] = value
                    elif current_section == "resources" and "-" in line:
                        resource_type = "video" if "動画" in line.lower() else "article"
                        current_module["resources"].append({
                            "type": resource_type,
                            "title": key.strip(),
                            "url": value
                        })
                        
        # 最後のモジュールを追加
        if current_module:
            curriculum["modules"].append(current_module)
            
        return curriculum

class CurriculumGenerationError(Exception):
    """カリキュラム生成に関するエラー"""
    pass
