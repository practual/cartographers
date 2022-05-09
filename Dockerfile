FROM node:12

WORKDIR /home/node/app

COPY . .

RUN yarn install

RUN yarn run webpack

FROM python:3

WORKDIR /usr/src/app

COPY . .

COPY --from=0 /home/node/app/static/ static/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir log

EXPOSE 5000

CMD [ "python", "./app.py" ]

