FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn httpx openai requests
COPY . .
# The container will run the proxy by default
CMD ["uvicorn", "vaas_proxy:app", "--host", "0.0.0.0", "--port", "8000"]