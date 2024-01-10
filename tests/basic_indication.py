from ..app import fairindicator

uri = "https://github.com/ImagingDataCommons/dicom-microscopy-viewer"
graph = "temporary"

suggestions = fairindicator.indicate_fair(uri, graph)

print(suggestions)