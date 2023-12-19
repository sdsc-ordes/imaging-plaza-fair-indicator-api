# imaging-plaza-fair-indicator-api

## How to deploy it? 

1. Fill the .env file containing all the GRAPHDB Credentials. 
2. Build the docker image
```
docker build -t imaging-plaza-fair-indicator:latest . 
```
3. Run the docker container
```
docker run -it --rm -p 8000:15400 -p 8501:8501 -env-file .env imaging-plaza-fair-indicator:latest
```

After this command, the API endpoint will be in port 8000 while the GUI in port 8501

## How to use the API? 

The endpoint expect the uid in the path: `0.0.0.0:8000/indicate/{uid}`

## How to use the GUI? 

Enter in `0.0.0.0:8501`

## Robin's notes

```
//1. First, run the SHACL validate on the current graph, using shacl shapes specific to fair level calc
//2. Then, the result of that call should be uploaded into a graph on GraphDB - and given a temporary Graph URI.
//3. Then, the query below should be run on that temporary Graph URI, after which the graph can be deleted.
//4. The result of the query should be parsed and presented to the user.

//Note: query could be further improved after to include labels rather than path URI's,
// but lets first make it work before we start pulling results from multiple graphs
```