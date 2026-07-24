MANAGE := uv run python manage.py

install:
		uv sync

render-start:
		gunicorn task_manager.wsgi

build:
		./build.sh

collectstatic:
		$(MANAGE) collectstatic --noinput

migrate:
		$(MANAGE) migrate

lint:
		uv run ruff check task_manager $(ARGS)

lint-fix:
		$(MAKE) lint ARGS=--fix

test:
		$(MANAGE) test