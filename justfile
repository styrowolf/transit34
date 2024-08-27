default:
    just --list

redis:
    valkey-server --save "" --appendonly no

redis-docker:
    docker run -p 6379:6379 valkey/valkey:7.2.5