FROM python:3.14.7

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./example /app

EXPOSE 8000

#CMD ["sleep", "infinity"]

ENTRYPOINT ["uv", "run", "main.py"]
