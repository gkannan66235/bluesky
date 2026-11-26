# Build + push (AKS nodes are linux/amd64):
#   az acr login -n crazstarter
#   docker build --platform linux/amd64 -t crazstarter.azurecr.io/bluesky:0.1.0 .
#   docker push crazstarter.azurecr.io/bluesky:0.1.0
FROM python:3.12-slim
WORKDIR /app
COPY app/server.py .
ENV APP_VERSION=0.1.0
USER 65534:65534
EXPOSE 8080
CMD ["python", "server.py"]
