from imaging_plaza_fair_indicator_api import fairindicator
# print(indicate_fair('https://github.com/flatironinstitute/CaImAn', 'https://imaging-plaza.epfl.ch/finalGraph', 'ImagingOntologyCombined.ttl'))

uri = "https://github.com/flatironinstitute/CaImAn"
graph = "https://imaging-plaza.epfl.ch/finalGraph"

suggestions = fairindicator.indicate_fair(uri, graph, "ImagingOntologyCombined.ttl")

print(suggestions)