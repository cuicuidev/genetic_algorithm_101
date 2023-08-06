import streamlit as st
from routes.a_simple_example_page import aSimpleExamplePage
from routes.genetic_algorithms_page import geneticAlgorithmsPage
from routes.playground_page import playgroundPage
from routes.about_page import aboutPage

PAGE_CONFIG = {"page_title"             : "Genetic Algorithms 101",
                "page_icon"             : ":seedling:",
                "layout"                : "wide",
                "initial_sidebar_state" : "expanded"}

def main():

    st.set_page_config(**PAGE_CONFIG)

    pages = {
        "Genetic Algorithms": geneticAlgorithmsPage,
        "A Simple Example": aSimpleExamplePage,
        "Playground": playgroundPage,
        "About": aboutPage
    }

    page_name = st.sidebar.selectbox(label = "Menu", options = list(pages.keys()), index = 0)

    pages[page_name]()

if __name__ == '__main__':
    main()
