import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # This should be in a config file ideally

def render_policy_search():
    """
    Renders an interface for searching policy documents via the backend API.
    """
    st.header("Semantic Search for Policy Documents")
    
    search_query = st.text_input(
        "Search Query:",
        placeholder="e.g., 'What are the city's policies on renewable energy?'"
    )

    if st.button("Search Policies"):
        if search_query:
            with st.spinner("Searching for relevant documents..."):
                try:
                    params = {"query": search_query, "top_k": 5}
                    response = requests.get(f"{API_URL}/policy/search-docs", params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    st.subheader("Search Results")
                    results = data.get("results", [])
                    
                    if not results:
                        st.info("No matching documents found.")
                    else:
                        for result in results:
                            with st.expander(f"**Score: {result['score']:.2f}** - Document ID: `{result['id']}`"):
                                st.markdown(result.get('metadata', {}).get('text', 'No text available.'))
                                summary = result.get('summary', None)
                                if summary:
                                    st.markdown("**Summary:**")
                                    st.success(summary)
                                else:
                                    st.info("No summary generated.")

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to perform search. Could not connect to the API.")
        else:
            st.warning("Please enter a search query.") 