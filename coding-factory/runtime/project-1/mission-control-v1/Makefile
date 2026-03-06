SHELL := /bin/bash

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

validate:
	docker compose config >/dev/null

seed-reset:
	docker compose down -v
	docker compose up -d

backup:
	./scripts/backup-postgres.sh

restore:
	@echo "Usage: ./scripts/restore-postgres.sh /path/to/backup.sql.gz"
