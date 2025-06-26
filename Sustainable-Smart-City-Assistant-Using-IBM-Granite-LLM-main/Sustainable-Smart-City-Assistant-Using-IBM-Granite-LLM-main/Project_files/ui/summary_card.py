import streamlit as st

def summary_card(title, value, delta=None, delta_color="normal", help_text=None):
    """
    Displays a single KPI metric in a styled card.
    """
    with st.container():
        st.markdown(
            f"""
            <div style="border: 1px solid #e6e6e6; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem;">
                <h3 style="margin-top: 0; margin-bottom: 0.5rem;">{title}</h3>
                <h1 style="margin-top: 0; margin-bottom: 0.5rem;">{value}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        # The st.metric is not easily styleable inside the div, so we place it outside
        # and rely on the container for grouping. A more advanced implementation
        # might use pure HTML for the whole component.
        # For this version, we will stick to a simpler markdown-based card.
        
    # Example of how it could be used with st.metric if styling was less important:
    # with st.container():
    #     st.metric(label=title, value=value, delta=delta, delta_color=delta_color, help=help_text) 