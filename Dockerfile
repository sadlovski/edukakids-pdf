FROM python:3.10-slim
WORKDIR /app
RUN pip install reportlab
COPY . /app
CMD ["python3", "gerar_modulo1.py"]