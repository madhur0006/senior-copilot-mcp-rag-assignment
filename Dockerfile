# Placeholder root Dockerfile.
# Later this may build the backend image, or docker-compose will use per-service Dockerfiles.

FROM python:3.12-slim
WORKDIR /app
COPY . /app
CMD ["python", "-c", "print('Replace with real service entrypoint')"]
