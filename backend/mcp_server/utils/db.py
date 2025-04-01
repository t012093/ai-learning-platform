from typing import Dict, List, Optional
from datetime import datetime
import json
import uuid

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncEngine

Base = declarative_base()

class LearningProfile(Base):
    __tablename__ = 'learning_profiles'
    
    id = Column(String, primary_key=True)
    goals = Column(Text, nullable=False)  # JSON配列として格納
    skill_level = Column(String, nullable=False)
    available_time = Column(String, nullable=False)
    learning_style = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Curriculum(Base):
    __tablename__ = 'curricula'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('learning_profiles.id'), nullable=False)
    modules = Column(Text, nullable=False)  # JSON配列として格納
    recommendations = Column(Text, nullable=False)  # JSONオブジェクトとして格納
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Module(Base):
    __tablename__ = 'modules'
    
    id = Column(String, primary_key=True)
    curriculum_id = Column(String, ForeignKey('curricula.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    duration = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    recommended_order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Resource(Base):
    __tablename__ = 'resources'
    
    id = Column(String, primary_key=True)
    module_id = Column(String, ForeignKey('modules.id'), nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LearningProgress(Base):
    __tablename__ = 'learning_progress'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('learning_profiles.id'), nullable=False)
    module_id = Column(String, ForeignKey('modules.id'), nullable=False)
    status = Column(String, nullable=False)
    completion_percentage = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Assessment(Base):
    __tablename__ = 'assessments'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('learning_profiles.id'), nullable=False)
    module_id = Column(String, ForeignKey('modules.id'), nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(Text)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())

class Database:
    def __init__(self, session=None):
        if session:
            # セッションが直接渡された場合（テスト時など）
            self.async_session = lambda: session
        else:
            # URL から新しいエンジンとセッションを作成
            self.engine: AsyncEngine = create_async_engine(
                "sqlite+aiosqlite:///./learning.db",
                echo=True  # SQLログを出力
            )
            self.async_session = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        
    async def init(self):
        """データベースの初期化とテーブル作成"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def create_profile(self, profile_data: Dict) -> LearningProfile:
        """学習プロファイルの作成"""
        async with self.async_session() as session:
            profile = LearningProfile(
                id=str(uuid.uuid4()),
                goals=json.dumps(profile_data["goals"]),
                skill_level=profile_data["skill_level"],
                available_time=profile_data["available_time"],
                learning_style=profile_data["learning_style"]
            )
            session.add(profile)
            await session.commit()
            return profile
            
    async def get_profile(self, user_id: str) -> Optional[Dict]:
        """学習プロファイルの取得"""
        async with self.async_session() as session:
            result = await session.get(LearningProfile, user_id)
            if result is None:
                return None
            return {
                "id": result.id,
                "goals": json.loads(result.goals),
                "skill_level": result.skill_level,
                "available_time": result.available_time,
                "learning_style": result.learning_style,
                "created_at": result.created_at.isoformat(),
                "updated_at": result.updated_at.isoformat() if result.updated_at else None
            }
            
    async def create_curriculum(self, curriculum_data: Dict) -> Curriculum:
        """カリキュラムの作成"""
        async with self.async_session() as session:
            curriculum = Curriculum(
                id=str(uuid.uuid4()),
                user_id=curriculum_data["user_id"],
                modules=json.dumps(curriculum_data["modules"]),
                recommendations=json.dumps(curriculum_data["recommendations"])
            )
            session.add(curriculum)
            await session.commit()
            return curriculum
            
    async def get_curriculum(self, user_id: str) -> Optional[Dict]:
        """カリキュラムの取得"""
        async with self.async_session() as session:
            result = await session.get(Curriculum, user_id)
            if result is None:
                return None
            return {
                "id": result.id,
                "user_id": result.user_id,
                "modules": json.loads(result.modules),
                "recommendations": json.loads(result.recommendations),
                "created_at": result.created_at.isoformat(),
                "updated_at": result.updated_at.isoformat() if result.updated_at else None
            }
            
    async def create_module(self, module_data: Dict) -> Module:
        """モジュールの作成"""
        async with self.async_session() as session:
            module = Module(
                id=str(uuid.uuid4()),
                curriculum_id=module_data["curriculum_id"],
                title=module_data["title"],
                description=module_data["description"],
                duration=module_data["duration"],
                difficulty=module_data["difficulty"],
                recommended_order=module_data["recommended_order"]
            )
            session.add(module)
            await session.commit()
            return module
            
    async def create_learning_progress(self, progress_data: Dict) -> LearningProgress:
        """学習進捗の記録"""
        async with self.async_session() as session:
            progress = LearningProgress(
                id=str(uuid.uuid4()),
                user_id=progress_data["user_id"],
                module_id=progress_data["module_id"],
                status=progress_data["status"],
                completion_percentage=progress_data.get("completion_percentage", 0)
            )
            session.add(progress)
            await session.commit()
            return progress
            
    async def update_learning_progress(
        self,
        progress_id: str,
        update_data: Dict
    ) -> Optional[LearningProgress]:
        """学習進捗の更新"""
        async with self.async_session() as session:
            progress = await session.get(LearningProgress, progress_id)
            if progress is None:
                return None
                
            for key, value in update_data.items():
                setattr(progress, key, value)
                
            await session.commit()
            return progress
            
    async def create_assessment(self, assessment_data: Dict) -> Assessment:
        """評価結果の記録"""
        async with self.async_session() as session:
            assessment = Assessment(
                id=str(uuid.uuid4()),
                user_id=assessment_data["user_id"],
                module_id=assessment_data["module_id"],
                score=assessment_data["score"],
                feedback=assessment_data.get("feedback")
            )
            session.add(assessment)
            await session.commit()
            return assessment

class DatabaseError(Exception):
    """データベース操作に関するエラー"""
    pass
