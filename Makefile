# Build images
build:
	docker compose build

# Start all services
up:
	docker compose up

up-d:
	docker compose up -d

# Stop all services
down:
	docker compose down

# Stop and remove volumes
down-v:
	docker compose down -v

# Restart all services
restart:
	docker compose restart

# View logs
logs:
	docker compose logs -f

logs-web:
	docker compose logs -f web

logs-celery:
	docker compose logs -f celery

# Run migrations
migrate:
	docker compose exec web python manage.py migrate

# Make migrations
makemigrations:
	docker compose exec web python manage.py makemigrations

# Create superuser
createsuperuser:
	docker compose exec web python manage.py createsuperuser

# Open Django shell
shell:
	docker compose exec web python manage.py shell

# Open psql shell
psql:
	docker compose exec postgres psql -U postgres -d otp_authentication_api

# Open redis-cli
redis-cli:
	docker compose exec redis redis-cli

# Run tests
test:
	docker compose exec web python manage.py test

# Rebuild and restart
rebuild:
	docker compose down
	docker compose up --build
