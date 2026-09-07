FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir prometheus-client
COPY vdu_simulator.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "vdu_simulator.py"]