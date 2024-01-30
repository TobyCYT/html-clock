sudo docker stop html-clock
sudo docker rm html-clock
sudo docker rmi myapp:0.0.1
sudo docker build -t myapp:0.0.1 .
sudo docker run -d -p 8080:5000 --name html-clock myapp:0.0.1 
# sudo docker run -d -p 42069:8080 myapp