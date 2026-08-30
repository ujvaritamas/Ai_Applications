build:
	docker build -t test_openwebui_langchain .

run:
	docker run -d --name test_openwebui_langchain -p 8000:8000 test_openwebui_langchain

clean:
	docker container rm -f test_openwebui_langchain
	docker image rm -f test_openwebui_langchain

run_all:
	docker-compose up -d

clean_all:
	docker-compose down -v
