import streamlit as st
from imaging_plaza_fair_indicator_api import indicate_fair

st.set_page_config(layout="wide")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Swiss_Data_Science_Center_%28SDSC%29.png/1598px-Swiss_Data_Science_Center_%28SDSC%29.png?20220401084815", width=200)
st.title("Imaging Plaza Fair Level Indicator")


# Dropdown
graph = st.selectbox("Select a graph", 
                      ["https://epfl.ch/example/finalGraph", 
                       "https://epfl.ch/example/temporaryGraph"],
                       index=0)

# Input text
uri = st.text_input("Enter the entry URI", value="https://github.com/SDSC-ORD/gimie")

# Button
if st.button("Indicate FAIR suggestions"):
    # Function logic goes here
    # You can use the selected option and input text in your function
    
    shapesfile = "/app/imaging_plaza_fair_indicator_api/shapes.ttl"
    suggestions = indicate_fair(uri, graph, shapesfile)

    st.json(suggestions)
