FROM node:16
WORKDIR /express
COPY ./package.json ./

RUN npm install

COPY ./server.js ./
COPY ./DialProCertificates /express/
COPY . ./
# COPY ./build /express/build/

EXPOSE 80 443

CMD [ "node", "server.js" ]