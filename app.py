"""
SkyMemo - Mood-Adaptive Weather Journaling
Main Streamlit Application
"""

import streamlit as st
from datetime import datetime
import os

# Import modules
from weather_handler import WeatherHandler
from prompt_generator import PromptGenerator
from journal_manager import JournalManager
from visualizer import Visualizer
from config import APP_SETTINGS, MOOD_COLORS

# Page configuration
st.set_page_config(
    page_title="SkyMemo",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'weather_handler' not in st.session_state:
    api_key = os.getenv('OPENWEATHER_API_KEY')
    st.session_state.weather_handler = WeatherHandler(api_key)

if 'prompt_generator' not in st.session_state:
    st.session_state.prompt_generator = PromptGenerator()

if 'journal_manager' not in st.session_state:
    st.session_state.journal_manager = JournalManager()

if 'visualizer' not in st.session_state:
    st.session_state.visualizer = Visualizer()

if 'current_weather' not in st.session_state:
    st.session_state.current_weather = None

if 'current_prompts' not in st.session_state:
    st.session_state.current_prompts = []

if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None


def main():
    """Main application function."""
    
    # Sidebar navigation
    st.sidebar.title("🌤️ SkyMemo")
    st.sidebar.markdown(f"*{APP_SETTINGS['tagline']}*")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigate",
        ["📝 New Entry", "📚 Journal History", "📊 Trends & Insights", "⚙️ Settings"]
    )
    
    # Display statistics in sidebar
    stats = st.session_state.journal_manager.get_statistics()
    st.sidebar.markdown("### 📈 Your Stats")
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Total Entries", stats['total_entries'])
    col2.metric("Current Streak", f"{stats['current_streak']} days")
    
    if stats['total_entries'] > 0:
        st.sidebar.metric("Avg Words/Entry", stats['avg_words_per_entry'])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("*Your journal data is stored locally and never leaves your device.*")
    
    # Page routing
    if page == "📝 New Entry":
        page_new_entry()
    elif page == "📚 Journal History":
        page_journal_history()
    elif page == "📊 Trends & Insights":
        page_trends()
    elif page == "⚙️ Settings":
        page_settings()


def page_new_entry():
    """Page for creating a new journal entry."""
    st.title("📝 New Journal Entry")
    st.markdown("---")
    
    # Weather input section
    st.header("1️⃣ Today's Weather")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        weather_mode = st.radio(
            "How would you like to input weather?",
            ["Manual Entry", "Fetch from API (Optional)"],
            horizontal=True
        )
    
    weather_data = None
    
    if weather_mode == "Manual Entry":
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-50.0,
                max_value=60.0,
                value=20.0,
                step=0.5
            )
        
        with col_b:
            condition = st.selectbox(
                "Weather Condition",
                ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy", 
                 "Snowy", "Foggy", "Windy"]
            )
        
        with col_c:
            precipitation = st.checkbox("Precipitation?", value=False)
        
        if st.button("🌡️ Set Weather", type="primary"):
            weather_data = st.session_state.weather_handler.get_weather_manual(
                temperature, condition.lower().replace(' ', '_'), precipitation
            )
            st.session_state.current_weather = weather_data
            st.success("✅ Weather recorded!")
    
    else:
        city = st.text_input("City Name", value=APP_SETTINGS['default_city'])
        
        if st.button("🌍 Fetch Weather", type="primary"):
            with st.spinner("Fetching weather data..."):
                weather_data = st.session_state.weather_handler.get_weather_api(city)
                
                if weather_data:
                    st.session_state.current_weather = weather_data
                    st.success(f"✅ Weather data fetched for {city}!")
                else:
                    st.error("❌ Could not fetch weather. Please check your API key or use manual entry.")
    
    # Display current weather
    if st.session_state.current_weather:
        st.markdown("### Current Weather")
        weather_desc = st.session_state.weather_handler.get_weather_description(
            st.session_state.current_weather
        )
        st.info(weather_desc)
    
    st.markdown("---")
    
    # Prompt generation section
    st.header("2️⃣ Choose a Journaling Prompt")
    
    if not st.session_state.current_weather:
        st.warning("⚠️ Please set the weather first to generate prompts.")
    else:
        if st.button("✨ Generate Prompts", type="primary") or not st.session_state.current_prompts:
            prompts = st.session_state.prompt_generator.generate_prompts(
                st.session_state.current_weather,
                num_prompts=5
            )
            st.session_state.current_prompts = prompts
        
        # Display prompts
        if st.session_state.current_prompts:
            for i, prompt_data in enumerate(st.session_state.current_prompts):
                mood = prompt_data['mood']
                prompt_text = prompt_data['text']
                is_primary = prompt_data['is_primary']
                
                # Get mood color
                color = MOOD_COLORS.get(mood, '#CCCCCC')
                
                # Create prompt card
                with st.container():
                    cols = st.columns([1, 20, 2])
                    
                    with cols[0]:
                        st.markdown(f"<div style='width:5px;height:80px;background:{color};border-radius:3px;'></div>", 
                                  unsafe_allow_html=True)
                    
                    with cols[1]:
                        badge = "⭐ Recommended" if is_primary else ""
                        st.markdown(f"**{mood.replace('_', ' ').title()}** {badge}")
                        st.markdown(f"*{prompt_text}*")
                        
                        # Writing style tip
                        tip = st.session_state.prompt_generator.suggest_writing_style(mood)
                        with st.expander("💡 Writing tip"):
                            st.write(tip)
                    
                    with cols[2]:
                        if st.button("Select", key=f"prompt_{i}"):
                            st.session_state.selected_prompt = {
                                'mood': mood,
                                'text': prompt_text
                            }
                            st.rerun()
                
                st.markdown("")  # Spacing
        
        if st.session_state.selected_prompt:
            st.success(f"✅ Selected: *{st.session_state.selected_prompt['text']}*")
    
    st.markdown("---")
    
    # Journal entry section
    st.header("3️⃣ Write Your Entry")
    
    if not st.session_state.selected_prompt:
        st.warning("⚠️ Please select a prompt above to begin writing.")
    else:
        mood = st.session_state.selected_prompt['mood']
        color = MOOD_COLORS.get(mood, '#CCCCCC')
        
        st.markdown(
            f"<div style='padding:15px;border-left:5px solid {color};background:#f0f2f6;border-radius:5px;margin-bottom:20px;'>"
            f"<strong>Prompt:</strong> <em>{st.session_state.selected_prompt['text']}</em>"
            f"</div>",
            unsafe_allow_html=True
        )
        
        journal_text = st.text_area(
            "Your thoughts...",
            height=300,
            placeholder="Let your thoughts flow freely...",
            key="journal_textarea"
        )
        
        # Word count
        word_count = len(journal_text.split()) if journal_text.strip() else 0
        st.caption(f"Words: {word_count}")
        
        # Save button
        if st.button("💾 Save Entry", type="primary", disabled=not journal_text.strip()):
            # Determine all mood tags
            primary_mood, secondary_moods = st.session_state.prompt_generator.determine_moods(
                st.session_state.current_weather
            )
            mood_tags = [primary_mood] + secondary_moods[:2]  # Include top 3 moods
            
            # Create entry
            entry = st.session_state.journal_manager.create_entry(
                weather_data=st.session_state.current_weather,
                mood_tags=mood_tags,
                prompt=st.session_state.selected_prompt['text'],
                journal_text=journal_text
            )
            
            st.success("🎉 Entry saved successfully!")
            st.balloons()
            
            # Reset state
            st.session_state.current_weather = None
            st.session_state.current_prompts = []
            st.session_state.selected_prompt = None
            
            # Show entry preview
            with st.expander("📄 View saved entry"):
                st.markdown(f"**Date:** {entry['date']}")
                st.markdown(f"**Mood:** {', '.join(mood_tags)}")
                st.markdown(f"**Weather:** {entry['weather']['condition_raw']}")
                st.markdown(f"**Entry:** {entry['text'][:200]}...")


def page_journal_history():
    """Page for viewing journal history."""
    st.title("📚 Journal History")
    st.markdown("---")
    
    entries = st.session_state.journal_manager.get_all_entries(
        limit=APP_SETTINGS['max_entries_display']
    )
    
    if not entries:
        st.info("📝 No journal entries yet. Start writing to see your history!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_text = st.text_input("🔍 Search entries", "")
    
    with col2:
        filter_mood = st.multiselect(
            "Filter by mood",
            options=list(MOOD_COLORS.keys())
        )
    
    with col3:
        sort_order = st.selectbox(
            "Sort by",
            ["Newest First", "Oldest First", "Most Words"]
        )
    
    # Apply filters
    filtered_entries = entries
    
    if search_text:
        filtered_entries = [
            e for e in filtered_entries 
            if search_text.lower() in e['text'].lower()
        ]
    
    if filter_mood:
        filtered_entries = [
            e for e in filtered_entries
            if any(mood in e.get('mood_tags', []) for mood in filter_mood)
        ]
    
    # Apply sorting
    if sort_order == "Oldest First":
        filtered_entries = list(reversed(filtered_entries))
    elif sort_order == "Most Words":
        filtered_entries = sorted(filtered_entries, 
                                 key=lambda x: x.get('word_count', 0), 
                                 reverse=True)
    
    st.markdown(f"### Showing {len(filtered_entries)} entries")
    st.markdown("")
    
    # Display entries
    for entry in filtered_entries:
        with st.expander(
            f"📅 {entry['date']} - {entry['weather']['condition'].replace('_', ' ').title()} "
            f"({entry['word_count']} words)"
        ):
            # Mood tags
            mood_badges = " ".join([
                f"<span style='background:{MOOD_COLORS.get(m, '#CCC')};color:white;padding:3px 8px;border-radius:12px;font-size:12px;margin-right:5px;'>{m}</span>"
                for m in entry.get('mood_tags', [])
            ])
            st.markdown(mood_badges, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Weather info
            weather_emoji = st.session_state.weather_handler.get_weather_emoji(
                entry['weather']['condition']
            )
            st.markdown(
                f"**Weather:** {weather_emoji} {entry['weather']['condition_raw']} "
                f"({entry['weather']['temperature']:.1f}°C)"
            )
            
            # Prompt
            st.markdown(f"**Prompt:** *{entry['prompt']}*")
            
            st.markdown("---")
            
            # Entry text
            st.markdown(entry['text'])
            
            # Actions
            col_a, col_b = st.columns([1, 5])
            with col_a:
                if st.button("🗑️ Delete", key=f"del_{entry['id']}"):
                    if st.session_state.journal_manager.delete_entry(entry['id']):
                        st.success("Entry deleted!")
                        st.rerun()


def page_trends():
    """Page for viewing trends and insights."""
    st.title("📊 Trends & Insights")
    st.markdown("---")
    
    entries = st.session_state.journal_manager.get_all_entries()
    
    if not entries:
        st.info("📝 No data yet. Create some journal entries to see your trends!")
        return
    
    stats = st.session_state.journal_manager.get_statistics()
    
    # Statistics overview
    st.header("📈 Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Entries", stats['total_entries'])
    col2.metric("Total Words", f"{stats['total_words']:,}")
    col3.metric("Longest Streak", f"{stats['longest_streak']} days")
    col4.metric("Current Streak", f"{stats['current_streak']} days")
    
    st.markdown("---")
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎭 Mood Analysis",
        "🌡️ Weather Patterns",
        "📝 Writing Activity",
        "🔗 Correlations"
    ])
    
    with tab1:
        st.subheader("Mood Distribution")
        fig = st.session_state.visualizer.create_mood_distribution_chart(entries)
        st.plotly_chart(fig, use_container_width=True)
        
        if stats['most_common_mood']:
            st.info(f"💡 Your most common mood is **{stats['most_common_mood']}**")
    
    with tab2:
        st.subheader("Temperature Over Time")
        fig = st.session_state.visualizer.create_weather_timeline(entries)
        st.plotly_chart(fig, use_container_width=True)
        
        if stats['most_common_weather']:
            weather_name = stats['most_common_weather'].replace('_', ' ').title()
            st.info(f"🌤️ You most often journal during **{weather_name}** weather")
    
    with tab3:
        st.subheader("Writing Activity Heatmap")
        fig = st.session_state.visualizer.create_writing_activity_heatmap(entries, days=30)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Word Count Trend")
        fig = st.session_state.visualizer.create_word_count_trend(entries)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Weather-Mood Correlation")
        fig = st.session_state.visualizer.create_weather_mood_correlation(entries)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 This heatmap shows how often you experience different moods in various weather conditions")


def page_settings():
    """Settings and about page."""
    st.title("⚙️ Settings")
    st.markdown("---")
    
    st.header("🔑 API Configuration (Optional)")
    st.markdown(
        "To enable automatic weather fetching, you need a free API key from "
        "[OpenWeatherMap](https://openweathermap.org/api)."
    )
    
    current_key = os.getenv('OPENWEATHER_API_KEY', '')
    
    if current_key:
        st.success("✅ API key is configured")
    else:
        st.warning("⚠️ No API key found. Using manual entry only.")
    
    st.markdown("To set your API key, create a `.env` file in the project directory with:")
    st.code("OPENWEATHER_API_KEY=your_api_key_here")
    
    st.markdown("---")
    
    st.header("📊 Data Management")
    
    stats = st.session_state.journal_manager.get_statistics()
    
    st.markdown(f"**Storage location:** `{APP_SETTINGS['entries_file']}`")
    st.markdown(f"**Total entries:** {stats['total_entries']}")
    st.markdown(f"**Total words written:** {stats['total_words']:,}")
    
    st.markdown("---")
    
    st.header("ℹ️ About SkyMemo")
    st.markdown(
        """
        **SkyMemo** is a mood-adaptive weather journaling application that generates 
        intelligent prompts based on current weather conditions and their psychological 
        correlations with human moods.
        
        ### Features
        - 🌤️ **Weather Input**: Manual or API-based weather entry
        - 🎭 **Smart Prompts**: AI-generated prompts tailored to weather and mood
        - 📝 **Local Journaling**: All data stored securely on your device
        - 📊 **Insights**: Visualize patterns in your writing and mood
        - 🔒 **Privacy First**: Your journal never leaves your computer
        
        ### Technology
        - Built with Python 3.11
        - Powered by Streamlit
        - Offline-capable
        - No account required
        
        ---
        
        Made with ❤️ for mindful reflection
        """
    )


if __name__ == "__main__":
    main()
