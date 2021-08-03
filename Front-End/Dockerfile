FROM node:current-alpine3.11
WORKDIR /STOCK-RESULTS-FRONT-END
ENV PATH="./node_modules/.bin:$PATH"
COPY . .
RUN npm install 
RUN npm run build
CMD ["npm" , "start"]
