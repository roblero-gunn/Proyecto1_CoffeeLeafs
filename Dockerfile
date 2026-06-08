FROM python:3.10-slim
WORKDIR /code
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./frontend /code/frontend
EXPOSE 8000
EXPOSE 7860
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & python frontend/ui.py
