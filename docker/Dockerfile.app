FROM python:3.12.3-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_COMPILE_BYTECODE=1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/client/ ./client/
COPY src/schema/ ./schema/
COPY src/streamlit_app.py .

CMD ["streamlit", "run", "streamlit_app.py"]
