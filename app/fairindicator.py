import rdflib
import requests
import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, QueryResult, TURTLE, CSV
import pyshacl

load_dotenv()
#set SPARQL endpoint authentication
db_host = os.environ.get("GRAPHDB_URL")
db_user = os.environ.get("GRAPHDB_USER")
db_password = os.environ.get("GRAPHDB_PASSWORD")

graph = 'https://epfl.ch/example/finalGraph'
softwareURI = 'https://github.com/SDSC-ORD/gimie'

get_relevant_software_query = """
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
                }}}}
""".format(softwareURI=softwareURI, graph=graph)

get_suggestion_query = """
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX : <https://epfl.ch/example/>
SELECT (GROUP_CONCAT(DISTINCT ?path; SEPARATOR=', ') AS ?youAreMissing) ?ToAchieve
WHERE {
  {    ?s a sh:ValidationResult.
    ?s sh:resultPath ?path.
    ?s sh:resultMessage ?ToAchieve.
  }
}
GROUP BY ?ToAchieve
ORDER BY ?ToAchieve
LIMIT 1
"""

#Get data from GraphDB
def get_data_from_graphdb(db_host, db_user, db_password):
    sparql = SPARQLWrapper(db_host)
    sparql.setQuery(get_relevant_software_query)
    sparql.setReturnFormat(TURTLE)
    sparql.setCredentials(user=db_user, passwd=db_password)
    results = sparql.query().convert()
    return results

#Load data into rdflib
def load_data_into_rdflib(results):
    data_g = rdflib.Graph()
    data_g.parse(data=results, format="turtle")
    return data_g

#Load SHACL shapes into rdflib
def load_shapes_into_rdflib(shapes_path):
    shapes_g = rdflib.Graph()
    shapes_g.parse(file=open(shapes_path), format="turtle")
    return shapes_g

#Run SHACL validation with pyshacl
def run_shacl_validation(data_g, shapes_g):
    validation_result = pyshacl.validate(data_graph = data_g, 
                                     shacl_graph = shapes_g, 
                                     inference = 'rdfs', 
                                     serialize_report_graph = 'turtle')
    validation_result = validation_result[1]
    results_g = rdflib.Graph()
    results_g.parse(validation_result, format="turtle")
    results_g.serialize(format="turtle")
    return results_g

def get_suggestions(results_g):
    #Run query on SHACL validation result to get suggestions
    result2 = results_g.query(get_suggestion_query)
    return result2.serialize(format="json")







def requestGraph(uid):


    pass

def indicate(): #TODO: It receives a JSON LD?


    return "" #TODO: Indications provided