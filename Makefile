install:
		uv sync

render-start:
    gunicorn task_manager.wsgi

build:
		./build.sh

lint:
		uv run ruff check task_manager $(ARGS)

lint-fix:
		$(MAKE) lint ARGS=--fix