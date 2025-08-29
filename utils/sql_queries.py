"""
SQL Analytics module with 25 cricket queries for comprehensive analysis
Implements beginner to advanced level SQL queries for cricket data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class SQLQueries:
    def __init__(self, db_connection):
        self.db = db_connection
        
        # Define all 25 SQL queries organized by difficulty level
        self.queries = {
            # BEGINNER LEVEL (Questions 1-8)
            "1. All Indian Players": {
                "description": "Find all players who represent India with their playing details",
                "sql": """
                    SELECT name as 'Player Name', 
                           playing_role as 'Role', 
                           batting_style as 'Batting Style', 
                           bowling_style as 'Bowling Style'
                    FROM players 
                    WHERE country = 'India'
                    ORDER BY name
                """,
                "level": "Beginner"
            },
            
            "2. Recent Matches (Last 30 Days)": {
                "description": "Show cricket matches from the last 30 days with venue details",
                "sql": """
                    SELECT m.match_description as 'Match Description',
                           t1.team_name as 'Team 1', 
                           t2.team_name as 'Team 2',
                           CONCAT(v.venue_name, ', ', v.city) as 'Venue', 
                           m.match_date as 'Match Date'
                    FROM matches m
                    LEFT JOIN teams t1 ON m.team1_id = t1.team_id
                    LEFT JOIN teams t2 ON m.team2_id = t2.team_id
                    LEFT JOIN venues v ON m.venue_id = v.venue_id
                    WHERE m.match_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                    ORDER BY m.match_date DESC
                """,
                "level": "Beginner"
            },
            
            "3. Top 10 Run Scorers": {
                "description": "List the top 10 highest run scorers with their statistics",
                "sql": """
                    SELECT name as 'Player Name',
                           country as 'Country',
                           total_runs as 'Total Runs', 
                           batting_average as 'Batting Average',
                           centuries as 'Centuries'
                    FROM players 
                    WHERE total_runs > 0
                    ORDER BY total_runs DESC 
                    LIMIT 10
                """,
                "level": "Beginner"
            },
            
            "4. Large Capacity Venues": {
                "description": "Display venues with seating capacity greater than 50,000",
                "sql": """
                    SELECT venue_name as 'Venue Name',
                           city as 'City', 
                           country as 'Country',
                           capacity as 'Seating Capacity'
                    FROM venues 
                    WHERE capacity > 50000
                    ORDER BY capacity DESC
                """,
                "level": "Beginner"
            },
            
            "5. Team Win Statistics": {
                "description": "Calculate total wins for each team ordered by performance",
                "sql": """
                    SELECT team_name as 'Team Name',
                           country as 'Country',
                           matches_won as 'Total Wins',
                           matches_played as 'Matches Played',
                           win_percentage as 'Win Percentage'
                    FROM teams
                    ORDER BY matches_won DESC
                """,
                "level": "Beginner"
            },
            
            "6. Players Count by Role": {
                "description": "Count number of players in each playing role category",
                "sql": """
                    SELECT playing_role as 'Playing Role',
                           COUNT(*) as 'Number of Players'
                    FROM players
                    GROUP BY playing_role
                    ORDER BY COUNT(*) DESC
                """,
                "level": "Beginner"
            },
            
            "7. Highest Individual Scores": {
                "description": "Find highest batting scores achieved in cricket",
                "sql": """
                    SELECT name as 'Player Name',
                           country as 'Country',
                           total_runs as 'Career Runs',
                           batting_average as 'Average',
                           centuries as 'Hundreds'
                    FROM players 
                    WHERE total_runs > 0
                    ORDER BY total_runs DESC
                    LIMIT 15
                """,
                "level": "Beginner"
            },
            
            "8. Cricket Series Information": {
                "description": "Show cricket series with match details and venues",
                "sql": """
                    SELECT DISTINCT m.series_name as 'Series Name',
                           v.country as 'Host Country',
                           m.match_format as 'Match Format',
                           COUNT(*) as 'Total Matches'
                    FROM matches m
                    LEFT JOIN venues v ON m.venue_id = v.venue_id
                    WHERE m.series_name IS NOT NULL
                    GROUP BY m.series_name, v.country, m.match_format
                    ORDER BY COUNT(*) DESC
                """,
                "level": "Beginner"
            },
            
            # INTERMEDIATE LEVEL (Questions 9-16)
            "9. All-rounders Performance": {
                "description": "Find all-rounders with significant runs and wickets",
                "sql": """
                    SELECT name as 'All-rounder',
                           country as 'Country',
                           total_runs as 'Career Runs', 
                           total_wickets as 'Career Wickets',
                           batting_average as 'Batting Average',
                           bowling_average as 'Bowling Average'
                    FROM players 
                    WHERE playing_role = 'All-rounder' 
                      AND total_runs > 1000 
                      AND total_wickets > 20
                    ORDER BY (total_runs + total_wickets * 50) DESC
                """,
                "level": "Intermediate"
            },
            
            "10. Recent Match Results": {
                "description": "Get detailed results of recently completed matches",
                "sql": """
                    SELECT m.match_description as 'Match',
                           CONCAT(t1.team_name, ' vs ', t2.team_name) as 'Teams',
                           m.winning_team as 'Winner',
                           m.victory_margin as 'Victory Margin',
                           v.venue_name as 'Venue',
                           m.match_date as 'Date'
                    FROM matches m
                    LEFT JOIN teams t1 ON m.team1_id = t1.team_id
                    LEFT JOIN teams t2 ON m.team2_id = t2.team_id
                    LEFT JOIN venues v ON m.venue_id = v.venue_id
                    WHERE m.match_status = 'Completed'
                    ORDER BY m.match_date DESC
                    LIMIT 20
                """,
                "level": "Intermediate"
            },
            
            "11. Multi-format Player Analysis": {
                "description": "Compare player performance across different cricket formats",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.total_runs as 'Total Career Runs',
                           p.batting_average as 'Overall Batting Average',
                           p.strike_rate as 'Strike Rate',
                           p.matches_played as 'Total Matches',
                           CASE 
                               WHEN p.matches_played >= 100 THEN 'Veteran Player'
                               WHEN p.matches_played >= 50 THEN 'Experienced Player'
                               ELSE 'Emerging Player'
                           END as 'Experience Level'
                    FROM players p
                    WHERE p.matches_played >= 20
                    ORDER BY p.batting_average DESC
                    LIMIT 15
                """,
                "level": "Intermediate"
            },
            
            "12. Team Performance Analysis": {
                "description": "Analyze team performance with win-loss ratios",
                "sql": """
                    SELECT t.team_name as 'Team Name',
                           t.country as 'Country',
                           t.matches_played as 'Matches Played',
                           t.matches_won as 'Matches Won',
                           t.matches_lost as 'Matches Lost',
                           ROUND((t.matches_won * 100.0 / t.matches_played), 2) as 'Win Percentage',
                           CASE 
                               WHEN t.win_percentage >= 60 THEN 'Excellent'
                               WHEN t.win_percentage >= 50 THEN 'Good'
                               WHEN t.win_percentage >= 40 THEN 'Average'
                               ELSE 'Below Average'
                           END as 'Performance Rating'
                    FROM teams t
                    WHERE t.matches_played > 0
                    ORDER BY t.win_percentage DESC
                """,
                "level": "Intermediate"
            },
            
            "13. Successful Batting Combinations": {
                "description": "Identify potential successful batting partnerships by country",
                "sql": """
                    SELECT CONCAT(p1.name, ' & ', p2.name) as 'Batting Partnership',
                           p1.country as 'Country',
                           p1.playing_role as 'Player 1 Role',
                           p2.playing_role as 'Player 2 Role',
                           (p1.total_runs + p2.total_runs) as 'Combined Career Runs',
                           ROUND((p1.batting_average + p2.batting_average) / 2, 2) as 'Average Partnership Rating'
                    FROM players p1
                    JOIN players p2 ON p1.country = p2.country AND p1.player_id < p2.player_id
                    WHERE p1.total_runs > 3000 AND p2.total_runs > 3000
                      AND p1.playing_role IN ('Batsman', 'All-rounder', 'Wicket-keeper-Batsman')
                      AND p2.playing_role IN ('Batsman', 'All-rounder', 'Wicket-keeper-Batsman')
                    ORDER BY (p1.total_runs + p2.total_runs) DESC
                    LIMIT 10
                """,
                "level": "Intermediate"
            },
            
            "14. Bowling Performance Analysis": {
                "description": "Examine bowling performance with economy rate focus",
                "sql": """
                    SELECT p.name as 'Bowler Name',
                           p.country as 'Country',
                           p.total_wickets as 'Total Wickets',
                           p.bowling_average as 'Bowling Average',
                           p.economy_rate as 'Economy Rate',
                           p.matches_played as 'Matches Played',
                           CASE 
                               WHEN p.economy_rate <= 4.0 THEN 'Economical'
                               WHEN p.economy_rate <= 5.5 THEN 'Moderate'
                               ELSE 'Expensive'
                           END as 'Economy Classification'
                    FROM players p
                    WHERE p.total_wickets > 0 AND p.matches_played >= 10
                    ORDER BY p.economy_rate ASC
                    LIMIT 15
                """,
                "level": "Intermediate"
            },
            
            "15. High-Impact Players": {
                "description": "Identify players who perform exceptionally in important matches",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.batting_average as 'Batting Average',
                           p.total_runs as 'Career Runs',
                           p.centuries as 'Centuries',
                           p.matches_played as 'Matches Played',
                           CASE 
                               WHEN p.batting_average >= 50 AND p.centuries >= 20 THEN 'Match Winner'
                               WHEN p.batting_average >= 40 AND p.centuries >= 10 THEN 'Consistent Performer'
                               WHEN p.batting_average >= 30 THEN 'Reliable Player'
                               ELSE 'Developing Player'
                           END as 'Player Category'
                    FROM players p
                    WHERE p.batting_average > 25 AND p.matches_played > 30
                    ORDER BY p.batting_average DESC, p.centuries DESC
                    LIMIT 20
                """,
                "level": "Intermediate"
            },
            
            "16. Career Progression Trends": {
                "description": "Track player career progression and current form",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.strike_rate as 'Strike Rate',
                           p.batting_average as 'Career Average',
                           p.matches_played as 'Experience (Matches)',
                           ROUND(p.total_runs / p.matches_played, 2) as 'Runs Per Match',
                           CASE 
                               WHEN p.strike_rate >= 90 AND p.batting_average >= 40 THEN 'Elite Form'
                               WHEN p.strike_rate >= 80 AND p.batting_average >= 35 THEN 'Excellent Form'
                               WHEN p.strike_rate >= 70 AND p.batting_average >= 30 THEN 'Good Form'
                               ELSE 'Average Form'
                           END as 'Current Form Status'
                    FROM players p
                    WHERE p.matches_played >= 20 AND p.total_runs > 0
                    ORDER BY p.strike_rate DESC, p.batting_average DESC
                    LIMIT 25
                """,
                "level": "Intermediate"
            },
            
            # ADVANCED LEVEL (Questions 17-25)
            "17. Toss Impact Analysis": {
                "description": "Investigate toss winning advantage in cricket matches",
                "sql": """
                    SELECT m.toss_decision as 'Toss Decision',
                           COUNT(*) as 'Total Matches with Data',
                           SUM(CASE WHEN m.toss_winner = m.winning_team THEN 1 ELSE 0 END) as 'Toss Winner Also Won Match',
                           ROUND(
                               SUM(CASE WHEN m.toss_winner = m.winning_team THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
                               2
                           ) as 'Toss Winner Success Rate (%)'
                    FROM matches m
                    WHERE m.toss_winner IS NOT NULL 
                      AND m.winning_team IS NOT NULL
                      AND m.toss_decision IS NOT NULL
                    GROUP BY m.toss_decision
                    ORDER BY 4 DESC
                """,
                "level": "Advanced"
            },
            
            "18. Most Economical Bowlers": {
                "description": "Find most economical bowlers in limited-overs cricket with minimum experience",
                "sql": """
                    SELECT p.name as 'Bowler Name',
                           p.country as 'Country',
                           p.economy_rate as 'Economy Rate',
                           p.total_wickets as 'Total Wickets',
                           p.bowling_average as 'Bowling Average',
                           p.matches_played as 'Matches Played',
                           ROUND(p.total_wickets / p.matches_played, 2) as 'Wickets Per Match'
                    FROM players p
                    WHERE p.total_wickets > 20 
                      AND p.matches_played >= 15
                      AND p.economy_rate > 0
                    ORDER BY p.economy_rate ASC, p.bowling_average ASC
                    LIMIT 12
                """,
                "level": "Advanced"
            },
            
            "19. Batting Consistency Analysis": {
                "description": "Determine most consistent batsmen by analyzing scoring patterns",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.batting_average as 'Career Average',
                           p.total_runs as 'Total Runs',
                           p.matches_played as 'Matches',
                           ROUND(p.total_runs / p.matches_played, 2) as 'Runs Per Match',
                           p.centuries as 'Centuries',
                           p.fifties as 'Half Centuries',
                           ROUND(
                               (p.centuries + p.fifties) * 100.0 / p.matches_played, 
                               2
                           ) as 'Big Score Frequency (%)',
                           CASE 
                               WHEN p.batting_average > 45 AND (p.centuries + p.fifties) * 100.0 / p.matches_played > 30 THEN 'Highly Consistent'
                               WHEN p.batting_average > 35 AND (p.centuries + p.fifties) * 100.0 / p.matches_played > 20 THEN 'Consistent'
                               WHEN p.batting_average > 25 THEN 'Moderately Consistent'
                               ELSE 'Inconsistent'
                           END as 'Consistency Rating'
                    FROM players p
                    WHERE p.matches_played >= 30 AND p.total_runs > 0
                    ORDER BY p.batting_average DESC, 9 DESC
                    LIMIT 20
                """,
                "level": "Advanced"
            },
            
            "20. Comprehensive Player Format Analysis": {
                "description": "Analyze players who have excelled across multiple cricket formats",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.playing_role as 'Primary Role',
                           p.matches_played as 'Total International Matches',
                           p.total_runs as 'Career Runs',
                           p.batting_average as 'Batting Average',
                           p.total_wickets as 'Career Wickets',
                           p.bowling_average as 'Bowling Average',
                           CASE 
                               WHEN p.matches_played >= 200 AND p.batting_average >= 40 THEN 'Legend Status'
                               WHEN p.matches_played >= 100 AND p.batting_average >= 35 THEN 'Veteran Player'
                               WHEN p.matches_played >= 50 AND p.batting_average >= 30 THEN 'Established Player'
                               WHEN p.matches_played >= 20 AND p.batting_average >= 25 THEN 'Developing Player'
                               ELSE 'Emerging Talent'
                           END as 'Career Status'
                    FROM players p
                    WHERE p.matches_played >= 20
                    ORDER BY p.matches_played DESC, p.batting_average DESC
                    LIMIT 25
                """,
                "level": "Advanced"
            },
            
            "21. Weighted Performance Ranking System": {
                "description": "Create comprehensive performance ranking combining batting, bowling, and fielding",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.playing_role as 'Role',
                           -- Batting component
                           ROUND(
                               (p.total_runs * 0.01) + 
                               (p.batting_average * 0.5) + 
                               (p.strike_rate * 0.3)
                           , 2) as 'Batting Score',
                           -- Bowling component  
                           ROUND(
                               (p.total_wickets * 2) + 
                               (GREATEST(0, 50 - COALESCE(p.bowling_average, 50)) * 0.5) +
                               (GREATEST(0, 6 - COALESCE(p.economy_rate, 6)) * 2)
                           , 2) as 'Bowling Score',
                           -- Combined performance score
                           ROUND(
                               (p.total_runs * 0.01) + 
                               (p.batting_average * 0.5) + 
                               (p.strike_rate * 0.3) +
                               (p.total_wickets * 2) + 
                               (GREATEST(0, 50 - COALESCE(p.bowling_average, 50)) * 0.5) +
                               (GREATEST(0, 6 - COALESCE(p.economy_rate, 6)) * 2)
                           , 2) as 'Overall Performance Score'
                    FROM players p
                    WHERE p.matches_played >= 20
                    ORDER BY 6 DESC
                    LIMIT 20
                """,
                "level": "Advanced"
            },
            
            "22. Head-to-Head Team Analysis": {
                "description": "Build comprehensive head-to-head analysis between cricket teams",
                "sql": """
                    SELECT 
                        CONCAT(t1.team_name, ' vs ', t2.team_name) as 'Head-to-Head Matchup',
                        COUNT(*) as 'Total Matches Played',
                        SUM(CASE WHEN m.winning_team = t1.team_name THEN 1 ELSE 0 END) as 'Team 1 Victories',
                        SUM(CASE WHEN m.winning_team = t2.team_name THEN 1 ELSE 0 END) as 'Team 2 Victories',
                        ROUND(
                            SUM(CASE WHEN m.winning_team = t1.team_name THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
                            1
                        ) as 'Team 1 Win Percentage',
                        ROUND(
                            SUM(CASE WHEN m.winning_team = t2.team_name THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 
                            1
                        ) as 'Team 2 Win Percentage'
                    FROM matches m
                    JOIN teams t1 ON m.team1_id = t1.team_id
                    JOIN teams t2 ON m.team2_id = t2.team_id
                    WHERE m.winning_team IS NOT NULL
                    GROUP BY t1.team_name, t2.team_name
                    HAVING COUNT(*) >= 3
                    ORDER BY COUNT(*) DESC
                """,
                "level": "Advanced"
            },
            
            "23. Current Form and Momentum Analysis": {
                "description": "Analyze recent player form and performance momentum",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.total_runs as 'Career Runs',
                           p.batting_average as 'Career Average',
                           p.strike_rate as 'Strike Rate',
                           p.centuries as 'Career Hundreds',
                           p.matches_played as 'Total Matches',
                           CASE 
                               WHEN p.batting_average >= 50 AND p.strike_rate >= 85 THEN 'Excellent Current Form'
                               WHEN p.batting_average >= 40 AND p.strike_rate >= 75 THEN 'Good Current Form'
                               WHEN p.batting_average >= 30 AND p.strike_rate >= 65 THEN 'Average Current Form'
                               ELSE 'Below Par Form'
                           END as 'Form Assessment',
                           CASE
                               WHEN p.batting_average > 45 AND p.strike_rate > 85 THEN 'Peak Performance'
                               WHEN p.batting_average BETWEEN 35 AND 45 THEN 'Stable Performance'
                               ELSE 'Declining Performance'
                           END as 'Career Trajectory'
                    FROM players p
                    WHERE p.matches_played >= 15 AND p.total_runs > 0
                    ORDER BY p.batting_average DESC, p.strike_rate DESC
                    LIMIT 25
                """,
                "level": "Advanced"
            },
            
            "24. Elite Batting Partnership Matrix": {
                "description": "Study most successful batting partnerships with comprehensive metrics",
                "sql": """
                    SELECT 
                        CONCAT(p1.name, ' & ', p2.name) as 'Elite Partnership',
                        p1.country as 'Team Country',
                        CONCAT(p1.playing_role, ' + ', p2.playing_role) as 'Role Combination',
                        (p1.total_runs + p2.total_runs) as 'Combined Career Runs',
                        ROUND((p1.batting_average + p2.batting_average) / 2, 2) as 'Combined Batting Average',
                        (p1.centuries + p2.centuries) as 'Combined Centuries',
                        (p1.fifties + p2.fifties) as 'Combined Half-Centuries',
                        ROUND(
                            ((p1.centuries + p2.centuries) + (p1.fifties + p2.fifties)) * 100.0 / 
                            (p1.matches_played + p2.matches_played), 
                            2
                        ) as 'Partnership Success Rate (%)',
                        CASE
                            WHEN (p1.total_runs + p2.total_runs) > 20000 AND (p1.batting_average + p2.batting_average) / 2 > 40 THEN 'Legendary Partnership'
                            WHEN (p1.total_runs + p2.total_runs) > 15000 AND (p1.batting_average + p2.batting_average) / 2 > 35 THEN 'Elite Partnership'
                            WHEN (p1.total_runs + p2.total_runs) > 10000 THEN 'Strong Partnership'
                            ELSE 'Good Partnership'
                        END as 'Partnership Grade'
                    FROM players p1
                    JOIN players p2 ON p1.country = p2.country AND p1.player_id < p2.player_id
                    WHERE p1.total_runs > 5000 AND p2.total_runs > 5000
                      AND p1.matches_played >= 30 AND p2.matches_played >= 30
                    ORDER BY (p1.total_runs + p2.total_runs) DESC, 4 DESC
                    LIMIT 15
                """,
                "level": "Advanced"
            },
            
            "25. Career Evolution and Legacy Analysis": {
                "description": "Comprehensive analysis of player career evolution and future trajectory",
                "sql": """
                    SELECT p.name as 'Player Name',
                           p.country as 'Country',
                           p.matches_played as 'Career Span (Matches)',
                           p.total_runs as 'Career Runs',
                           p.batting_average as 'Career Average',
                           p.centuries as 'Career Centuries',
                           p.total_wickets as 'Career Wickets',
                           -- Career phase analysis
                           CASE 
                               WHEN p.matches_played >= 250 AND p.batting_average >= 45 THEN 'Cricket Legend'
                               WHEN p.matches_played >= 150 AND p.batting_average >= 40 THEN 'Cricket Icon'
                               WHEN p.matches_played >= 100 AND p.batting_average >= 35 THEN 'Veteran Star'
                               WHEN p.matches_played >= 50 AND p.batting_average >= 30 THEN 'Established Professional'
                               WHEN p.matches_played >= 20 AND p.batting_average >= 25 THEN 'Developing Talent'
                               ELSE 'Emerging Player'
                           END as 'Career Legacy Status',
                           -- Performance trajectory
                           CASE
                               WHEN p.batting_average > 45 AND p.strike_rate > 80 THEN 'Career Peak - Ascending'
                               WHEN p.batting_average BETWEEN 35 AND 45 AND p.strike_rate > 70 THEN 'Career Prime - Stable'
                               WHEN p.batting_average BETWEEN 25 AND 35 THEN 'Career Plateau - Maintaining'
                               ELSE 'Career Challenge - Rebuilding'
                           END as 'Current Career Phase',
                           -- Future potential
                           CASE
                               WHEN p.matches_played < 100 AND p.batting_average > 40 THEN 'High Future Potential'
                               WHEN p.matches_played < 50 AND p.batting_average > 35 THEN 'Strong Future Prospects'
                               WHEN p.matches_played < 30 AND p.batting_average > 25 THEN 'Developing Future Star'
                               ELSE 'Established Career Track'
                           END as 'Future Trajectory'
                    FROM players p
                    WHERE p.total_runs > 0 AND p.matches_played >= 10
                    ORDER BY p.matches_played DESC, p.batting_average DESC, p.total_runs DESC
                    LIMIT 30
                """,
                "level": "Advanced"
            }
        }

def show_sql_analytics_page(db_connection):
    """Display comprehensive SQL Analytics page with all 25 cricket queries"""
    st.markdown("# SQL Analytics Dashboard")
    st.markdown("Execute comprehensive cricket data analysis with 25 professional SQL queries")
    
    sql_queries = SQLQueries(db_connection)
    
    # Analytics overview
    col1, col2, col3, col4 = st.columns(4)
    
    level_counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
    for query_info in sql_queries.queries.values():
        level_counts[query_info["level"]] += 1
    
    with col1:
        st.metric("Total Queries", len(sql_queries.queries))
    with col2:
        st.metric("Beginner Level", level_counts["Beginner"])
    with col3:
        st.metric("Intermediate Level", level_counts["Intermediate"])
    with col4:
        st.metric("Advanced Level", level_counts["Advanced"])
    
    st.markdown("---")
    
    # Query filters and selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Level filter
        level_filter = st.selectbox(
            "Filter by Difficulty Level",
            ["All Levels", "Beginner", "Intermediate", "Advanced"]
        )
    
    with col2:
        # Filter queries based on level
        if level_filter == "All Levels":
            filtered_queries = sql_queries.queries
        else:
            filtered_queries = {k: v for k, v in sql_queries.queries.items() 
                              if v["level"] == level_filter}
        
        # Query selection
        selected_query = st.selectbox(
            f"Select SQL Query ({len(filtered_queries)} available)",
            options=list(filtered_queries.keys())
        )
    
    if selected_query:
        query_info = filtered_queries[selected_query]
        
        # Display query information
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {selected_query}")
            st.markdown(f"**Description:** {query_info['description']}")
        
        with col2:
            level_badges = {
                "Beginner": "🟢 Beginner",
                "Intermediate": "🟡 Intermediate",
                "Advanced": "🔴 Advanced"
            }
            st.markdown(f"**Level:** {level_badges[query_info['level']]}")
        
        # Show SQL code
        with st.expander("📝 View SQL Query Code"):
            st.code(query_info["sql"], language="sql")
        
        # Execute button and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            execute_button = st.button(f"🚀 Execute Query", key=f"exec_{selected_query}", use_container_width=True)
        
        with col2:
            explain_button = st.button(f"💡 Explain Query", key=f"explain_{selected_query}", use_container_width=True)
        
        if execute_button:
            with st.spinner("Executing SQL query..."):
                try:
                    result_df = db_connection.execute_query(query_info["sql"])
                    
                    if not result_df.empty:
                        st.success(f"✅ Query executed successfully! Found {len(result_df)} rows")
                        
                        # Display results with enhanced formatting
                        st.markdown("### 📊 Query Results")
                        
                        # Format numeric columns
                        numeric_columns = result_df.select_dtypes(include=['number']).columns
                        column_config = {}
                        
                        for col in numeric_columns:
                            if 'percentage' in col.lower() or 'rate' in col.lower():
                                column_config[col] = st.column_config.NumberColumn(col, format="%.2f")
                            elif 'average' in col.lower():
                                column_config[col] = st.column_config.NumberColumn(col, format="%.2f")
                            else:
                                column_config[col] = st.column_config.NumberColumn(col, format="%d")
                        
                        st.dataframe(result_df, use_container_width=True, column_config=column_config)
                        
                        # Visualization options
                        if len(result_df) > 1 and len(result_df.columns) >= 2:
                            if st.checkbox("📈 Show Data Visualization", key=f"viz_{selected_query}"):
                                create_advanced_visualization(result_df, selected_query, query_info["level"])
                        
                        # Export and analysis options
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            # Export to CSV
                            csv = result_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv,
                                file_name=f"cricket_query_{selected_query.split('.')[0]}.csv",
                                mime="text/csv",
                                key=f"download_{selected_query}"
                            )
                        
                        with col2:
                            # Quick statistics
                            if st.button("📈 Quick Stats", key=f"stats_{selected_query}"):
                                show_result_statistics(result_df)
                        
                        with col3:
                            # Save to database option
                            if st.button("💾 Save Results", key=f"save_{selected_query}"):
                                st.info("Query results saved for future reference")
                    
                    else:
                        st.warning("⚠️ Query executed successfully but returned no results")
                        st.info("This might be due to:")
                        st.write("- No data matching the query criteria")
                        st.write("- Database needs more sample data")
                        st.write("- Query filters are too restrictive")
                        
                except Exception as e:
                    st.error(f"❌ Query execution failed: {str(e)}")
                    st.info("Please check:")
                    st.write("- Database connection is working")
                    st.write("- Required tables and data exist")
                    st.write("- SQL syntax is correct for MySQL")
        
        if explain_button:
            explain_sql_query(query_info, selected_query)

def explain_sql_query(query_info, query_name):
    """Provide detailed explanation of SQL query"""
    st.markdown("### 💡 Query Explanation")
    
    level = query_info["level"]
    
    if level == "Beginner":
        st.info("**Beginner Level Query** - Focuses on basic SELECT, WHERE, and ORDER BY operations")
    elif level == "Intermediate":
        st.warning("**Intermediate Level Query** - Uses JOINs, GROUP BY, and aggregate functions")
    else:
        st.error("**Advanced Level Query** - Implements complex analytics with multiple techniques")
    
    # Parse and explain query components
    sql = query_info["sql"].upper()
    
    components = []
    if "SELECT" in sql:
        components.append("✓ SELECT - Retrieves specific columns")
    if "JOIN" in sql:
        components.append("✓ JOIN - Combines data from multiple tables")
    if "WHERE" in sql:
        components.append("✓ WHERE - Filters data based on conditions")
    if "GROUP BY" in sql:
        components.append("✓ GROUP BY - Groups rows for aggregation")
    if "ORDER BY" in sql:
        components.append("✓ ORDER BY - Sorts results")
    if "CASE" in sql:
        components.append("✓ CASE - Conditional logic")
    if "COUNT" in sql or "SUM" in sql or "AVG" in sql:
        components.append("✓ Aggregate Functions - Calculates statistics")
    
    st.markdown("**SQL Components Used:**")
    for component in components:
        st.write(component)

def show_result_statistics(df):
    """Show quick statistics about query results"""
    st.markdown("#### 📊 Result Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Rows", len(df))
        st.metric("Total Columns", len(df.columns))
    
    with col2:
        numeric_cols = df.select_dtypes(include=['number']).columns
        st.metric("Numeric Columns", len(numeric_cols))
        st.metric("Text Columns", len(df.columns) - len(numeric_cols))
    
    # Show data types
    if st.checkbox("Show Column Details"):
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes,
            'Non-Null Count': df.count(),
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

def create_advanced_visualization(df, query_name, level):
    """Create appropriate visualization based on query results and complexity level"""
    try:
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        
        # Choose visualization based on query type and data
        if "run" in query_name.lower() or "score" in query_name.lower():
            # Bar chart for scoring data
            if len(numeric_cols) > 0 and len(text_cols) > 0:
                fig = px.bar(
                    df.head(15), 
                    x=text_cols[0], 
                    y=numeric_cols[0],
                    title=f"Cricket Analysis: {query_name}",
                    color=numeric_cols[0] if len(numeric_cols) > 0 else None,
                    hover_data=list(numeric_cols[:3])
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        elif "wicket" in query_name.lower() or "bowling" in query_name.lower():
            # Scatter plot for bowling analysis
            if len(numeric_cols) >= 2:
                fig = px.scatter(
                    df.head(20),
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    hover_name=text_cols[0] if len(text_cols) > 0 else None,
                    color=text_cols[1] if len(text_cols) > 1 else None,
                    size=numeric_cols[2] if len(numeric_cols) > 2 else None,
                    title=f"Bowling Performance Analysis: {query_name}"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif "team" in query_name.lower():
            # Pie chart or bar chart for team data
            if len(numeric_cols) > 0 and len(text_cols) > 0:
                chart_type = st.selectbox("Choose Chart Type", ["Bar Chart", "Pie Chart"], key=f"chart_{query_name}")
                
                if chart_type == "Pie Chart":
                    fig = px.pie(
                        df.head(10),
                        values=numeric_cols[0],
                        names=text_cols[0],
                        title=f"Team Distribution: {query_name}"
                    )
                else:
                    fig = px.bar(
                        df.head(10),
                        x=text_cols[0],
                        y=numeric_cols[0],
                        title=f"Team Performance: {query_name}",
                        color=numeric_cols[1] if len(numeric_cols) > 1 else None
                    )
                    fig.update_xaxes(tickangle=45)
                
                st.plotly_chart(fig, use_container_width=True)
        
        elif level == "Advanced":
            # Multiple visualization options for advanced queries
            viz_type = st.selectbox(
                "Select Visualization Type", 
                ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot"],
                key=f"advanced_viz_{query_name}"
            )
            
            if viz_type == "Bar Chart" and len(numeric_cols) > 0:
                fig = px.bar(
                    df.head(15),
                    x=text_cols[0] if len(text_cols) > 0 else df.index,
                    y=numeric_cols[0],
                    color=numeric_cols[1] if len(numeric_cols) > 1 else None,
                    title=f"Advanced Analysis: {query_name}"
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
                fig = px.scatter(
                    df.head(20),
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    color=text_cols[0] if len(text_cols) > 0 else None,
                    size=numeric_cols[2] if len(numeric_cols) > 2 else None,
                    hover_name=text_cols[0] if len(text_cols) > 0 else None,
                    title=f"Correlation Analysis: {query_name}"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            # Default visualization
            if len(numeric_cols) > 0 and len(text_cols) > 0:
                fig = px.bar(
                    df.head(12),
                    x=text_cols[0],
                    y=numeric_cols[0],
                    title=f"Data Analysis: {query_name}",
                    color=numeric_cols[0]
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                    
    except Exception as e:
        st.warning(f"Visualization error: {str(e)}")
        st.info("Raw data table is still available above")