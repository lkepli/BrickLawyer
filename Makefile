install:
	pip install -r requirements.txt

run_api:
	uvicorn api.main:app --reload

test_structure:
	bash tests/test_structure.sh

docker_build:
	docker build -t bricklawyer-api .

docker_run:
	docker run -p 8080:8080 -e PORT=8080 bricklawyer-api
