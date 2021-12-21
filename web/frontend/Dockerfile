# Create a small nginx container in two phases as explained there: https://tiangolo.medium.com/react-in-docker-with-nginx-built-with-multi-stage-docker-builds-including-testing-8cc49d6ec305

FROM  node:15 as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build

FROM nginx:1.19


COPY --from=build-stage /app/build/ /usr/share/nginx/html

EXPOSE 80

RUN echo "server { \n\
  listen 80; \n\
  location / { \n\
    root /usr/share/nginx/html; \n\
    index index.html index.htm; \n\
    try_files \$uri \$uri/ /index.html =404; \n\
  } \n\
  include /etc/nginx/extra-conf.d/*.conf; \n\
}" > /etc/nginx/conf.d/default.conf