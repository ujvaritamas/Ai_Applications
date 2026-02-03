this will start ollama with docker (not recommended on macbooks -> gpu won't be used if llm running inside docker container)

```
docker compose up -d

docker exec -it ollama /bin/bash 
ollama pull gemma3:4b
```