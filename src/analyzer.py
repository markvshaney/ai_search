#analyzer.property
import pandas as pd
import numpy as np
from collections import Counter
from typing import List, Dict
from .text_processor import TextProcessor

class Analyzer:
    def __init__(self):
        self.text_processor = TextProcessor()

    def analyze_search_results(self, results: List[Dict]) -> Dict:
        """Analyze search results and return various metrics."""
        try:
            all_text = ' '.join([r['snippet'] for r in results])

            analysis = {
                'total_results': len(results),
                'word_frequency': self._get_word_frequency(results),
                'entity_analysis': self._analyze_entities(results),
                'summary': self._generate_summary(all_text)
            }
            return analysis
        except Exception as e:
            print(f"Error in analysis: {e}")
            return {
                'total_results': 0,
                'word_frequency': {},
                'entity_analysis': {},
                'summary': "Analysis unavailable"
            }

    def _get_word_frequency(self, results: List[Dict]) -> Dict:
        """Calculate word frequency across all results."""
        try:
            all_text = ' '.join([r['snippet'] for r in results])
            tokens = self.text_processor.preprocess_text(all_text)
            # Ensure we have at least some tokens
            if not tokens:
                return {}
            return dict(Counter(tokens).most_common(20))
        except Exception as e:
            print(f"Error in word frequency analysis: {e}")
            return {}

    def _analyze_entities(self, results: List[Dict]) -> Dict:
        """Analyze named entities in the search results."""
        try:
            all_text = ' '.join([r['snippet'] for r in results])
            entities = self.text_processor.extract_entities(all_text)

            entity_types = {}
            for entity, ent_type in entities:
                if ent_type not in entity_types:
                    entity_types[ent_type] = []
                entity_types[ent_type].append(entity)

            # Get top 5 entities for each type
            for ent_type in entity_types:
                entity_types[ent_type] = Counter(entity_types[ent_type]).most_common(5)

            return entity_types
        except Exception as e:
            print(f"Error in entity analysis: {e}")
            return {}

    def _generate_summary(self, text: str) -> str:
        """Generate a summary of the search results."""
        try:
            return self.text_processor.get_summary(text)
        except Exception as e:
            print(f"Error in summary generation: {e}")
            return "Summary unavailable"

    def generate_report(self, query: str, results: List[Dict], analysis: Dict) -> pd.DataFrame:
        """Generate a structured report from the analysis results."""
        try:
            report_data = []

            # Add basic statistics
            report_data.append({
                'Metric': 'Total Results',
                'Value': analysis['total_results']
            })

            # Add top words
            for word, count in analysis.get('word_frequency', {}).items():
                report_data.append({
                    'Metric': f'Word Frequency: {word}',
                    'Value': count
                })

            # Add entity information
            for entity_type, entities in analysis.get('entity_analysis', {}).items():
                for entity, count in entities:
                    report_data.append({
                        'Metric': f'Entity ({entity_type})',
                        'Value': f'{entity} ({count})'
                    })

            return pd.DataFrame(report_data)
        except Exception as e:
            print(f"Error in report generation: {e}")
            return pd.DataFrame(columns=['Metric', 'Value'])