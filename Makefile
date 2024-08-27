run:
	cp -n .env.example .env || true
	docker-compose up --build
