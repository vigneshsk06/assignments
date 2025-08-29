"""
🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics
Main Streamlit application with multi-page navigation and real data integration
"""

import streamlit as st
import os
import sys
from pathlib import Path
import pandas as pd

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import utilities and pages
from utils.db_connection import DatabaseConnection
from utils.api_client import CricbuzzAPI

# Page configuration
st.set_page_config(
    page_title="🏏 Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and visibility
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #444;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        color: #333;
    }
    .sidebar-info {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #333;
    }
    
    /* Fix text visibility issues */
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        color: #333333 !important;
        border: 1px solid #ddd;
    }
    
    .stSelectbox label {
        color: #333333 !important;
    }
    
    .stTextInput > div > div > input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    
    .stNumberInput > div > div > input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    
    .stButton > button {
        color: #333333;
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    
    .stButton > button:hover {
        background-color: #f0f2f6;
        border-color: #1f77b4;
    }
    
    /* Fix form styling */
    .stForm {
        color: #333333;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 10px;
        background-color: #fafafa;
    }
    
    /* Ensure all text is visible */
    div[data-testid="stMarkdownContainer"] {
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = DatabaseConnection()
    
    if 'api_client' not in st.session_state:
        st.session_state.api_client = CricbuzzAPI()

def show_sidebar():
    """Display sidebar navigation and information"""
    with st.sidebar:
        st.markdown("## 🏏 Navigation")
        
        # Page selection
        pages = {
            "🏠 Home": "home",
            "📊 Live Matches": "live_matches",
            "⭐ Player Stats": "player_stats", 
            "🔍 SQL Analytics": "sql_analytics",
            "⚙️ CRUD Operations": "crud_operations"
        }
        
        selected_page = st.selectbox(
            "Select Page",
            options=list(pages.keys()),
            key="page_selector"
        )
        
        st.markdown("---")
        
        # Project information
        with st.container():
            st.markdown("""
            <div class="sidebar-info">
            <h4>📋 Project Info</h4>
            <p><strong>Domain:</strong> Sports Analytics</p>
            <p><strong>Submitted by : Vignesh SK</strong></p>
            <p><strong>Batch : AIML-C-WD-E-B20</strong></p>
            <p><strong>Tech Stack:</strong></p>
            <ul>
                <li>🐍 Python</li>
                <li>📊 Streamlit</li>
                <li>🗄️ MySQL Database</li>
                <li>🌐 REST API</li>
                <li>📈 Data Visualization</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Database status
        st.markdown("### 📊 Database Status")
        try:
            db = st.session_state.db_connection
            players_count = db.execute_query("SELECT COUNT(*) as count FROM players")
            teams_count = db.execute_query("SELECT COUNT(*) as count FROM teams")
            
            if not players_count.empty and not teams_count.empty:
                st.success(f"✅ MySQL Connected")
                st.info(f"Players: {players_count.iloc[0]['count']}")
                st.info(f"Teams: {teams_count.iloc[0]['count']}")
            else:
                st.warning("⚠️ Database Issues")
        except Exception as e:
            st.error(f"❌ Database Error: {str(e)[:50]}...")
        
        # API status
        st.markdown("### 🌐 API Status")
        st.success("✅ API Key Configured")
        st.info("Using live Cricbuzz data")
        
        return pages[selected_page]

def populate_with_real_data():
    """Populate database with real cricket data from API"""
    st.markdown("### 🌐 Real-Time Data Integration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Fetch Latest Matches"):
            with st.spinner("Fetching real cricket data from Cricbuzz API..."):
                try:
                    api_client = st.session_state.api_client
                    db = st.session_state.db_connection
                    
                    # Test API connection
                    api_working = api_client.test_api_connection()
                    
                    if api_working:
                        # Get recent matches from API
                        recent_matches = api_client.get_recent_matches()
                        
                        if recent_matches:
                            # Store matches in database
                            stored_count = 0
                            for match in recent_matches[:10]:  # Store first 10 matches
                                success = db.insert_real_match_data(match)
                                if success:
                                    stored_count += 1
                            
                            st.success(f"✅ Successfully stored {stored_count} real matches in MySQL database!")
                            
                            # Show sample of fetched data
                            if recent_matches:
                                st.markdown("**Sample of fetched matches:**")
                                sample_df = pd.DataFrame(recent_matches[:5])
                                st.dataframe(sample_df[['description', 'team1', 'team2', 'status']], use_container_width=True)
                        else:
                            st.warning("No recent matches found from API")
                    else:
                        st.error("API connection failed")
                        
                except Exception as e:
                    st.error(f"Error fetching real data: {e}")
    
    with col2:
        if st.button("📊 View Real Match Data"):
            try:
                db = st.session_state.db_connection
                real_matches = db.get_real_matches_from_db()
                
                if not real_matches.empty:
                    st.success(f"Found {len(real_matches)} real matches in database")
                    st.dataframe(real_matches, use_container_width=True)
                else:
                    st.info("No real match data in database yet. Click 'Fetch Latest Matches' first.")
                    
            except Exception as e:
                st.error(f"Error loading real match data: {e}")

def show_home_page():
    """Display home page with real data integration"""
    st.markdown('<h1 class="main-header">🏏 Cricbuzz LiveStats</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-Time Cricket Insights & SQL-Based Analytics</p>', unsafe_allow_html=True)
    
    # Project overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h3>⚡ Real-time Data</h3>
        <p>Live match updates and player statistics from Cricbuzz API</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h3>🗄️ MySQL Database</h3>
        <p>Robust MySQL database with real cricket data storage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
        <h3>⚙️ CRUD Operations</h3>
        <p>Full database management with create, read, update, delete operations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Real data integration section
    populate_with_real_data()
    
    st.markdown("---")
    
    # Database overview
    st.markdown("## 📊 Database Overview")
    
    try:
        db = st.session_state.db_connection
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            players_count = db.execute_query("SELECT COUNT(*) as count FROM players")
            count = players_count.iloc[0]['count'] if not players_count.empty else 0
            st.metric("Total Players", count)
        
        with col2:
            teams_count = db.execute_query("SELECT COUNT(*) as count FROM teams")
            count = teams_count.iloc[0]['count'] if not teams_count.empty else 0
            st.metric("Total Teams", count)
        
        with col3:
            venues_count = db.execute_query("SELECT COUNT(*) as count FROM venues")
            count = venues_count.iloc[0]['count'] if not venues_count.empty else 0
            st.metric("Total Venues", count)
        
        with col4:
            matches_count = db.execute_query("SELECT COUNT(*) as count FROM matches")
            count = matches_count.iloc[0]['count'] if not matches_count.empty else 0
            st.metric("Total Matches", count)
        
        # Top performers
        st.markdown("### 🌟 Top Performers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🏏 Top Run Scorers**")
            top_batsmen = db.execute_query("""
                SELECT name, country, total_runs, batting_average 
                FROM players 
                WHERE total_runs > 0 
                ORDER BY total_runs DESC 
                LIMIT 5
            """)
            if not top_batsmen.empty:
                st.dataframe(top_batsmen, use_container_width=True)
        
        with col2:
            st.markdown("**🎳 Top Wicket Takers**")
            top_bowlers = db.execute_query("""
                SELECT name, country, total_wickets, bowling_average 
                FROM players 
                WHERE total_wickets > 0 
                ORDER BY total_wickets DESC 
                LIMIT 5
            """)
            if not top_bowlers.empty:
                st.dataframe(top_bowlers, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading database stats: {e}")
    
    # API Integration Status
    st.markdown("---")
    st.markdown("## 🌐 API Integration Status")
    
    try:
        api_client = st.session_state.api_client
        
        # Test API call
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Test API Connection"):
                with st.spinner("Testing Cricbuzz API..."):
                    api_working = api_client.test_api_connection()
                    if api_working:
                        st.success("API connection successful!")
                    else:
                        st.error("API connection failed")
        
        with col2:
            if st.button("📋 Show Recent API Data"):
                with st.spinner("Fetching recent matches..."):
                    recent_data = api_client.get_recent_matches()
                    if recent_data:
                        st.write(f"Found {len(recent_data)} recent matches")
                        # Show first few matches
                        for i, match in enumerate(recent_data[:3]):
                            st.write(f"{i+1}. {match.get('description', 'N/A')} - {match.get('status', 'N/A')}")
                    else:
                        st.warning("No recent match data available")
    
    except Exception as e:
        st.error(f"Error with API integration: {e}")
    
    # Getting started guide
    st.markdown("## 🚀 Getting Started")
    
    with st.expander("📖 How to use this application"):
        st.markdown("""
        1. **🏠 Home**: Overview and real data integration (you are here!)
        2. **📊 Live Matches**: View ongoing cricket matches with real-time data
        3. **⭐ Player Stats**: Browse player statistics with filtering options
        4. **🔍 SQL Analytics**: Execute 25+ SQL queries on real cricket data
        5. **⚙️ CRUD Operations**: Manage player and team data in MySQL database
        
        **Real Data**: Click 'Fetch Latest Matches' above to populate database with live cricket data
        
        **Navigation**: Use the sidebar on the left to switch between pages
        """)

def show_live_matches():
    """Display live matches page with real API data"""
    st.markdown("# 📊 Live Cricket Matches")
    st.markdown("Real-time cricket match updates from Cricbuzz API")
    
    api_client = st.session_state.api_client
    
    # API status indicator
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Data Source**: Cricbuzz API with your RapidAPI key")
    with col2:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Tabs for different match types
    tab1, tab2, tab3 = st.tabs(["🔴 Live Matches", "📋 Recent Matches", "🗄️ Stored Matches"])
    
    with tab1:
        st.markdown("### 🔴 Currently Live Matches")
        
        with st.spinner("Fetching live matches from Cricbuzz API..."):
            live_matches = api_client.get_live_matches()
        
        if live_matches:
            st.success(f"Found {len(live_matches)} live matches")
            
            for i, match in enumerate(live_matches):
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{match.get('description', 'N/A')}**")
                        st.markdown(f"🏟️ {match.get('venue', 'N/A')}, {match.get('city', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"⚔️ **{match.get('team1', 'N/A')} vs {match.get('team2', 'N/A')}**")
                        st.markdown(f"📊 {match.get('status', 'N/A')}")
                    
                    with col3:
                        st.markdown(f"🏏 {match.get('format', 'N/A')}")
                        if st.button(f"Store Match", key=f"store_live_{i}"):
                            # Store this match in database
                            db = st.session_state.db_connection
                            success = db.insert_real_match_data(match)
                            if success:
                                st.success("Match stored in database!")
                            else:
                                st.error("Failed to store match")
                    
                    st.markdown("---")
        else:
            st.info("🔍 No live matches currently available from API")
    
    with tab2:
        st.markdown("### 📋 Recent Completed Matches")
        
        with st.spinner("Fetching recent matches from API..."):
            recent_matches = api_client.get_recent_matches()
        
        if recent_matches:
            st.success(f"Found {len(recent_matches)} recent matches from API")
            
            # Store all button
            if st.button("💾 Store All Recent Matches in Database"):
                db = st.session_state.db_connection
                stored_count = 0
                
                progress_bar = st.progress(0)
                for i, match in enumerate(recent_matches):
                    success = db.insert_real_match_data(match)
                    if success:
                        stored_count += 1
                    progress_bar.progress((i + 1) / len(recent_matches))
                
                st.success(f"Stored {stored_count}/{len(recent_matches)} matches in database")
            
            # Display recent matches
            for i, match in enumerate(recent_matches[:10]):
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{match.get('description', 'N/A')}**")
                        st.markdown(f"🏟️ {match.get('venue', 'N/A')}, {match.get('city', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"⚔️ **{match.get('team1', 'N/A')} vs {match.get('team2', 'N/A')}**")
                        st.markdown(f"🏆 {match.get('result', match.get('status', 'N/A'))}")
                    
                    with col3:
                        st.markdown(f"🏏 {match.get('format', 'N/A')}")
                        if st.button(f"Details", key=f"recent_{i}"):
                            st.json(match)  # Show full match details
                    
                    st.markdown("---")
        else:
            st.warning("No recent matches available from API")
    
    with tab3:
        st.markdown("### 🗄️ Matches Stored in Database")
        
        try:
            db = st.session_state.db_connection
            stored_matches = db.get_real_matches_from_db()
            
            if not stored_matches.empty:
                st.success(f"Found {len(stored_matches)} matches stored in MySQL database")
                st.dataframe(stored_matches, use_container_width=True)
            else:
                st.info("No matches stored in database yet. Use 'Store All Recent Matches' button to populate.")
                
        except Exception as e:
            st.error(f"Error loading stored matches: {e}")

def show_player_stats():
    """Display player statistics page"""
    st.markdown("# ⭐ Player Statistics")
    st.markdown("Cricket player performance and career statistics")
    
    api_client = st.session_state.api_client
    db = st.session_state.db_connection
    
    # Tabs for different stats
    tab1, tab2, tab3 = st.tabs(["🏏 Batting Stats", "🎳 Bowling Stats", "🔍 Player Search"])
    
    with tab1:
        st.markdown("### 🏏 Top Batsmen Statistics")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            country_filter = st.selectbox("Filter by Country", ["All", "India", "Australia", "England", "Pakistan", "New Zealand"])
        with col2:
            sort_by = st.selectbox("Sort by", ["Total Runs", "Batting Average", "Strike Rate", "Centuries"])
        
        try:
            # Build query based on filters
            base_query = """
                SELECT name, country, total_runs, batting_average, strike_rate, 
                       centuries, fifties, matches_played
                FROM players 
                WHERE total_runs > 0
            """
            
            if country_filter != "All":
                base_query += f" AND country = '{country_filter}'"
            
            # Add sorting
            sort_mapping = {
                "Total Runs": "total_runs DESC",
                "Batting Average": "batting_average DESC",
                "Strike Rate": "strike_rate DESC",
                "Centuries": "centuries DESC"
            }
            base_query += f" ORDER BY {sort_mapping[sort_by]} LIMIT 20"
            
            batting_stats = db.execute_query(base_query)
            
            if not batting_stats.empty:
                st.dataframe(
                    batting_stats,
                    use_container_width=True,
                    column_config={
                        "total_runs": st.column_config.NumberColumn("Runs", format="%d"),
                        "batting_average": st.column_config.NumberColumn("Average", format="%.2f"),
                        "strike_rate": st.column_config.NumberColumn("Strike Rate", format="%.2f"),
                        "centuries": st.column_config.NumberColumn("100s", format="%d"),
                        "fifties": st.column_config.NumberColumn("50s", format="%d")
                    }
                )
                
                # Visualization
                if st.checkbox("Show Batting Visualization"):
                    import plotly.express as px
                    
                    fig = px.scatter(
                        batting_stats.head(10),
                        x="batting_average",
                        y="strike_rate",
                        size="total_runs",
                        color="country",
                        hover_name="name",
                        title="Batting Average vs Strike Rate",
                        labels={
                            "batting_average": "Batting Average",
                            "strike_rate": "Strike Rate",
                            "total_runs": "Total Runs"
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No batting statistics available")
                
        except Exception as e:
            st.error(f"Error loading batting stats: {e}")
    
    with tab2:
        st.markdown("### 🎳 Top Bowlers Statistics")
        
        try:
            bowling_stats = db.execute_query("""
                SELECT name, country, total_wickets, bowling_average, economy_rate, matches_played
                FROM players 
                WHERE total_wickets > 0
                ORDER BY total_wickets DESC
                LIMIT 20
            """)
            
            if not bowling_stats.empty:
                st.dataframe(
                    bowling_stats,
                    use_container_width=True,
                    column_config={
                        "total_wickets": st.column_config.NumberColumn("Wickets", format="%d"),
                        "bowling_average": st.column_config.NumberColumn("Bowling Avg", format="%.2f"),
                        "economy_rate": st.column_config.NumberColumn("Economy", format="%.2f")
                    }
                )
                
                # Bowling visualization
                if st.checkbox("Show Bowling Visualization"):
                    import plotly.express as px
                    
                    fig = px.bar(
                        bowling_stats.head(10),
                        x="name",
                        y="total_wickets",
                        color="economy_rate",
                        title="Top Wicket Takers",
                        labels={"total_wickets": "Total Wickets", "name": "Player"}
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No bowling statistics available")
                
        except Exception as e:
            st.error(f"Error loading bowling stats: {e}")
    
    with tab3:
        st.markdown("### 🔍 Player Search")
        
        search_name = st.text_input("Enter player name to search:")
        
        if search_name:
            try:
                search_results = db.execute_query("""
                    SELECT * FROM players 
                    WHERE name LIKE %s
                    ORDER BY matches_played DESC
                """, (f"%{search_name}%",))
                
                if not search_results.empty:
                    st.markdown(f"**Found {len(search_results)} player(s):**")
                    
                    for _, player in search_results.iterrows():
                        with st.expander(f"🏏 {player['name']} ({player['country']})"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**🏏 Batting Stats:**")
                                st.write(f"Total Runs: {player['total_runs']}")
                                st.write(f"Average: {player['batting_average']:.2f}")
                                st.write(f"Strike Rate: {player['strike_rate']:.2f}")
                                st.write(f"Centuries: {player['centuries']}")
                                st.write(f"Fifties: {player['fifties']}")
                            
                            with col2:
                                st.markdown("**🎳 Bowling Stats:**")
                                st.write(f"Wickets: {player['total_wickets']}")
                                st.write(f"Bowling Average: {player['bowling_average']:.2f}")
                                st.write(f"Economy Rate: {player['economy_rate']:.2f}")
                                st.write(f"Playing Role: {player['playing_role']}")
                                st.write(f"Matches: {player['matches_played']}")
                else:
                    st.info(f"No players found with name containing '{search_name}'")
                    
            except Exception as e:
                st.error(f"Error searching players: {e}")

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Show sidebar and get selected page
    current_page = show_sidebar()
    
    # Display selected page
    if current_page == "home":
        show_home_page()
    elif current_page == "live_matches":
        show_live_matches()
    elif current_page == "player_stats":
        show_player_stats()
    elif current_page == "sql_analytics":
        try:
            from utils.sql_queries import show_sql_analytics_page
            show_sql_analytics_page(st.session_state.db_connection)
        except ImportError:
            st.markdown("# 🔍 SQL Analytics")
            st.error("SQL Analytics module not found. Please create utils/sql_queries.py")
            st.info("This page will show 25 SQL queries for cricket data analysis")
    elif current_page == "crud_operations":
        try:
            from utils.crud_operations import show_crud_operations_page
            show_crud_operations_page(st.session_state.db_connection)
        except ImportError:
            st.markdown("# ⚙️ CRUD Operations")
            st.error("CRUD Operations module not found. Please create utils/crud_operations.py")
            st.info("This page will provide database management operations")

if __name__ == "__main__":
    main()