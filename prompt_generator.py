"""
Intelligent prompt generation system for SkyMemo.
Generates mood-adaptive journaling prompts based on weather conditions.
"""

import random
from typing import List, Dict, Tuple
from config import WEATHER_MOOD_MAP, TEMP_MODIFIERS, PROMPT_TEMPLATES


class PromptGenerator:
    def __init__(self):
        """Initialize the prompt generator."""
        self.mood_map = WEATHER_MOOD_MAP
        self.temp_modifiers = TEMP_MODIFIERS
        self.templates = PROMPT_TEMPLATES
    
    def determine_moods(self, weather_data: Dict) -> Tuple[str, List[str]]:
        """
        Determine primary and secondary moods based on weather.
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Tuple of (primary_mood, list of secondary_moods)
        """
        condition = weather_data.get('condition', 'partly_cloudy')
        temp_category = weather_data.get('temperature_category', 'mild')
        
        # Get base moods from weather condition
        mood_info = self.mood_map.get(condition, self.mood_map['partly_cloudy'])
        primary_mood = mood_info['primary_mood']
        secondary_moods = mood_info['secondary_moods'].copy()
        
        # Add temperature-influenced moods
        temp_info = self.temp_modifiers.get(temp_category, {})
        temp_moods = temp_info.get('moods', [])
        
        # Merge temperature moods with secondary moods
        for mood in temp_moods:
            if mood not in secondary_moods and mood != primary_mood:
                secondary_moods.append(mood)
        
        return primary_mood, secondary_moods
    
    def generate_prompts(self, weather_data: Dict, num_prompts: int = 5) -> List[Dict]:
        """
        Generate journaling prompts based on weather conditions.
        
        Args:
            weather_data: Weather data dictionary
            num_prompts: Number of prompts to generate (default 5)
            
        Returns:
            List of prompt dictionaries with mood and text
        """
        condition = weather_data.get('condition', 'partly_cloudy')
        condition_raw = weather_data.get('condition_raw', condition)
        
        # Get weather description
        mood_info = self.mood_map.get(condition, self.mood_map['partly_cloudy'])
        weather_desc = mood_info['description']
        
        # Determine moods
        primary_mood, secondary_moods = self.determine_moods(weather_data)
        
        # Collect all relevant moods
        all_moods = [primary_mood] + secondary_moods
        
        prompts = []
        used_templates = set()
        
        # Generate prompts from different mood categories
        for mood in all_moods:
            if len(prompts) >= num_prompts:
                break
            
            if mood not in self.templates:
                continue
            
            # Get templates for this mood
            mood_templates = self.templates[mood]
            
            # Filter out already used templates
            available_templates = [t for t in mood_templates if t not in used_templates]
            
            if not available_templates:
                continue
            
            # Select a random template
            template = random.choice(available_templates)
            used_templates.add(template)
            
            # Fill in the template with weather info
            prompt_text = template.format(
                weather_desc=weather_desc,
                weather_condition=condition.replace('_', ' ')
            )
            
            prompts.append({
                'mood': mood,
                'text': prompt_text,
                'is_primary': mood == primary_mood
            })
        
        # If we don't have enough prompts, add more from primary mood
        while len(prompts) < num_prompts and primary_mood in self.templates:
            available = [t for t in self.templates[primary_mood] if t not in used_templates]
            if not available:
                break
            
            template = random.choice(available)
            used_templates.add(template)
            
            prompt_text = template.format(
                weather_desc=weather_desc,
                weather_condition=condition.replace('_', ' ')
            )
            
            prompts.append({
                'mood': primary_mood,
                'text': prompt_text,
                'is_primary': True
            })
        
        # Shuffle to mix moods
        random.shuffle(prompts)
        
        return prompts
    
    def get_mood_description(self, mood: str) -> str:
        """
        Get a description of what a mood represents.
        
        Args:
            mood: Mood tag
            
        Returns:
            Description string
        """
        descriptions = {
            'reflective': 'Deep thinking, contemplation, looking inward',
            'energetic': 'Active, motivated, full of possibilities',
            'calm': 'Peaceful, centered, tranquil',
            'melancholic': 'Processing sadness, gentle grief, introspection',
            'hopeful': 'Optimistic, forward-looking, expecting positive change',
            'intense': 'Strong emotions, passion, powerful feelings',
            'cozy': 'Comfortable, warm, seeking comfort and safety',
            'balanced': 'Harmonious, stable, equilibrium',
            'peaceful': 'Serene, quiet, undisturbed',
            'mysterious': 'Unclear, questioning, exploring the unknown',
            'introspective': 'Self-examining, thoughtful, analytical',
            'dynamic': 'Changing, active, in motion',
            'crisp': 'Clear-minded, alert, focused',
            'vibrant': 'Full of energy, colorful, lively'
        }
        return descriptions.get(mood, 'A unique emotional state')
    
    def suggest_writing_style(self, mood: str) -> str:
        """
        Suggest a writing style based on mood.
        
        Args:
            mood: Mood tag
            
        Returns:
            Writing style suggestion
        """
        styles = {
            'reflective': 'Take your time. Write slowly and thoughtfully.',
            'energetic': 'Let your thoughts flow freely. Write with excitement!',
            'calm': 'Breathe and write gently. No rush.',
            'melancholic': 'Be kind to yourself. Write without judgment.',
            'hopeful': 'Dream on paper. Write about possibilities.',
            'intense': 'Don\'t hold back. Express what you truly feel.',
            'cozy': 'Get comfortable. Write as if talking to a friend.',
            'balanced': 'Find your rhythm. Write with steady awareness.'
        }
        return styles.get(mood, 'Write authentically from your current state.')
