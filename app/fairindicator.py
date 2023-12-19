import rdflib
import requests
import os

db_host = os.environ.get("GRAPHDB_URL")
db_user = os.environ.get("GRAPHDB_USER")
db_password = os.environ.get("GRAPHDB_PASSWORD")


query = """
export const getFairSuggestionQuery = async (graph: string, repository: string) => `
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX : <https://epfl.ch/example/>
SELECT (GROUP_CONCAT(DISTINCT ?path; SEPARATOR=', ') AS ?youAreMissing) ?ToAchieve
WHERE {
  GRAPH <${TemporaryValidationGraphOutput}> {
    ?s a sh:ValidationResult.
    ?s sh:resultPath ?path.
    ?s sh:resultMessage ?ToAchieve.
  }
}
GROUP BY ?ToAchieve
ORDER BY ?ToAchieve
LIMIT 1
"""


def requestGraph(uid):


    pass

def indicate(): #TODO: It receives a JSON LD?


    return "" #TODO: Indications provided