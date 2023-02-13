# Used for local development
build:
	docker build . -t zero_shot_text_classification:latest

run:
	docker-compose up --build zero_shot_text_classification

test:
	docker-compose run --build zero_shot_text_classification test 