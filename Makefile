# Used for local development
build:
	docker build . -t zero_shot_text_classification:latest

run: build
	docker-compose up run 

test: build
	docker-compose run test 