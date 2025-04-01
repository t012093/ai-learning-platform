FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# 環境変数の設定
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# ポートの公開
EXPOSE 3001

# アプリケーションの起動
CMD ["python", "-m", "mcp_server"]
