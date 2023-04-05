FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache --user -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]