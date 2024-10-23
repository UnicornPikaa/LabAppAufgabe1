FROM python:3

WORKDIR /src/app

COPY CloudNutzungsAnwendung.py ./

RUN pip install requests

CMD ["python", "./CloudNutzungsAnwendung.py"]