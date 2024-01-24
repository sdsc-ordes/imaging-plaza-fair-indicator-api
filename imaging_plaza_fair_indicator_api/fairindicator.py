import rdflib
import requests
import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, QueryResult, TURTLE, CSV
import pyshacl
import json 

def get_data_from_graphdb(db_host: str, 
                          db_user: str, 
                          db_password: str,
                          softwareURI: str,
                          graph:str) -> bytes:
    """
    Get data from GraphDB.

    Args:
        db_host: The host URL of the GraphDB.
        db_user: The username for authentication.
        db_password: The password for authentication.
        softwareURI: Indentifier of target software
        graph: Graph where the entry is located

    Returns:
        The data as a bytes object.
    """

    get_relevant_software_query: str = """
    PREFIX ex: <https://epfl.ch/example/>
    CONSTRUCT {{
    ?subject ex:graph <{graph}>  .
    ?subject ?predicate ?object .
    ?object ?p ?o .
    }} WHERE {{
        GRAPH <{graph}> {{
        {{?subject ?predicate ?object .
        filter(?subject = <{softwareURI}> )
        OPTIONAL {{ ?object ?p ?o . }}
                }}}}}}
    """.format(softwareURI=softwareURI, graph=graph) 

    sparql = SPARQLWrapper(db_host)
    sparql.setQuery(get_relevant_software_query)
    sparql.setReturnFormat(TURTLE)
    sparql.setCredentials(user=db_user, passwd=db_password)
    results = sparql.query().convert()
    return results

def load_data_into_rdflib(results: bytes) -> rdflib.Graph:
    """
    Load data into rdflib.

    Args:
        results: The data to be loaded as a string in Turtle format.

    Returns:
        The loaded data as an rdflib.Graph object.
    """
    data_g = rdflib.Graph()
    data_g.parse(data=results, format="turtle")
    return data_g

def load_shapes_into_rdflib(shapes_path: str) -> rdflib.Graph:
    """
    Load SHACL shapes into rdflib graph object.

    Args:
        shapes_path: The path to the SHACL shapes file in turtle format.

    Returns:
        The loaded SHACL shapes as an rdflib.Graph object.
    """
    shapes_g = rdflib.Graph()
    shapes_g.parse(file=open(shapes_path), format="turtle")
    return shapes_g

def run_shacl_validation(data_g: rdflib.Graph|str|bytes, shapes_g: rdflib.Graph|str|bytes) -> rdflib.Graph:
    """
    Run SHACL validation with pyshacl.

    Args:
        data_g: The data graph as an rdflib.Graph object, string or file.
        shapes_g: The SHACL shapes graph as an rdflib.Graph object, string or file.

    Returns:
        The validation results as an rdflib.Graph object.
    """
    validation_result = pyshacl.validate(data_graph=data_g, 
                                         shacl_graph=shapes_g, 
                                         inference='rdfs', 
                                         serialize_report_graph='turtle')
    validation_result = validation_result[1]
    results_g = rdflib.Graph()
    results_g.parse(validation_result, format="turtle")
    results_g.serialize(format="turtle")
    return results_g

def get_suggestions(results_g: rdflib.Graph) -> str:
    """
    Get suggestions on which properties to fill in to move to a next fair level from the SHACL validation results.

    Args:
        results_g: The SHACL validation report as an rdflib.Graph object.

    Returns:
        The suggestions as a serialized JSON string.
    """

    get_suggestion_query: str = """
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX : <https://epfl.ch/example/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    CONSTRUCT {
        ?s ?path ?ToAchieve
    }
    WHERE{
    ?s a sh:ValidationResult;
       sh:resultPath ?path;
       sh:resultMessage ?ToAchieve.
    BIND(STRAFTER(?ToAchieve, "Fair level ") AS ?fairLevelNum)
    BIND(xsd:integer(?fairLevelNum) AS ?fairLevel)
    FILTER (?fairLevel = ?minFair)
    {
        SELECT (MIN(?fairLevel) AS ?minFair)
        WHERE {
            ?s a sh:ValidationResult;
               sh:resultPath ?path;
               sh:resultMessage ?ToAchieve.
            BIND(STRAFTER(?ToAchieve, "Fair level ") AS ?fairLevelNum)
            BIND(xsd:integer(?fairLevelNum) AS ?fairLevel)
            }
        } 
    }
    """

    result2 = results_g.query(get_suggestion_query)
    return result2.serialize(format="json")


def indicate_fair(softwareURI:str, graph:str, shapesfile:str = "shapes.ttl") -> dict:

    load_dotenv()

    # Set SPARQL endpoint authentication
    db_host: str = os.environ.get("GRAPHDB_URL")
    db_user: str = os.environ.get("GRAPHDB_USER")
    db_password: str = os.environ.get("GRAPHDB_PASSWORD")

    #graph: str = 'https://epfl.ch/example/finalGraph'
    #softwareURI: str = 'https://github.com/SDSC-ORD/gimie'



    results = get_data_from_graphdb(db_host, db_user, db_password, softwareURI, graph)
    data_g = load_data_into_rdflib(results)

    shapes_g = load_shapes_into_rdflib(shapesfile)
    results_g = run_shacl_validation(data_g, shapes_g)
    suggestions = get_suggestions(results_g)

    suggestions_dict = json.loads(suggestions)
    if "head" in suggestions_dict:
        del suggestions_dict["head"]
    suggestions_dict = json.dumps(suggestions_dict)
    return suggestions_dict


