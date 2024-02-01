import rdflib
import requests
import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, QueryResult, TURTLE, CSV, JSONLD
import pyshacl
import json 

get_suggestion_query: str = """
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX : <https://epfl.ch/example/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

select ?focusNode ?path ?ToAchieve
WHERE{
    
    {
        SELECT (MIN(?fairLevel) AS ?minFair) 
        WHERE {
            ?s a sh:ValidationResult;
                 sh:focusNode ?focusNode ;
                 sh:resultPath ?path;
                 sh:resultMessage ?ToAchieve.
            BIND(STRAFTER(?ToAchieve, "Fair level ") AS ?fairLevelNum)
            BIND(xsd:integer(?fairLevelNum) AS ?fairLevel)
        }
    }
    ?s a sh:ValidationResult;
         sh:focusNode ?focusNode ;
         sh:resultPath ?path;
         sh:resultMessage ?ToAchieve.
    BIND(STRAFTER(?ToAchieve, "Fair level ") AS ?fairLevelNum)
    BIND(xsd:integer(?fairLevelNum) AS ?fairLevel)
    FILTER (?fairLevel = ?minFair)
}
"""



results_g = rdflib.Graph()
results_g.parse("test.ttl", format="turtle")
result2 = results_g.query(get_suggestion_query)
result2.serialize(format='json')
# print(result2.serialize(format='json'))
suggestions_dict = json.loads(result2.serialize(format='json'))
if "head" in suggestions_dict:
    del suggestions_dict["head"]
suggestions_dict = json.dumps(suggestions_dict)
print(suggestions_dict)
# suggestions_dict = json.loads(s='test.json',)
# if "head" in suggestions_dict:
#     del suggestions_dict["head"]
# suggestions_dict = json.dumps(suggestions_dict)

