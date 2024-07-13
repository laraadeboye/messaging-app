
# Messaging System with RabbitMQ/Celery and Python Application behind Nginx
### Table of Contents
- Overview
- Prerequisites
- Steps
    - Step 1: Install RabbitMQ
    - Step 2: Install Celery
    - Step 3: Install Nginx
    - Step 4: Install Ngrok
    - Step 5: Start the Application
- App Usage
- Conclusion

## Overview
This project will teach you:

- How to set up and use RabbitMQ and Celery for task queuing and worker management.
- How to create a Python application using Flask and integrate it with Celery and RabbitMQ.
- How to configure Nginx as a reverse proxy server to serve your application.
- How to expose your local application endpoint to the public using ngrok.


Message brokers act as intermediaries between different services, ensuring reliable communication. They store incoming requests in a queue and serve them sequentially to receiving services. By decoupling services in this manner, you enhance scalability and performance. RabbitMQ is a message broker that implements the Advanced Message Queuing Protocol (AMQP). It facilitates communication between different components of a distributed system by sending messages between them. Celery is a distributed task queue framework that allows you to run asynchronous tasks in the background. It is often used for long-running or scheduled background tasks in web applications.

## Prerequisites
Linux machine
Python 3.10 or higher

## Steps
#### Step 1: Install RabbitMQ

1. Update system packages.

```sh
sudo apt update
Install RabbitMQ server
```

2. Install RabbitMQ server.

```sh
sudo apt install rabbitmq-server -y
Start the RabbitMQ service
```

3. Start the RabbitMQ service.

```sh
sudo systemctl start rabbitmq-server
Enable RabbitMQ service on boot
```

4. Enable RabbitMQ service on boot.

```sh
sudo systemctl enable rabbitmq-server
Check the status of RabbitMQ
```

5. Check the status of RabbitMQ

```sh
sudo systemctl status rabbitmq-server
Set up the RabbitMQ Management Plugin
```

6. [Optional] Set up the RabbitMQ Management Plugin

```sh
sudo rabbitmq-plugins enable rabbitmq_management
sudo systemctl restart rabbitmq-server
```

7. Access RabbitMQ Management Web interface

- **URL**: http://localhost:15672/
- **Default credentials**:
   - Username: guest
   - Password: guest


#### Step 2: Install Celery
Install Celery with the pip library:

```sh
pip install "celery[librabbitmq]"
```
or

```
pip install -U celery
```

#### Step 3: Install Nginx
1. Update the apt package manager

```sh
sudo apt update -y
```
2. Install Nginx

```sh
sudo apt install nginx -y
```

3. Start Nginx

```sh
sudo systemctl start nginx
```

4. Create a new configuration file for the application

```sh
sudo nano /etc/nginx/sites-available/messaging-app
```

5. Add the following configuration to the file:

```sh
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
6. Enable the configuration by creating a symlink to sites-enabled:

```sh
sudo ln -s /etc/nginx/sites-available/messaging-app /etc/nginx/sites-enabled/
```

7. Verify the link was created:

```sh
ls -l /etc/nginx/sites-enabled/
```

8. Test Nginx for syntax errors:

```sh
sudo nginx -t
```

9. Reload Nginx to apply changes:

```sh
sudo systemctl reload nginx
```

#### Step 4: Install Ngrok
1. Install and configure Ngrok

```sh
sudo apt install ngrok
ngrok --version
```
2. Sign up on [ngrok website](https://dashboard.ngrok.com/signup) and get [authentication token](https://dashboard.ngrok.com/get-started/your-authtoken)

3. Run on terminal to authenticate the downloaded app:

```sh
ngrok authtoken <YOUR_AUTH_TOKEN>
```

#### Step 5: Start the Application
1. Clone this repository and change directory to the messaging-app folder:

```sh
cd messaging-app
```
2. Create a file to log the date and time messages with appropriate permissions:

```sh
sudo touch /var/log/messaging_system.log
sudo chown $USER:$USER /var/log/messaging_system.log
sudo chmod 664 /var/log/messaging_system.log
```
3. Start a Python virtual environment to manage dependencies:

```sh
python3 -m venv venv
source venv/bin/activate
```
4. Install the dependencies in the requirements.txt:

```sh
pip3 install -r requirements.txt
```
or to install and upgrade the dependencies:

```sh
pip3 install -r requirements.txt --user --upgrade
```
5. Run the different components of the app on different terminals:

- On `app.py` terminal:

```sh
python3 app.py
```
This command starts the application.

- On `tasks.py` terminal:

```sh
celery -A tasks worker --loglevel=info
```

- On Ngrok terminal:

```sh
ngrok http 5000
```
6. Copy the custom link exposed by ngrok and paste it on a web browser to access the application. The link is similar to:

```sh
https://19e3-102-89-40-117.ngrok-free.app/
```
## App Usage
The app interacts with RabbitMQ/Celery for email sending and logging functionality.

- **For Email sending**, type the following in your web browser, replacing the [ngrok endpoint] and [Destination Email] with the exposed endpoint and valid email respectively:

```sh
https://[ngrok endpoint]/?sendmail=[Destination Email]
```

e.g.

```sh
https://19e3-102-89-40-117.ngrok-free.app/?sendmail=example@gmail.com
```
The web session will display: `Email to [Destination Email] queued for sending`.

- **For message logging**, type the following in your web browser:

```sh
https://[ngrok endpoint]/?talktome=1
```
e.g.

```sh
https://19e3-102-89-40-117.ngrok-free.app/?talktome=1
```
The web session will display: `Current time and date logged`.

## Conclusion
This app demonstrates how RabbitMQ and Celery are used for task queue management and how to integrate them with a Python application and Nginx.




