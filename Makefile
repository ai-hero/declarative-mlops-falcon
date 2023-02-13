# Used for local development
build:
	docker build . -t zero_shot_text_classification:latest

run:
	docker-compose up run 

test:
	docker-compose run test 