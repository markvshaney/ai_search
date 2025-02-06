#app.py
import streamlit as st
import time
from src.search_engine import SearchEngine
from src.analyzer import Analyzer
from src.visualizer import Visualizer

# Initialize components
search_engine = SearchEngine()
analyzer = Analyzer()
visualizer = Visualizer()

# Page config
st.set_page_config(
    page_title="Search & Analysis Tool",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 Search & Analysis Tool")
st.markdown("""
This tool helps you search, analyze, and visualize information from the web.
Enter a search query below to get started.
""")

# Search interface
query = st.text_input("Enter your search query:", "")
max_results = st.slider("Maximum number of results:", 5, 20, 10)

if st.button("Search and Analyze"):
    if query:
        with st.spinner("Searching and analyzing..."):
            # Search
            progress_bar = st.progress(0)
            results = search_engine.search(query, max_results)
            progress_bar.progress(33)

            # Analysis
            if results:
                analysis = analyzer.analyze_search_results(results)
                progress_bar.progress(66)

                # Visualizations
                report_df = analyzer.generate_report(query, results, analysis)
                progress_bar.progress(100)
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "Search Results", 
                    "Analysis", 
                    "Visualizations",
                    "Report"
                ])

                with tab1:
                    st.subheader("Search Results")
                    for i, result in enumerate(results, 1):
                        with st.expander(f"{i}. {result['title']}"):
                            st.write(result['snippet'])
                            st.write(f"URL: {result['url']}")

                with tab2:
                    st.subheader("Analysis")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Top Words**")
                        st.write(analysis['word_frequency'])
                    
                    with col2:
                        st.write("**Named Entities**")
                        st.write(analysis['entity_analysis'])
                    
                    st.write("**Summary**")
                    st.write(analysis['summary'])

                with tab3:
                    st.subheader("Visualizations")
                    
                    # Word frequency plot
                    st.plotly_chart(
                        visualizer.create_word_frequency_plot(
                            analysis['word_frequency']
                        ),
                        use_container_width=True
                    )
                    
                    # Entity distribution
                    st.plotly_chart(
                        visualizer.create_entity_distribution(
                            analysis['entity_analysis']
                        ),
                        use_container_width=True
                    )
                    
                    # Results overview
                    st.plotly_chart(
                        visualizer.create_results_overview(results),
                        use_container_width=True
                    )

                with tab4:
                    st.subheader("Analysis Report")
                    st.dataframe(report_df, use_container_width=True)
                    
                    # Download button for report
                    csv = report_df.to_csv(index=False)
                    st.download_button(
                        label="Download Report as CSV",
                        data=csv,
                        file_name=f'search_analysis_{query}.csv',
                        mime='text/csv',
                    )

            else:
                st.error("No results found. Please try a different search query.")
    else:
        st.warning("Please enter a search query.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Streamlit, NLTK, and Plotly</p>
</div>
""", unsafe_allow_html=True)
