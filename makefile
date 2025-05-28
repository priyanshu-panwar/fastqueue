.PHONY: run test 

# Run the FastAPI app
run:
	poetry run uvicorn app.main:app --reload --port 9080

# Run tests
test:
	poetry run pytest

# Build Docker image with optional TAG (default: latest)
build:
	docker build -t fastqueue:$(TAG) .

# Run Docker image with optional TAG (default: latest)
docker-run:
	docker run -p 9080:9080 fastqueue:$(TAG)

# Default TAG value
TAG ?= latest