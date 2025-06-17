# Makefile — Simplify Dev Workflow

install:
	pip install -r requirements.txt

run:
	python assistant/main.py

docker-build:
	docker build -t ai_personal_assistant .

docker-run:
	docker run -it --env-file .env ai_personal_assistant
