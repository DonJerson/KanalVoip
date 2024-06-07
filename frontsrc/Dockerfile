     
# A minimal Docker image with Node and Puppeteer
#
# Initially based upon:
# https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md#running-puppeteer-in-docker

FROM node:14
# RUN apt-get update
WORKDIR /kamfront

COPY package.json .

RUN npm install
COPY ./ .
COPY webpack.config.js ./node_modules/react-scripts/config/webpack.config.js
COPY webpackDevServer.config.js ./node_modules/react-scripts/config/webpackDevServer.config.js

#COPY public/ .public/

# Disable warning error messages

ENV DISABLE_ESLINT_PLUGIN=true

CMD [ "npm","start"]