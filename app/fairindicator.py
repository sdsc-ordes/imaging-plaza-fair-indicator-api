import rdflib
import requests
import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, QueryResult, TURTLE, CSV
import pyshacl

load_dotenv()

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

query = """
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

sparql = SPARQLWrapper(db_host)
sparql.setQuery(get_relevant_software_query)
sparql.setReturnFormat(TURTLE)
sparql.setCredentials(user=db_user, passwd=db_password)
results = sparql.query().convert()
# print(results)
###WORKS UPTO HERE, Now convert to JSON-LD, put in a rdflib graph and then use the indicator function on that

g = rdflib.Graph()
g.parse(data=results, format="turtle")
g.serialize(destination='data.ttl', format='turtle')

shapes = open("./app/shapes.ttl", "r").read()
# print(shapes)

# print(g.serialize(format="turtle"))

#TODO: Run SHACL validation on result
g2 = rdflib.Graph()
validation_result = pyshacl.validate(data_graph = g, shapes_graph = shapes, inference = 'rdfs', serialize_report_graph = 'turtle')
validation_result = validation_result[1]
g2.parse(validation_result, format="turtle")
g2.serialize(format="turtle")
report = open('report.ttl', 'w')
print(g2.serialize(format="turtle"))
print(report)

error_report = open('report.ttl', 'r').read()
result2 = g2.query(query)

print(result2.serialize(format="csv"))

#TODO: Run query on SHACL validation result to get suggestions




def requestGraph(uid):


    pass

def indicate(): #TODO: It receives a JSON LD?


    return "" #TODO: Indications provided