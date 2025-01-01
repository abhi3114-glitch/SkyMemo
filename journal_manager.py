"""
Journal entry management system for SkyMemo.
Handles CRUD operations and data persistence.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import APP_SETTINGS


class JournalManager:
    def __init__(self):
        """Initialize journal manager."""
        self.entries_file = APP_SETTINGS['entries_file']
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data directory and entries file exist."""
        os.makedirs(os.path.dirname(self.entries_file), exist_ok=True)
        if not os.path.exists(self.entries_file):
            with open(self.entries_file, 'w') as f:
                json.dump([], f)
    
    def _load_entries(self) -> List[Dict]:
        """Load all entries from file."""
        try:
            with open(self.entries_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading entries: {e}")
            return []
    
    def _save_entries(self, entries: List[Dict]):
        """Save entries to file."""
        try:
            with open(self.entries_file, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving entries: {e}")
    
    def create_entry(self, weather_data: Dict, mood_tags: List[str], 
                    prompt: str, journal_text: str) -> Dict:
        """
        Create a new journal entry.
        
        Args:
            weather_data: Weather data dictionary
            mood_tags: List of mood tags
            prompt: Selected prompt text
            journal_text: User's journal entry
            
        Returns:
            Created entry dictionary
        """
        entry = {
            'id': datetime.now().isoformat(),
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'weather': {
                'temperature': weather_data.get('temperature'),
                'condition': weather_data.get('condition'),
                'condition_raw': weather_data.get('condition_raw'),
                'precipitation': weather_data.get('precipitation', False)
            },
            'mood_tags': mood_tags,
            'prompt': prompt,
            'text': journal_text,
            'word_count': len(journal_text.split())
        }
        
        # Load existing entries
        entries = self._load_entries()
        
        # Add new entry at the beginning
        entries.insert(0, entry)
        
        # Save updated entries
        self._save_entries(entries)
        
        return entry
    
    def get_all_entries(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get all journal entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of entry dictionaries
        """
        entries = self._load_entries()
        if limit:
            return entries[:limit]
        return entries
    
    def get_entry_by_id(self, entry_id: str) -> Optional[Dict]:
        """
        Get a specific entry by ID.
        
        Args:
            entry_id: Entry ID (timestamp)
            
        Returns:
            Entry dictionary or None
        """
        entries = self._load_entries()
        for entry in entries:
            if entry['id'] == entry_id:
                return entry
        return None
    
    def get_entries_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get entries within a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of entries within range
        """
        entries = self._load_entries()
        filtered = []
        
        for entry in entries:
            entry_date = entry.get('date', '')
            if start_date <= entry_date <= end_date:
                filtered.append(entry)
        
        return filtered
    
    def get_entries_by_mood(self, mood: str) -> List[Dict]:
        """
        Get entries with a specific mood tag.
        
        Args:
            mood: Mood tag to filter by
            
        Returns:
            List of matching entries
        """
        entries = self._load_entries()
        return [e for e in entries if mood in e.get('mood_tags', [])]
    
    def update_entry(self, entry_id: str, updated_text: str) -> bool:
        """
        Update an existing entry's text.
        
        Args:
            entry_id: Entry ID to update
            updated_text: New journal text
            
        Returns:
            True if successful, False otherwise
        """
        entries = self._load_entries()
        
        for entry in entries:
            if entry['id'] == entry_id:
                entry['text'] = updated_text
                entry['word_count'] = len(updated_text.split())
                entry['updated_at'] = datetime.now().isoformat()
                self._save_entries(entries)
                return True
        
        return False
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete an entry.
        
        Args:
            entry_id: Entry ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        entries = self._load_entries()
        original_length = len(entries)
        
        entries = [e for e in entries if e['id'] != entry_id]
        
        if len(entries) < original_length:
            self._save_entries(entries)
            return True
        
        return False
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about journal entries.
        
        Returns:
            Statistics dictionary
        """
        entries = self._load_entries()
        
        if not entries:
            return {
                'total_entries': 0,
                'total_words': 0,
                'avg_words_per_entry': 0,
                'most_common_mood': None,
                'most_common_weather': None,
                'longest_streak': 0,
                'current_streak': 0
            }
        
        # Basic stats
        total_entries = len(entries)
        total_words = sum(e.get('word_count', 0) for e in entries)
        avg_words = total_words / total_entries if total_entries > 0 else 0
        
        # Mood frequency
        mood_counts = {}
        for entry in entries:
            for mood in entry.get('mood_tags', []):
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
        most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else None
        
        # Weather frequency
        weather_counts = {}
        for entry in entries:
            condition = entry.get('weather', {}).get('condition')
            if condition:
                weather_counts[condition] = weather_counts.get(condition, 0) + 1
        most_common_weather = max(weather_counts.items(), key=lambda x: x[1])[0] if weather_counts else None
        
        # Calculate streaks
        dates = sorted(set(e.get('date') for e in entries if e.get('date')))
        longest_streak = self._calculate_longest_streak(dates)
        current_streak = self._calculate_current_streak(dates)
        
        return {
            'total_entries': total_entries,
            'total_words': total_words,
            'avg_words_per_entry': round(avg_words, 1),
            'most_common_mood': most_common_mood,
            'most_common_weather': most_common_weather,
            'longest_streak': longest_streak,
            'current_streak': current_streak,
            'mood_distribution': mood_counts,
            'weather_distribution': weather_counts
        }
    
    def _calculate_longest_streak(self, dates: List[str]) -> int:
        """Calculate the longest consecutive day streak."""
        if not dates:
            return 0
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(dates)):
            prev_date = datetime.fromisoformat(dates[i-1])
            curr_date = datetime.fromisoformat(dates[i])
            
            if (curr_date - prev_date).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak
    
    def _calculate_current_streak(self, dates: List[str]) -> int:
        """Calculate the current consecutive day streak."""
        if not dates:
            return 0
        
        today = datetime.now().date()
        streak = 0
        
        # Check from most recent date backwards
        for i, date_str in enumerate(reversed(dates)):
            date = datetime.fromisoformat(date_str).date()
            expected_date = today - timedelta(days=i)
            
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak
