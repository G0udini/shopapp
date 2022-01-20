# Shop Application

### Shop appliation where you can buy fake products, have a discount or add items to cart for later purchase

___

## Build & Run

### requirements

* docker
* .env file in root directory with following rules:

```shell
SECRET_KEY=
DEBUG=True

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# RabbitMQ settings
RABBITMQ_PROTOCOL=amqp
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# Braintree settings to have a fake ability to process payment
# You must to login in Braintree Sandbox to have this keys
BRAINTREE_MERCHANT_ID=
BRAINTREE_PUBLIC_KEY=
BRAINTREE_PRIVATE_KEY=
```

Use **docker-compose up --build** command to run app in docker

## Description

This application is realize a real online shop where you can:

1. Add products to the cart and continue searching for products
2. Buy products with fake payment process
3. See recommendations wich shows what other people buy with chosen products
4. Choose category you want
5. Use discount coupons
6. Have an email with payment details
7. Have pdf with order details

## Features

1. Celery with RabbitMQ for delayed tasks(sending email)
2. Custom cart that saved in session
3. Redis for dynamically adding and calculating recommendations for products
4. Generating PDF by html and css
5. Fake payment that processed by a third-party service
