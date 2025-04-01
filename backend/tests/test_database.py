import pytest
import json
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from mcp_server.utils.db import Base, LearningProfile, Curriculum, Module, LearningProgress


async def test_create_profile(db_session: AsyncSession, test_profile_data: dict):
    """学習プロファイルの作成テスト"""
    # プロファイルの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),  # JSONに変換
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    
    db_session.add(profile)
    await db_session.commit()
    await db_session.refresh(profile)

    assert isinstance(profile, LearningProfile)
    assert profile.id is not None
    assert json.loads(profile.goals) == test_profile_data["goals"]  # JSON文字列を読み込み
    assert profile.skill_level == test_profile_data["skill_level"]
    assert isinstance(profile.created_at, datetime)


async def test_get_profile(db_session: AsyncSession, test_profile_data: dict):
    """学習プロファイルの取得テスト"""
    # プロファイルの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),  # JSONに変換
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    
    db_session.add(profile)
    await db_session.commit()
    await db_session.refresh(profile)

    # プロファイルの取得（非同期メソッドを await で呼び出し）
    result = await db_session.get(LearningProfile, profile.id)
    
    assert result is not None
    assert result.id == profile.id
    assert json.loads(result.goals) == test_profile_data["goals"]


async def test_create_curriculum(db_session: AsyncSession, test_profile_data: dict, test_curriculum_data: dict):
    """カリキュラムの作成テスト"""
    # プロファイルの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    db_session.add(profile)
    await db_session.flush()

    # カリキュラムの作成
    curriculum = Curriculum(
        id=str(uuid.uuid4()),
        user_id=profile.id,
        modules=json.dumps(test_curriculum_data["modules"]),
        recommendations=json.dumps(test_curriculum_data["recommendations"])
    )

    db_session.add(curriculum)
    await db_session.commit()
    await db_session.refresh(curriculum)

    assert isinstance(curriculum, Curriculum)
    assert curriculum.id is not None
    assert curriculum.user_id == profile.id
    assert isinstance(curriculum.created_at, datetime)


async def test_create_module(db_session: AsyncSession, test_profile_data: dict, test_curriculum_data: dict):
    """モジュールの作成テスト"""
    # プロファイルとカリキュラムの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    db_session.add(profile)
    await db_session.flush()

    curriculum = Curriculum(
        id=str(uuid.uuid4()),
        user_id=profile.id,
        modules=json.dumps(test_curriculum_data["modules"]),
        recommendations=json.dumps(test_curriculum_data["recommendations"])
    )
    db_session.add(curriculum)
    await db_session.flush()

    # モジュールの作成
    module_data = test_curriculum_data["modules"][0]
    module = Module(
        id=str(uuid.uuid4()),
        curriculum_id=curriculum.id,
        title=module_data["title"],
        description=module_data["description"],
        duration=module_data["duration"],
        difficulty=module_data["difficulty"],
        recommended_order=module_data["recommended_order"]
        # resources フィールドは Module モデルには存在しない
    )

    db_session.add(module)
    await db_session.commit()
    await db_session.refresh(module)

    assert isinstance(module, Module)
    assert module.id is not None
    assert module.curriculum_id == curriculum.id
    assert module.title == module_data["title"]
    assert isinstance(module.created_at, datetime)


async def test_create_learning_progress(db_session: AsyncSession, test_profile_data: dict):
    """学習進捗の記録テスト"""
    # プロファイルの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    db_session.add(profile)
    await db_session.flush()

    # モジュールの作成（テスト用）
    module = Module(
        id=str(uuid.uuid4()),
        curriculum_id=str(uuid.uuid4()),
        title="テストモジュール",
        description="テスト用のモジュールです",
        duration="1週間",
        difficulty="初級",
        recommended_order=1
    )
    db_session.add(module)
    await db_session.flush()

    # 学習進捗の記録
    progress = LearningProgress(
        id=str(uuid.uuid4()),
        user_id=profile.id,
        module_id=module.id,
        status="in_progress",
        completion_percentage=30
    )

    db_session.add(progress)
    await db_session.commit()
    await db_session.refresh(progress)

    assert isinstance(progress, LearningProgress)
    assert progress.id is not None
    assert progress.user_id == profile.id
    assert progress.module_id == module.id
    assert progress.status == "in_progress"
    assert progress.completion_percentage == 30
    assert isinstance(progress.created_at, datetime)


async def test_update_learning_progress(db_session: AsyncSession, test_profile_data: dict):
    """学習進捗の更新テスト"""
    # プロファイルの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    db_session.add(profile)
    await db_session.flush()

    # モジュールの作成（テスト用）
    module = Module(
        id=str(uuid.uuid4()),
        curriculum_id=str(uuid.uuid4()),
        title="テストモジュール",
        description="テスト用のモジュールです",
        duration="1週間",
        difficulty="初級",
        recommended_order=1
    )
    db_session.add(module)
    await db_session.flush()

    # 初期の進捗を作成
    progress = LearningProgress(
        id=str(uuid.uuid4()),
        user_id=profile.id,
        module_id=module.id,
        status="in_progress",
        completion_percentage=30
    )
    db_session.add(progress)
    await db_session.flush()

    # 進捗を更新
    progress.status = "completed"
    progress.completion_percentage = 100
    progress.completed_at = datetime.now()
    await db_session.commit()
    await db_session.refresh(progress)

    assert progress.status == "completed"
    assert progress.completion_percentage == 100
    assert progress.completed_at is not None


async def test_get_curriculum(db_session: AsyncSession, test_profile_data: dict, test_curriculum_data: dict):
    """カリキュラムの取得テスト"""
    # プロファイルの作成
    profile = LearningProfile(
        id=str(uuid.uuid4()),
        goals=json.dumps(test_profile_data["goals"]),
        skill_level=test_profile_data["skill_level"],
        available_time=test_profile_data["available_time"],
        learning_style=test_profile_data["learning_style"]
    )
    db_session.add(profile)
    await db_session.flush()

    # カリキュラムの作成
    curriculum = Curriculum(
        id=str(uuid.uuid4()),
        user_id=profile.id,
        modules=json.dumps(test_curriculum_data["modules"]),
        recommendations=json.dumps(test_curriculum_data["recommendations"])
    )
    db_session.add(curriculum)
    await db_session.commit()
    await db_session.refresh(curriculum)

    # カリキュラムの取得（非同期メソッドを await で呼び出し）
    result = await db_session.get(Curriculum, curriculum.id)
    
    assert result is not None
    assert result.id == curriculum.id
    assert result.user_id == profile.id
