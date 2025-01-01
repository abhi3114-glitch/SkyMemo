"""
Configuration file for SkyMemo application.
Contains mood correlations, prompt templates, and app settings.
"""

# Weather to mood correlation mappings
WEATHER_MOOD_MAP = {
    'sunny': {
        'primary_mood': 'energetic',
        'secondary_moods': ['hopeful', 'calm'],
        'description': 'bright and uplifting'
    },
    'partly_cloudy': {
        'primary_mood': 'calm',
        'secondary_moods': ['reflective', 'balanced'],
        'description': 'mixed and transitional'
    },
    'cloudy': {
        'primary_mood': 'reflective',
        'secondary_moods': ['calm', 'introspective'],
        'description': 'contemplative and soft'
    },
    'rainy': {
        'primary_mood': 'reflective',
        'secondary_moods': ['melancholic', 'cozy'],
        'description': 'introspective and cozy'
    },
    'stormy': {
        'primary_mood': 'intense',
        'secondary_moods': ['energetic', 'dramatic'],
        'description': 'powerful and dramatic'
    },
    'snowy': {
        'primary_mood': 'calm',
        'secondary_moods': ['peaceful', 'quiet'],
        'description': 'serene and hushed'
    },
    'foggy': {
        'primary_mood': 'mysterious',
        'secondary_moods': ['reflective', 'uncertain'],
        'description': 'unclear and mysterious'
    },
    'windy': {
        'primary_mood': 'energetic',
        'secondary_moods': ['restless', 'dynamic'],
        'description': 'dynamic and changeable'
    }
}

# Temperature-based mood modifiers
TEMP_MODIFIERS = {
    'very_cold': {'threshold': 0, 'moods': ['cozy', 'introspective']},
    'cold': {'threshold': 10, 'moods': ['crisp', 'alert']},
    'cool': {'threshold': 15, 'moods': ['comfortable', 'balanced']},
    'mild': {'threshold': 20, 'moods': ['pleasant', 'calm']},
    'warm': {'threshold': 25, 'moods': ['energetic', 'vibrant']},
    'hot': {'threshold': 30, 'moods': ['lazy', 'relaxed']},
    'very_hot': {'threshold': 35, 'moods': ['sluggish', 'seeking_rest']}
}

# Journaling prompt templates
PROMPT_TEMPLATES = {
    'reflective': [
        "Today's {weather_desc} weather invites reflection. What emotions are sitting with you right now?",
        "The {weather_condition} outside mirrors inner contemplation. What thoughts have been recurring lately?",
        "In this {weather_desc} moment, what aspects of your life deserve deeper attention?",
        "How does today's {weather_condition} weather influence your perspective on recent events?",
        "What would you tell your past self about handling days like this {weather_desc} one?"
    ],
    'energetic': [
        "The {weather_desc} weather sparks energy! What goals are you excited to pursue?",
        "This {weather_condition} day feels full of possibility. What would you do if you couldn't fail?",
        "With {weather_desc} conditions outside, what adventure or project calls to you?",
        "The vibrant {weather_condition} weather energizes action. What's one thing you'll accomplish today?",
        "This {weather_desc} energy is contagious. What brings you alive right now?"
    ],
    'calm': [
        "The {weather_desc} atmosphere invites peace. What are you grateful for today?",
        "In this {weather_condition} stillness, what simple pleasures brought you joy?",
        "Today's {weather_desc} weather suggests rest. How can you be kinder to yourself?",
        "The gentle {weather_condition} conditions create space for calm. What does your body need right now?",
        "This {weather_desc} moment is perfect for appreciation. What went well today?"
    ],
    'melancholic': [
        "The {weather_desc} weather holds space for sadness. What loss or change are you processing?",
        "This {weather_condition} day allows for gentle grief. What do you need to let go of?",
        "In {weather_desc} weather like this, what memories surface for you?",
        "The {weather_condition} atmosphere validates difficult feelings. What hurts right now?",
        "This {weather_desc} backdrop supports healing. What wisdom has pain taught you?"
    ],
    'hopeful': [
        "Today's {weather_desc} weather whispers possibility. What new beginning excites you?",
        "The {weather_condition} conditions feel like a fresh start. What are you hopeful about?",
        "This {weather_desc} day suggests transformation. What positive change do you sense coming?",
        "With {weather_condition} weather like this, what dream feels closer to reality?",
        "The {weather_desc} atmosphere nurtures hope. What future version of yourself can you envision?"
    ],
    'intense': [
        "Today's {weather_desc} weather matches inner intensity. What strong emotions need expression?",
        "The {weather_condition} conditions mirror passion. What are you fired up about?",
        "This {weather_desc} energy demands attention. What truth needs to be spoken?",
        "The powerful {weather_condition} weather reflects big feelings. What's demanding to be felt?",
        "In this {weather_desc} intensity, what bold action is calling you?"
    ],
    'cozy': [
        "The {weather_desc} weather invites coziness. What comforts are you savoring today?",
        "This {weather_condition} day is perfect for nesting. What makes you feel safe and warm?",
        "Today's {weather_desc} conditions suggest hygge. What small pleasures warmed your heart?",
        "The {weather_condition} weather creates a cocoon. What are you protecting or nurturing?",
        "This {weather_desc} atmosphere invites softness. How can you pamper yourself today?"
    ],
    'balanced': [
        "Today's {weather_desc} weather suggests equilibrium. What feels in harmony right now?",
        "The {weather_condition} conditions mirror balance. Where are you finding your center?",
        "This {weather_desc} day invites moderation. What needs right-sizing in your life?",
        "The steady {weather_condition} weather reflects stability. What foundations are you building?",
        "In this {weather_desc} balance, what opposing forces are you integrating?"
    ]
}

# Weather condition keywords for classification
WEATHER_KEYWORDS = {
    'sunny': ['sun', 'sunny', 'clear', 'bright'],
    'partly_cloudy': ['partly cloudy', 'partly sunny', 'scattered clouds'],
    'cloudy': ['cloudy', 'overcast', 'grey', 'gray'],
    'rainy': ['rain', 'rainy', 'drizzle', 'shower', 'precipitation'],
    'stormy': ['storm', 'thunder', 'lightning', 'severe'],
    'snowy': ['snow', 'snowy', 'flurries', 'blizzard'],
    'foggy': ['fog', 'foggy', 'mist', 'misty', 'haze'],
    'windy': ['wind', 'windy', 'breezy', 'gusty']
}

# Application settings
APP_SETTINGS = {
    'app_name': 'SkyMemo',
    'tagline': 'Mood-Adaptive Weather Journaling',
    'data_dir': 'data',
    'entries_file': 'data/entries.json',
    'weather_cache_file': 'data/weather_cache.json',
    'max_entries_display': 50,
    'default_city': 'London',
    'temperature_unit': 'celsius'  # or 'fahrenheit'
}

# Mood color scheme for visualization
MOOD_COLORS = {
    'reflective': '#6B7FD7',      # Soft blue
    'energetic': '#F59E42',       # Vibrant orange
    'calm': '#7BC8A4',            # Gentle green
    'melancholic': '#8E9AAF',     # Muted purple-gray
    'hopeful': '#FFD93D',         # Warm yellow
    'intense': '#E63946',         # Bold red
    'cozy': '#D4A574',            # Warm brown
    'balanced': '#4ECDC4',        # Teal
    'peaceful': '#A8DADC',        # Light blue
    'mysterious': '#52489C'       # Deep purple
}
