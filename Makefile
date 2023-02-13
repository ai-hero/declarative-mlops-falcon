# Used for local development
build:
	docker build . -t zero_shot_text_classification:latest

run: build
	docker-compose up --build zero_shot_text_classification

test: build
	docker-compose run --build zero_shot_text_classification test 