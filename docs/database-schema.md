# データベーススキーマ仕様書

## 1. 概要

システムで使用するSQLiteデータベースのスキーマ定義です。初期実装ではSQLiteを使用し、後にPostgreSQLへの移行を想定しています。

## 2. テーブル定義

### 2.1 learning_profiles
学習者のプロファイル情報を管理するテーブル

```sql
CREATE TABLE learning_profiles (
    id TEXT PRIMARY KEY,
    goals TEXT NOT NULL,  -- JSON配列として格納
    skill_level TEXT NOT NULL,  -- 'beginner', 'intermediate', 'advanced'
    available_time TEXT NOT NULL,
    learning_style TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 更新時のタイムスタンプを自動更新するトリガー
CREATE TRIGGER update_learning_profiles_timestamp 
    AFTER UPDATE ON learning_profiles
    FOR EACH ROW
BEGIN
    UPDATE learning_profiles 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = OLD.id;
END;
```

### 2.2 curricula
生成されたカリキュラム情報を管理するテーブル

```sql
CREATE TABLE curricula (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    modules TEXT NOT NULL,  -- JSON配列として格納
    recommendations TEXT NOT NULL,  -- JSONオブジェクトとして格納
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES learning_profiles(id)
);

CREATE TRIGGER update_curricula_timestamp 
    AFTER UPDATE ON curricula
    FOR EACH ROW
BEGIN
    UPDATE curricula 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = OLD.id;
END;
```

### 2.3 modules
カリキュラムのモジュール情報を管理するテーブル

```sql
CREATE TABLE modules (
    id TEXT PRIMARY KEY,
    curriculum_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    duration TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    recommended_order INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (curriculum_id) REFERENCES curricula(id)
);
```

### 2.4 resources
学習リソース情報を管理するテーブル

```sql
CREATE TABLE resources (
    id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'video', 'article', etc.
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);
```

### 2.5 learning_progress
学習の進捗状況を管理するテーブル

```sql
CREATE TABLE learning_progress (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    status TEXT NOT NULL,  -- 'not_started', 'in_progress', 'completed'
    completion_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES learning_profiles(id),
    FOREIGN KEY (module_id) REFERENCES modules(id)
);

CREATE TRIGGER update_learning_progress_timestamp 
    AFTER UPDATE ON learning_progress
    FOR EACH ROW
BEGIN
    UPDATE learning_progress 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = OLD.id;
END;
```

### 2.6 assessments
学習評価結果を管理するテーブル

```sql
CREATE TABLE assessments (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    feedback TEXT,
    taken_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES learning_profiles(id),
    FOREIGN KEY (module_id) REFERENCES modules(id)
);
```

## 3. インデックス定義

```sql
-- learning_profiles
CREATE INDEX idx_learning_profiles_updated_at ON learning_profiles(updated_at);

-- curricula
CREATE INDEX idx_curricula_user_id ON curricula(user_id);
CREATE INDEX idx_curricula_updated_at ON curricula(updated_at);

-- modules
CREATE INDEX idx_modules_curriculum_id ON modules(curriculum_id);
CREATE INDEX idx_modules_recommended_order ON modules(recommended_order);

-- resources
CREATE INDEX idx_resources_module_id ON resources(module_id);
CREATE INDEX idx_resources_type ON resources(type);

-- learning_progress
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_learning_progress_module_id ON learning_progress(module_id);
CREATE INDEX idx_learning_progress_status ON learning_progress(status);
CREATE INDEX idx_learning_progress_updated_at ON learning_progress(updated_at);

-- assessments
CREATE INDEX idx_assessments_user_id ON assessments(user_id);
CREATE INDEX idx_assessments_module_id ON assessments(module_id);
CREATE INDEX idx_assessments_taken_at ON assessments(taken_at);
```

## 4. データ型の制約

### 4.1 status型の制約
```sql
CREATE TABLE valid_status (
    status TEXT PRIMARY KEY
);

INSERT INTO valid_status (status) VALUES
    ('not_started'),
    ('in_progress'),
    ('completed');

-- learning_progressテーブルのstatusカラムに対する制約
ALTER TABLE learning_progress
ADD CONSTRAINT valid_status_check
CHECK (status IN (SELECT status FROM valid_status));
```

### 4.2 difficulty型の制約
```sql
CREATE TABLE valid_difficulty (
    difficulty TEXT PRIMARY KEY
);

INSERT INTO valid_difficulty (difficulty) VALUES
    ('beginner'),
    ('intermediate'),
    ('advanced');

-- modulesテーブルのdifficultyカラムに対する制約
ALTER TABLE modules
ADD CONSTRAINT valid_difficulty_check
CHECK (difficulty IN (SELECT difficulty FROM valid_difficulty));
```

## 5. マイグレーション管理

データベースのマイグレーションには`alembic`を使用します。

```python
# alembic/versions/xxxx_initial.py
"""初期マイグレーション

Revision ID: xxxx
Revises: 
Create Date: 2025-03-31 04:04:29.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'xxxx'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # テーブル作成
    op.create_table(
        'learning_profiles',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('goals', sa.Text(), nullable=False),
        # ... 他のカラム定義
        sa.PrimaryKeyConstraint('id')
    )
    # ... 他のテーブル作成
    
def downgrade() -> None:
    # テーブル削除（逆順）
    op.drop_table('assessments')
    op.drop_table('learning_progress')
    # ... 他のテーブル削除
