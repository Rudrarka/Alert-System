FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
ENV FLASK_APP=modules

# CMD ["python","run.py"]
CMD ["sh","start.sh"]