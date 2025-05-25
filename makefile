.PHONY: run test 

# Run the FastAPI app
run:
	poetry run uvicorn app.main:app --reload

# Run tests
test:
	poetry run pytest