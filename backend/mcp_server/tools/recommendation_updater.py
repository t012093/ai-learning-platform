from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timedelta

from ..utils.openai_client import OpenAIClient
from ..utils.db import Database

class RecommendationUpdater:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def update(
        self,
        progress: Dict[str, Any],
        profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        学習進捗に基づいてレコメンデーションを更新する

        Args:
            progress: 学習進捗データ
                {
                    "completed_modules": List[str],
                    "assessment_results": Dict[str, Any],
                    "user_id": str
                }
            profile: 学習プロファイル（オプション）

        Returns:
            Dict[str, Any]: 更新されたレコメンデーション
                {
                    "next_modules": List[str],
                    "focus_areas": List[str],
                    "adjusted_difficulty": str
                }
        """
        try:
            # 学習パターンと進捗を分析
            learning_patterns = self._analyze_learning_patterns(progress)
            
            # OpenAI APIを使用してレコメンデーションを生成
            response = await self.openai_client.update_recommendations(
                progress,
                profile or {}
            )
            
            # レスポンスからJSONデータを抽出
            try:
                result = json.loads(response["content"])
            except json.JSONDecodeError:
                # JSON形式でない場合は、構造化データに変換を試みる
                result = self._extract_recommendations_from_text(response["content"])
            
            # レコメンデーションの最適化
            result = self._optimize_recommendations(result, learning_patterns)
            
            # 結果の検証
            self._validate_recommendations(result)
            
            return result
            
        except Exception as e:
            raise RecommendationUpdateError(f"レコメンデーション更新中にエラーが発生しました: {str(e)}")

    def _analyze_learning_patterns(self, progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        学習パターンを分析する

        Args:
            progress: 学習進捗データ

        Returns:
            Dict[str, Any]: 分析結果
        """
        patterns = {
            "completion_rate": 0.0,
            "average_score": 0.0,
            "learning_speed": "normal",
            "weak_areas": [],
            "strong_areas": []
        }
        
        # 完了率の計算
        if progress.get("completed_modules"):
            total_modules = len(progress["completed_modules"]) + len(
                progress.get("remaining_modules", [])
            )
            patterns["completion_rate"] = len(
                progress["completed_modules"]
            ) / total_modules if total_modules > 0 else 0
            
        # 評価スコアの分析
        assessment_results = progress.get("assessment_results", {})
        if assessment_results:
            scores = [result["score"] for result in assessment_results.values()]
            patterns["average_score"] = sum(scores) / len(scores) if scores else 0
            
            # 強みと弱みの分野を特定
            for module_id, result in assessment_results.items():
                if result["score"] >= 80:
                    patterns["strong_areas"].append(module_id)
                elif result["score"] <= 60:
                    patterns["weak_areas"].append(module_id)
                    
        # 学習速度の分析
        if progress.get("module_completion_times"):
            completion_times = progress["module_completion_times"]
            avg_time = sum(
                (datetime.fromisoformat(time["end"]) - datetime.fromisoformat(time["start"])).days
                for time in completion_times
            ) / len(completion_times)
            
            if avg_time < 7:  # 1週間未満
                patterns["learning_speed"] = "fast"
            elif avg_time > 14:  # 2週間以上
                patterns["learning_speed"] = "slow"
                
        return patterns

    def _optimize_recommendations(
        self,
        recommendations: Dict[str, Any],
        learning_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        学習パターンに基づいてレコメンデーションを最適化する

        Args:
            recommendations: 生成されたレコメンデーション
            learning_patterns: 学習パターン分析結果

        Returns:
            Dict[str, Any]: 最適化されたレコメンデーション
        """
        # 完了率に基づく調整
        if learning_patterns["completion_rate"] < 0.3:
            # 進捗が遅い場合、より基礎的なモジュールを推奨
            recommendations["adjusted_difficulty"] = "基礎"
            recommendations["focus_areas"].insert(0, "基礎の復習")
            
        # 評価スコアに基づく調整
        if learning_patterns["average_score"] < 70:
            # スコアが低い場合、復習を推奨
            recommendations["focus_areas"].extend(learning_patterns["weak_areas"])
            
        # 学習速度に基づく調整
        if learning_patterns["learning_speed"] == "fast":
            # 学習が速い場合、より高度な内容を追加
            recommendations["next_modules"].extend(
                self._get_advanced_modules(recommendations["next_modules"])
            )
        elif learning_patterns["learning_speed"] == "slow":
            # 学習が遅い場合、補足的な内容を追加
            recommendations["next_modules"] = self._get_simplified_modules(
                recommendations["next_modules"]
            )
            
        return recommendations

    def _validate_recommendations(self, recommendations: Dict[str, Any]) -> None:
        """
        レコメンデーションデータのバリデーション

        Args:
            recommendations: レコメンデーションデータ

        Raises:
            RecommendationUpdateError: バリデーションエラー時
        """
        required_fields = ["next_modules", "focus_areas", "adjusted_difficulty"]
        
        for field in required_fields:
            if field not in recommendations:
                raise RecommendationUpdateError(f"必須フィールド '{field}' が欠落しています")
                
        if not isinstance(recommendations["next_modules"], list):
            raise RecommendationUpdateError("next_modulesはリスト形式である必要があります")
            
        if not isinstance(recommendations["focus_areas"], list):
            raise RecommendationUpdateError("focus_areasはリスト形式である必要があります")

    def _get_advanced_modules(self, current_modules: List[str]) -> List[str]:
        """より高度なモジュールを提案"""
        # ここに実際のロジックを実装
        return ["発展学習モジュール1", "応用演習モジュール2"]

    def _get_simplified_modules(self, current_modules: List[str]) -> List[str]:
        """より基礎的なモジュールを提案"""
        # ここに実際のロジックを実装
        return ["基礎復習モジュール1", "演習補足モジュール2"]

    def _extract_recommendations_from_text(self, text: str) -> Dict[str, Any]:
        """
        テキストからレコメンデーション情報を抽出する

        Args:
            text: OpenAI APIからの応答テキスト

        Returns:
            Dict[str, Any]: 構造化されたレコメンデーションデータ
        """
        recommendations = {
            "next_modules": [],
            "focus_areas": [],
            "adjusted_difficulty": "基礎"
        }
        
        current_section = None
        
        # テキストを行ごとに分析
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # セクションの特定
            if "次のモジュール" in line or "Next Modules" in line:
                current_section = "next_modules"
            elif "重点分野" in line or "Focus Areas" in line:
                current_section = "focus_areas"
            elif "難易度" in line or "Difficulty" in line:
                current_section = "difficulty"
            elif current_section and "-" in line:
                value = line.split("-", 1)[1].strip()
                
                if current_section == "next_modules":
                    recommendations["next_modules"].append(value)
                elif current_section == "focus_areas":
                    recommendations["focus_areas"].append(value)
                elif current_section == "difficulty":
                    recommendations["adjusted_difficulty"] = value
                    
        return recommendations

class RecommendationUpdateError(Exception):
    """レコメンデーション更新に関するエラー"""
    pass
