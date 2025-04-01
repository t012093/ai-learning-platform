# テストパッケージの初期化
import os
import sys
from pathlib import Path

# プロジェクトルートをPYTHONPATHに追加
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# テスト環境変数の設定
os.environ.setdefault('ENVIRONMENT', 'test')
os.environ.setdefault('DEBUG_MODE', 'true')
os.environ.setdefault('TEST_MODE', 'true')

# テストデータベースの設定
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

# OpenAI APIのモック設定
if not os.getenv('MOCK_OPENAI_RESPONSES'):
    os.environ['MOCK_OPENAI_RESPONSES'] = 'true'

# ロギングの設定
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
