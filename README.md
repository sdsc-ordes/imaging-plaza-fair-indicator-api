# imaging-plaza-fair-indicator-api

## How to deploy it? 

1. Fill the .env file containing all the GRAPHDB Credentials. It's important to add `/repositories/imagingplaza` to your graphDB deployment. 

2. Build the docker image

``` bash
docker build -t imaging-plaza-fair-indicator-api:latest . 
```

3. Run the docker container

``` bash
docker run -it --rm -p 8000:15400 -p 8501:8501 --env-file .env imaging-plaza-fair-indicator-api:latest
```

After this command, the API endpoint will be in port 8000 while the GUI in port 8501

## How to use the API? 

The endpoint expect the uid in the path: `0.0.0.0:8000/indicate/?uri={URI}&graph{GRAPH}`

## How to use the GUI? 

Go to `0.0.0.0:8501`

## Robin's notes

```
//1. First, run the SHACL validate on the current graph, using shacl shapes specific to fair level calc
//2. Then, the result of that call should be uploaded into a graph on GraphDB - and given a temporary Graph URI.
//3. Then, the query below should be run on that temporary Graph URI, after which the graph can be deleted.
//4. The result of the query should be parsed and presented to the user.

//Note: query could be further improved after to include labels rather than path URI's,
// but lets first make it work before we start pulling results from multiple graphs
```

## DEV

These are useful command for development and testing.

```
poetry install
poetry shell
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 15400
```

How to run an example call?

```
http://0.0.0.0:15400/indicate/?uri=https://github.com/SDSC-ORD/gimie&graph=https://epfl.ch/example/temporaryGraph
```

How to use it as package
```
from fairindicator import *
graph="https://epfl.ch/example/temporaryGraph"
uri="https://github.com/SDSC-ORD/gimie"
suggestions = indicate_fair(uri, graph)
```

## Things to improve

1. Include the shapesfile as a parameter variables instead of a hardcoded path within the scripts.


## Changelog

- v0.0.8 - Dockerfile simplified
- v0.0.7 - Update to ontology v0.7
- v0.0.6 - Initial prod version. Ontology v0.6