"""
Visualization module for SkyMemo.
Creates charts and graphs for journal trends and weather patterns.
"""

import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from config import MOOD_COLORS


class Visualizer:
    def __init__(self):
        """Initialize the visualizer."""
        self.mood_colors = MOOD_COLORS
    
    def create_mood_distribution_chart(self, entries: List[Dict]) -> go.Figure:
        """
        Create a pie chart showing mood tag distribution.
        
        Args:
            entries: List of journal entries
            
        Returns:
            Plotly figure
        """
        mood_counts = {}
        for entry in entries:
            for mood in entry.get('mood_tags', []):
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        if not mood_counts:
            # Empty chart
            fig = go.Figure()
            fig.add_annotation(
                text="No entries yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="gray")
            )
            return fig
        
        moods = list(mood_counts.keys())
        counts = list(mood_counts.values())
        colors = [self.mood_colors.get(m, '#CCCCCC') for m in moods]
        
        fig = go.Figure(data=[go.Pie(
            labels=moods,
            values=counts,
            marker=dict(colors=colors),
            hole=0.3,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Mood Distribution",
            showlegend=True,
            height=400
        )
        
        return fig
    
    def create_weather_timeline(self, entries: List[Dict]) -> go.Figure:
        """
        Create a timeline of temperature and weather conditions.
        
        Args:
            entries: List of journal entries
            
        Returns:
            Plotly figure
        """
        if not entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No entries yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="gray")
            )
            return fig
        
        # Sort entries by date
        sorted_entries = sorted(entries, key=lambda x: x.get('timestamp', ''))
        
        dates = [e.get('date', '') for e in sorted_entries]
        temps = [e.get('weather', {}).get('temperature', 0) for e in sorted_entries]
        conditions = [e.get('weather', {}).get('condition', 'unknown') for e in sorted_entries]
        
        fig = go.Figure()
        
        # Add temperature line
        fig.add_trace(go.Scatter(
            x=dates,
            y=temps,
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Temperature: %{y}°C<extra></extra>'
        ))
        
        fig.update_layout(
            title="Temperature Trend",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_writing_activity_heatmap(self, entries: List[Dict], days: int = 30) -> go.Figure:
        """
        Create a calendar heatmap of writing activity.
        
        Args:
            entries: List of journal entries
            days: Number of days to show
            
        Returns:
            Plotly figure
        """
        # Create date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Count entries per date
        date_counts = {}
        for entry in entries:
            entry_date = entry.get('date', '')
            if entry_date:
                date_counts[entry_date] = date_counts.get(entry_date, 0) + 1
        
        # Create data for heatmap
        dates = []
        counts = []
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            dates.append(date_str)
            counts.append(date_counts.get(date_str, 0))
            current_date += timedelta(days=1)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            x=dates,
            y=['Entries'],
            z=[counts],
            colorscale='Greens',
            showscale=True,
            hovertemplate='<b>%{x}</b><br>Entries: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Writing Activity (Last {days} Days)",
            xaxis_title="Date",
            yaxis_title="",
            height=200,
            xaxis=dict(tickangle=-45)
        )
        
        return fig
    
    def create_word_count_trend(self, entries: List[Dict]) -> go.Figure:
        """
        Create a chart showing word count trends.
        
        Args:
            entries: List of journal entries
            
        Returns:
            Plotly figure
        """
        if not entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No entries yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="gray")
            )
            return fig
        
        sorted_entries = sorted(entries, key=lambda x: x.get('timestamp', ''))
        
        dates = [e.get('date', '') for e in sorted_entries]
        word_counts = [e.get('word_count', 0) for e in sorted_entries]
        
        # Calculate moving average
        window_size = min(7, len(word_counts))
        moving_avg = []
        for i in range(len(word_counts)):
            start_idx = max(0, i - window_size + 1)
            avg = sum(word_counts[start_idx:i+1]) / (i - start_idx + 1)
            moving_avg.append(avg)
        
        fig = go.Figure()
        
        # Add actual word counts
        fig.add_trace(go.Bar(
            x=dates,
            y=word_counts,
            name='Word Count',
            marker_color='#4ECDC4',
            opacity=0.6,
            hovertemplate='<b>%{x}</b><br>Words: %{y}<extra></extra>'
        ))
        
        # Add moving average line
        if len(moving_avg) > 1:
            fig.add_trace(go.Scatter(
                x=dates,
                y=moving_avg,
                name='Average Trend',
                line=dict(color='#FF6B6B', width=3),
                mode='lines',
                hovertemplate='<b>%{x}</b><br>Avg: %{y:.1f} words<extra></extra>'
            ))
        
        fig.update_layout(
            title="Word Count Trend",
            xaxis_title="Date",
            yaxis_title="Words",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_weather_mood_correlation(self, entries: List[Dict]) -> go.Figure:
        """
        Create a chart showing correlation between weather and moods.
        
        Args:
            entries: List of journal entries
            
        Returns:
            Plotly figure
        """
        if not entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No entries yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="gray")
            )
            return fig
        
        # Build correlation matrix
        weather_mood_pairs = {}
        
        for entry in entries:
            weather = entry.get('weather', {}).get('condition', 'unknown')
            for mood in entry.get('mood_tags', []):
                key = f"{weather}_{mood}"
                weather_mood_pairs[key] = weather_mood_pairs.get(key, 0) + 1
        
        # Prepare data for heatmap
        weathers = sorted(set(e.get('weather', {}).get('condition', '') for e in entries if e.get('weather', {}).get('condition')))
        all_moods = set()
        for e in entries:
            all_moods.update(e.get('mood_tags', []))
        moods = sorted(all_moods)
        
        # Create matrix
        matrix = []
        for weather in weathers:
            row = []
            for mood in moods:
                count = weather_mood_pairs.get(f"{weather}_{mood}", 0)
                row.append(count)
            matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            x=moods,
            y=[w.replace('_', ' ').title() for w in weathers],
            z=matrix,
            colorscale='Viridis',
            hovertemplate='<b>%{y}</b> + <b>%{x}</b><br>Count: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Weather-Mood Correlation",
            xaxis_title="Mood Tags",
            yaxis_title="Weather Conditions",
            height=400
        )
        
        return fig
