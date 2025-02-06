import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List

class Visualizer:
    def create_word_frequency_plot(self, word_freq: Dict):
        """Create a bar chart for word frequency."""
        try:
            if not word_freq:
                return self._create_empty_plot("No word frequency data available")

            words = list(word_freq.keys())
            frequencies = list(word_freq.values())

            fig = px.bar(
                x=words,
                y=frequencies,
                title='Word Frequency Distribution',
                labels={'x': 'Words', 'y': 'Frequency'},
                template='plotly_white'
            )

            fig.update_layout(
                xaxis_tickangle=-45,
                showlegend=False,
                height=400
            )

            return fig
        except Exception as e:
            print(f"Error creating word frequency plot: {e}")
            return self._create_empty_plot("Error creating word frequency visualization")

    def create_entity_distribution(self, entity_analysis: Dict):
        """Create a sunburst chart for entity distribution."""
        try:
            if not entity_analysis:
                return self._create_empty_plot("No entity data available")

            # Prepare data for sunburst chart
            labels = []
            parents = []
            values = []

            for entity_type, entities in entity_analysis.items():
                labels.append(entity_type)
                parents.append("")
                values.append(sum(count for _, count in entities))

                for entity, count in entities:
                    labels.append(entity)
                    parents.append(entity_type)
                    values.append(count)

            if not labels:
                return self._create_empty_plot("No entities found in the analysis")

            fig = go.Figure(go.Sunburst(
                labels=labels,
                parents=parents,
                values=values,
            ))

            fig.update_layout(
                title='Named Entity Distribution',
                width=600,
                height=600
            )

            return fig
        except Exception as e:
            print(f"Error creating entity distribution plot: {e}")
            return self._create_empty_plot("Error creating entity visualization")

    def create_results_overview(self, results: List[Dict]):
        """Create a scatter plot of search results."""
        try:
            if not results:
                return self._create_empty_plot("No search results available")

            titles = [r['title'][:30] + '...' if len(r['title']) > 30 else r['title'] 
                     for r in results]
            snippet_lengths = [len(r['snippet']) for r in results]

            fig = px.scatter(
                x=range(len(results)),
                y=snippet_lengths,
                text=titles,
                title='Search Results Overview',
                labels={'x': 'Result Index', 'y': 'Snippet Length'},
                template='plotly_white'
            )

            fig.update_traces(
                textposition='top center',
                marker=dict(size=10)
            )

            fig.update_layout(
                height=400,
                showlegend=False
            )

            return fig
        except Exception as e:
            print(f"Error creating results overview plot: {e}")
            return self._create_empty_plot("Error creating results visualization")

    def _create_empty_plot(self, message: str):
        """Create an empty plot with an error message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(height=400)
        return fig