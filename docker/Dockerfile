# Python 3.11 ベースイメージを使用
FROM python:3.11

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをコピー
COPY code/requirements.txt /app/.
COPY code/*.py /app/.
COPY code/credential /app/credential/.

# パッケージをインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ポート 8080 を開放（Cloud Functions のデフォルトポート）
EXPOSE 8080

# Cloud Functions をエミュレートするために functions-framework を実行
CMD ["functions-framework", "--target=main", "--debug", "--port=8080"]

# curl -X POST http://localhost:8080/ -H "Ce-Id: 12345" -H "Ce-Type: my-event" -H "Ce-Source: curl-command" -H "Ce-Specversion: 1.0"
