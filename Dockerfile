FROM python:3-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/DarkCat09/python-aternos.git
RUN cd python-aternos
RUN pip install -e .[dev]

CMD [ "python", "./main.py" ]