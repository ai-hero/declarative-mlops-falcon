# Used for local development
build:
	docker build . -t zero_shot_text_classification:latest

run: 
	docker-compose up --build run 

test: 
	docker-compose run --build test 