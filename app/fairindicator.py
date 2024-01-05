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
    CONSTRUCT {
      ?subject ex:graph <https://epfl.ch/example/finalGraph>  .
      ?subject ?predicate ?object .
      ?object ?p ?o .
    } WHERE {
        GRAPH <https://epfl.ch/example/finalGraph> {
        {?subject ?predicate ?object .
         filter(?subject = <https://github.com/ImagingDataCommons/dicom-microscopy-viewer> )
        OPTIONAL { ?object ?p ?o . }
                }}}
"""
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
# sparql = SPARQLWrapper(db_host)
# sparql.setQuery(get_relevant_software_query)
# sparql.setReturnFormat(TURTLE)
# sparql.setCredentials(user=db_user, passwd=db_password)
# results = sparql.query().convert()

# #Load data into rdflib
# data_g = rdflib.Graph()
# data_g.parse(data=results, format="turtle")
# data_g.serialize(destination='data.ttl', format='turtle')

###TEMPORARY: Load data from file
data_g = rdflib.Graph()
data_g.parse(file=open("./data.ttl"), format="turtle")
###ENDOFTEMPORARY

#Load SHACL shapes into rdflib
shapes_g = rdflib.Graph()
shapes_g.parse(file=open("./app/shapes.ttl"), format="turtle")

#Run SHACL validation with pyshacl
validation_result = pyshacl.validate(data_graph = data_g, 
                                     shacl_graph = shapes_g, 
                                     inference = 'rdfs', 
                                     serialize_report_graph = 'turtle')
validation_result = validation_result[1]
# print(validation_result)
shapes_g.parse(validation_result, format="turtle")
shapes_g.serialize(format="turtle")

#Run query on SHACL validation result to get suggestions
result2 = shapes_g.query(get_suggestion_query)
print(result2.serialize(format="csv"))

#TODO: Run query on SHACL validation result to get suggestions




def requestGraph(uid):


    pass

def indicate(): #TODO: It receives a JSON LD?


    return "" #TODO: Indications provided