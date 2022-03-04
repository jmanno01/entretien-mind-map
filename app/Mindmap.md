# Welcome to Mindmap

## This is a set of instructions that will help the user use this tool
- Please install `pip install pipenv`,  
- Navigate to the `entretien-mind-map` once clone on your local machine, 
- Run commands `pip install flask`, `pip install flask-sqlalchemy`, `pip install treelib`, `pip install markdown`, `pip install pytest`
- Then run the command `./bin/run.sh`
- Look on your terminal for the `ip_address` where the application will run, ex : `Running on http://ip_address:5000/`
- On `mac` -> `command + click`, or on `windows` -> `windows icon + click` to go the application website
- `(Press CTRL + C to quit)`

## `POST` to `/mindmap`
-  Any name could be included in the `name` field
```json
 curl -X POST -H "Content-Type: application/json" -d '{
  "name": "test-map"
}' http://localhost:5000/mindmaps
```

## `GET` infromations from `/mindmaps`
- `curl -X GET -H "Content-Type: application/json" http://localhost:5000/mindmaps`
```json
{
  "id": 1, 
  "name": "test-map"
}
```

## `POST` to `/mindmaps/Leaf`
- First way 
```json
 curl -X POST -H "Content-Type: application/json" -d '{
  "path": "I", "text": "", "mindmap_id": 1
}' http://localhost:5000/mindmaps/leaf
```

`output`: 
```json
{
     "[Output]": "This leaf has been successfully added"
}
```

- Other way
```json
 curl -X POST -H "Content-Type: application/json" -d '{
  "path": "I/dreamed", "text": "since I was able to sleep well", "mindmap_id": 1
}' http://localhost:5000/mindmaps/leaf
```

`output`: 
```json
{
     "[Output]": "This leaf has been successfully added"
}
```


## `GET` infromations from `/mindmaps/leaves`
- `curl -X GET -H "Content-Type: application/json" http://localhost:5000/mindmaps/leaves`

- `First Output:`
```json
{
    "Leaves": [
            "{'path': 'root/I', 'text': '', 'map_info': mindmap_id=1 | mindmap_name=test-map}"
        ]
}
```

- `Second Output:`
```json
{
    "Leaves": [
             "{'path': 'root/I/dreamed', 'text': 'since I was able to sleep well', 'map_info': mindmap_id=1 | mindmap_name=test-map}"
        ]
}
```


## Print the tree
- ` curl -X GET -H "Content-Type: application/json" http://localhost:5000/mindmaps/tree`

- `First Output:`
```json
root
    └── I
```

- `Second Output:`
```json
 root
    └── I
        └── dreamed
```


# Dockerfile 
- A Dockerfile is also provide, which will hep run the application in ddifferent environment

## Sets of command to build a docker image and run a container 
- Build the image: `docker build -t "desired_name" .`
- Run the docker container with a desire name: `docker run --name desired_name -d -p 5000:5000 desired_name`