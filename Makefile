# AI Learning Platform Makefile

.PHONY: help dev prod down clean test lint

# デフォルトのターゲット
help:
	@echo "利用可能なコマンド:"
	@echo "  make dev     - 開発環境を起動"
	@echo "  make prod    - 本番環境を起動"
	@echo "  make down    - 環境を停止"
	@echo "  make clean   - コンテナとボリュームを削除"
	@echo "  make test    - テストを実行"
	@echo "  make lint    - リンターを実行"
	@echo "  make build   - イメージをビルド"
	@echo "  make migrate - DBマイグレーションを実行"

# 開発環境
dev:
	docker-compose up -d

# 本番環境
prod:
	docker-compose -f docker-compose.prod.yml up -d

# 環境の停止
down:
	docker-compose down
	docker-compose -f docker-compose.prod.yml down

# クリーンアップ
clean:
	docker-compose down -v
	docker-compose -f docker-compose.prod.yml down -v
	rm -rf backend/__pycache__
	rm -rf frontend/.next
	rm -rf frontend/node_modules
	find . -name "*.pyc" -delete

# イメージのビルド
build:
	docker-compose build
	docker-compose -f docker-compose.prod.yml build

# テスト実行
test: test-backend test-frontend

test-backend:
	cd backend && python -m pytest

test-frontend:
	cd frontend && npm test

# リンター実行
lint: lint-backend lint-frontend

lint-backend:
	cd backend && \
	flake8 mcp_server && \
	mypy mcp_server && \
	black --check mcp_server

lint-frontend:
	cd frontend && \
	npm run lint

# DBマイグレーション
migrate:
	cd backend && python scripts/init_db.py

# 開発用の便利なコマンド
setup: setup-backend setup-frontend

setup-backend:
	cd backend && \
	python -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt

setup-frontend:
	cd frontend && npm install

# ログの表示
logs:
	docker-compose logs -f

# 本番環境のログ表示
logs-prod:
	docker-compose -f docker-compose.prod.yml logs -f

# SSL証明書の生成（開発環境用の自己署名証明書）
ssl:
	mkdir -p nginx/ssl
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout nginx/ssl/server.key \
		-out nginx/ssl/server.crt \
		-subj "/C=JP/ST=Tokyo/L=Tokyo/O=Development/CN=localhost"

# データベースのバックアップ
backup:
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	docker-compose exec db pg_dump -U postgres ai_learning > \
		"backup/ai_learning_$$timestamp.sql"

# 各種チェック
check: check-env check-docker check-deps

check-env:
	@if [ ! -f backend/.env ]; then \
		echo "Error: backend/.env file is missing"; \
		exit 1; \
	fi

check-docker:
	@if ! docker info > /dev/null 2>&1; then \
		echo "Error: Docker is not running"; \
		exit 1; \
	fi

check-deps:
	@if ! command -v python3 > /dev/null; then \
		echo "Error: Python3 is not installed"; \
		exit 1; \
	fi
	@if ! command -v node > /dev/null; then \
		echo "Error: Node.js is not installed"; \
		exit 1; \
	fi

# バージョン情報の表示
version:
	@echo "AI Learning Platform"
	@docker --version
	@docker-compose --version
	@python3 --version
	@node --version
	@npm --version
