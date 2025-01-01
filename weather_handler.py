"""
Weather data handling module for SkyMemo.
Supports manual weather entry and optional API integration.
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple
from config import WEATHER_KEYWORDS, TEMP_MODIFIERS, APP_SETTINGS


class WeatherHandler:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize weather handler with optional API key."""
        self.api_key = api_key
        self.cache_file = APP_SETTINGS['weather_cache_file']
        self._ensure_cache_file()
    
    def _ensure_cache_file(self):
        """Ensure the cache file exists."""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w') as f:
                json.dump({}, f)
    
    def classify_weather_condition(self, description: str) -> str:
        """
        Classify weather description into standard categories.
        
        Args:
            description: Weather description string
            
        Returns:
            Standardized weather condition
        """
        description = description.lower()
        
        # Check each category for keyword matches
        for condition, keywords in WEATHER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description:
                    return condition
        
        # Default to partly cloudy if no match
        return 'partly_cloudy'
    
    def classify_temperature(self, temp_celsius: float) -> str:
        """
        Classify temperature into descriptive categories.
        
        Args:
            temp_celsius: Temperature in Celsius
            
        Returns:
            Temperature category
        """
        for category, info in sorted(TEMP_MODIFIERS.items(), 
                                     key=lambda x: x[1]['threshold'], 
                                     reverse=True):
            if temp_celsius >= info['threshold']:
                return category
        return 'very_cold'
    
    def get_weather_manual(self, temperature: float, 
                          condition: str, 
                          precipitation: bool = False) -> Dict:
        """
        Process manually entered weather data.
        
        Args:
            temperature: Temperature in Celsius
            condition: Weather condition description
            precipitation: Whether there's rain/snow
            
        Returns:
            Standardized weather data dictionary
        """
        classified_condition = self.classify_weather_condition(condition)
        temp_category = self.classify_temperature(temperature)
        
        # Adjust condition based on precipitation
        if precipitation and classified_condition == 'cloudy':
            classified_condition = 'rainy'
        
        weather_data = {
            'temperature': temperature,
            'temperature_category': temp_category,
            'condition': classified_condition,
            'condition_raw': condition,
            'precipitation': precipitation,
            'timestamp': datetime.now().isoformat(),
            'source': 'manual'
        }
        
        return weather_data
    
    def get_weather_api(self, city: str) -> Optional[Dict]:
        """
        Fetch weather data from OpenWeatherMap API.
        
        Args:
            city: City name
            
        Returns:
            Weather data dictionary or None if failed
        """
        if not self.api_key:
            return None
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            weather_data = {
                'temperature': data['main']['temp'],
                'temperature_category': self.classify_temperature(data['main']['temp']),
                'condition': self.classify_weather_condition(data['weather'][0]['description']),
                'condition_raw': data['weather'][0]['description'],
                'precipitation': 'rain' in data['weather'][0]['description'].lower() or 
                               'snow' in data['weather'][0]['description'].lower(),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'city': city,
                'timestamp': datetime.now().isoformat(),
                'source': 'api'
            }
            
            # Cache the result
            self._cache_weather(city, weather_data)
            
            return weather_data
            
        except Exception as e:
            print(f"Error fetching weather from API: {e}")
            return self._get_cached_weather(city)
    
    def _cache_weather(self, city: str, weather_data: Dict):
        """Cache weather data for offline use."""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            cache[city] = weather_data
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Error caching weather: {e}")
    
    def _get_cached_weather(self, city: str) -> Optional[Dict]:
        """Retrieve cached weather data."""
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            return cache.get(city)
        except Exception:
            return None
    
    def get_weather_emoji(self, condition: str) -> str:
        """
        Get emoji representation for weather condition.
        
        Args:
            condition: Weather condition
            
        Returns:
            Emoji string
        """
        emoji_map = {
            'sunny': '☀️',
            'partly_cloudy': '⛅',
            'cloudy': '☁️',
            'rainy': '🌧️',
            'stormy': '⛈️',
            'snowy': '🌨️',
            'foggy': '🌫️',
            'windy': '💨'
        }
        return emoji_map.get(condition, '🌤️')
    
    def get_weather_description(self, weather_data: Dict) -> str:
        """
        Generate a natural language description of weather.
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Human-readable description
        """
        temp = weather_data['temperature']
        condition = weather_data['condition']
        emoji = self.get_weather_emoji(condition)
        
        # Temperature descriptor
        if temp < 0:
            temp_desc = "freezing"
        elif temp < 10:
            temp_desc = "cold"
        elif temp < 20:
            temp_desc = "cool"
        elif temp < 25:
            temp_desc = "pleasant"
        elif temp < 30:
            temp_desc = "warm"
        else:
            temp_desc = "hot"
        
        condition_formatted = condition.replace('_', ' ')
        
        description = f"{emoji} {temp_desc} {condition_formatted} ({temp:.1f}°C)"
        
        if weather_data.get('precipitation'):
            description += " with precipitation"
        
        return description
