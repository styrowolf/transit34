default:
    just --list

redis:
    valkey-server --save "" --appendonly no

server-local:
    DATABASE=/Users/oguzkurt/programming/pt/data/2024-11-29/iett.sqlite3 uv run fastapi dev src/t34/__init__.py

redis-docker:
    docker run -p 6379:6379 valkey/valkey:7.2.5