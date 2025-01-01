# SkyMemo - Mood-Adaptive Weather Journaling

SkyMemo is an intelligent journaling application that generates smart, mood-adaptive prompts based on weather conditions and their psychological correlations with human emotions.

## Features

### Weather Input
- **Manual Entry**: Input temperature, weather conditions, and precipitation manually.
- **API Integration**: Optional automatic weather fetching via OpenWeatherMap API.
- **Offline Capable**: Works completely offline with manual entry.

### Smart Prompt Generation
- **Mood Detection**: Automatically correlates weather with psychological moods.
- **Mood Categories**: Reflective, energetic, calm, melancholic, hopeful, intense, cozy, balanced.
- **Dynamic Prompts**: Generates 3-5 contextual journaling prompts based on current weather.
- **NLP Templates**: Template-based system with dynamic variable substitution.

### Journal Management
- **Local Storage**: All entries stored in JSON format on your device.
- **Privacy First**: Your journal never leaves your computer.
- **Search & Filter**: Find entries by text, mood, or weather condition.
- **Word Count Tracking**: Monitor your writing volume over time.

### Trends & Insights
- **Mood Distribution**: Pie chart showing your emotional patterns.
- **Weather Timeline**: Track temperature and conditions over time.
- **Writing Activity Heatmap**: Calendar view of your journaling consistency.
- **Word Count Trends**: Visualize writing volume with moving averages.
- **Weather-Mood Correlation**: Heatmap showing relationships between weather and moods.
- **Streak Tracking**: Monitor your longest and current writing streaks.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/abhi3114-glitch/SkyMemo.git
   cd SkyMemo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **[Optional] Configure Weather API**
   
   For automatic weather fetching:
   - Get a free API key from OpenWeatherMap.
   - Copy `.env.example` to `.env`.
   - Add your API key to `.env`:
     ```
     OPENWEATHER_API_KEY=your_actual_api_key_here
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   
   The app will automatically open at `http://localhost:8501`.

## How to Use

### Creating Your First Entry

1. **Set the Weather**
   - Choose between manual entry or API fetch.
   - Manual: Enter temperature, select condition, check precipitation if applicable.
   - API: Enter your city name and click "Fetch Weather".

2. **Generate Prompts**
   - Click "Generate Prompts" to create 5 mood-based journaling prompts.
   - Each prompt is tailored to the current weather conditions.
   - Primary mood prompts are marked for visibility.

3. **Select a Prompt**
   - Browse through the generated prompts.
   - Click "Select" on the one that resonates with you.
   - View writing tips specific to that mood.

4. **Write Your Entry**
   - Let your thoughts flow in the text area.
   - Word count is tracked automatically.
   - Click "Save Entry" when finished.

### Viewing Your History

- Navigate to "Journal History" in the sidebar.
- Search entries by text content.
- Filter by mood tags.
- Sort by date or word count.
- View and delete past entries.

### Exploring Trends

- Navigate to "Trends & Insights".
- View statistics: total entries, words, streaks.
- Explore visualizations across 4 tabs:
  - **Mood Analysis**: See your emotional patterns.
  - **Weather Patterns**: Track temperature over time.
  - **Writing Activity**: View consistency heatmaps and word trends.
  - **Correlations**: Discover weather-mood relationships.

## Technical Details

### Project Structure
```
SkyMemo/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and constants
├── weather_handler.py     # Weather data processing
├── prompt_generator.py    # Intelligent prompt generation
├── journal_manager.py     # Entry CRUD operations
├── visualizer.py          # Charts and graphs
├── requirements.txt       # Python dependencies
├── .env.example          # API key template
├── data/
│   ├── entries.json      # Journal entries (created automatically)
│   └── weather_cache.json # Weather cache (created automatically)
└── README.md             # This file
```

### Weather-Mood Correlations

The application uses research-based correlations between weather and mood including:
- Sunny: Energetic, Hopeful, Calm
- Partly Cloudy: Calm, Reflective, Balanced
- Cloudy: Reflective, Calm, Introspective
- Rainy: Reflective, Melancholic, Cozy
- Stormy: Intense, Energetic, Dramatic
- Snowy: Calm, Peaceful, Quiet
- Foggy: Mysterious, Reflective, Uncertain
- Windy: Energetic, Restless, Dynamic

Temperature also influences mood selection, adding modifiers like "cozy" for cold weather or "vibrant" for warm weather.

### Data Storage

All data is stored locally in JSON format:

- **Entries**: `data/entries.json`
  - Includes timestamp, weather data, mood tags, prompt, and journal text.
  - Automatically tracks word count.
  - Preserves complete weather context.

- **Weather Cache**: `data/weather_cache.json`
  - Caches API weather data for offline use.
  - Reduces API calls.

## License

MIT License.
