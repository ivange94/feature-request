FROM python:3
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN flask db upgrade
CMD ["flask", "run", "--host=0.0.0.0"]
