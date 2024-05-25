FROM python:3.9-slim

RUN useradd -ms /bin/bash appuser

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py

USER appuser

CMD ["flask", "run", "--host=0.0.0.0"]
