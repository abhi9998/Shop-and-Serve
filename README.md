# ECE651-SnS

Project for ECE651


## Python code formatter
Python code is formatted using 'black'. It can be installed using below command 
```
pip install black
```

To format file
```
black {source_file_or_directory}
```

## Run server
```
python3 manage.py runserver
```

## To deploy changes
```
sudo heroku container:push web --app ece651-sns-qa
sudo heroku container:release web --app ece651-sns-qa
```


## Command useful for debugging 
```
sudo heroku login
heroku git:remote -a ece651-sns-qa
git push <dev-branch>:main
sudo docker build --tag sns:latest . # To build 
```
