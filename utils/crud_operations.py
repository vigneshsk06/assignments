"""
Complete CRUD Operations module for a Cricket database (Streamlit)
Fully organized and stitched: View, Create, Update, Delete, Bulk tools, and DB utilities.

"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

# =========================================
# ENTRYPOINT
# =========================================
def show_crud_operations_page(db_connection):
    st.markdown("# Database Management System")
    st.markdown("Complete CRUD operations for cricket data with advanced features")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📖 View Data",
        "➕ Add Records",
        "✏️ Edit Records",
        "🗑️ Delete Records",
        "📊 Bulk Operations",
        "🔧 Database Tools",
    ])

    with tab1:
        show_read_operations(db_connection)

    with tab2:
        show_create_operations(db_connection)

    with tab3:
        show_update_operations(db_connection)

    with tab4:
        show_delete_operations(db_connection)

    with tab5:
        show_bulk_operations(db_connection)

    with tab6:
        show_database_tools(db_connection)

# =========================================
# READ
# =========================================
def show_read_operations(db_connection):
    st.markdown("## 📖 View Database Records")

    col1, col2, col3 = st.columns(3)
    with col1:
        table_options = {
            "Players Database": "players",
            "Teams Information": "teams",
            "Venue Details": "venues",
            "Match Records": "matches",
        }
        selected_table_label = st.selectbox("Select table to explore:", list(table_options.keys()))
        table_name = table_options[selected_table_label]

    with col2:
        limit = st.number_input("Records to display:", min_value=5, max_value=200, value=25)

    with col3:
        sort_order = st.selectbox("Sort order:", ["DESC (Newest First)", "ASC (Oldest First)"])
        sort_direction = "DESC" if "DESC" in sort_order else "ASC"

    # Optional player filters
    country_filter = []
    role_filter = []
    min_matches = 0
    if table_name == "players":
        st.markdown("### 🔍 Player Filters")
        f1, f2, f3 = st.columns(3)
        with f1:
            country_filter = st.multiselect(
                "Filter by Countries:",
                [
                    "India",
                    "Australia",
                    "England",
                    "Pakistan",
                    "New Zealand",
                    "South Africa",
                    "West Indies",
                    "Sri Lanka",
                    "Bangladesh",
                ],
            )
        with f2:
            role_filter = st.multiselect(
                "Filter by Roles:",
                ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
            )
        with f3:
            min_matches = st.number_input("Minimum matches played:", min_value=0, value=0)

    if st.button("📊 Load and Analyze Data", use_container_width=True):
        try:
            if table_name == "players":
                query = (
                    """
                    SELECT player_id AS ID,
                           name AS `Player Name`,
                           country AS Country,
                           playing_role AS Role,
                           batting_style AS `Batting Style`,
                           bowling_style AS `Bowling Style`,
                           total_runs AS Runs,
                           total_wickets AS Wickets,
                           batting_average AS `Bat Avg`,
                           bowling_average AS `Bowl Avg`,
                           strike_rate AS `Strike Rate`,
                           economy_rate AS Economy,
                           centuries AS `100s`,
                           fifties AS `50s`,
                           matches_played AS Matches
                    FROM players
                    WHERE 1=1
                    """
                )
                if country_filter:
                    placeholders = ", ".join(["%s"] * len(country_filter))
                    query += f" AND country IN ({placeholders})"
                if role_filter:
                    placeholders_r = ", ".join(["%s"] * len(role_filter))
                    query += f" AND playing_role IN ({placeholders_r})"
                if min_matches > 0:
                    query += " AND matches_played >= %s"
                query += f" ORDER BY player_id {sort_direction} LIMIT %s"

                params = tuple(country_filter) + tuple(role_filter) + (
                    min_matches,
                ) if min_matches > 0 else tuple(country_filter) + tuple(role_filter)
                # append limit
                params = params + (limit,)

                df = db_connection.execute_query(query, params)

            elif table_name == "teams":
                df = db_connection.execute_query(
                    f"""
                    SELECT team_id AS ID,
                           team_name AS `Team Name`,
                           country AS Country,
                           matches_played AS Matches,
                           matches_won AS Wins,
                           matches_lost AS Losses,
                           win_percentage AS `Win %`
                    FROM teams
                    ORDER BY team_id {sort_direction}
                    LIMIT %s
                    """,
                    (limit,),
                )
            elif table_name == "venues":
                df = db_connection.execute_query(
                    f"""
                    SELECT venue_id AS ID,
                           venue_name AS `Venue Name`,
                           city AS City,
                           country AS Country,
                           capacity AS Capacity,
                           established_year AS `Est. Year`
                    FROM venues
                    ORDER BY venue_id {sort_direction}
                    LIMIT %s
                    """,
                    (limit,),
                )
            else:  # matches
                df = db_connection.execute_query(
                    f"""
                    SELECT m.match_id AS ID,
                           m.match_description AS `Match Description`,
                           t1.team_name AS `Team 1`,
                           t2.team_name AS `Team 2`,
                           v.venue_name AS Venue,
                           m.match_date AS Date,
                           m.match_format AS Format,
                           m.status AS Status,
                           m.winning_team AS Winner,
                           m.victory_margin AS `Victory Margin`
                    FROM matches m
                    LEFT JOIN teams t1 ON m.team1_id = t1.team_id
                    LEFT JOIN teams t2 ON m.team2_id = t2.team_id
                    LEFT JOIN venues v ON m.venue_id = v.venue_id
                    ORDER BY m.match_id {sort_direction}
                    LIMIT %s
                    """,
                    (limit,),
                )

            if df is None or df.empty:
                st.warning("No data found.")
                return

            st.success(f"✅ Loaded {len(df)} records from {selected_table_label}")
            # Display with simple formatting
            st.dataframe(df, use_container_width=True)

            st.markdown("### 📈 Quick Data Analysis")
            c1, c2, c3 = st.columns(3)
            with c1:
                csv = df.to_csv(index=False)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label=f"📥 Export {table_name}",
                    data=csv,
                    file_name=f"{table_name}_{timestamp}.csv",
                    mime="text/csv",
                )
            with c2:
                if st.button("📊 Show Statistics"):
                    show_data_statistics(df)
            with c3:
                if len(df.select_dtypes(include=["number"]).columns) > 0 and st.button("📈 Visualize Data"):
                    create_data_visualization(df, table_name)
        except Exception as e:
            st.error(f"Error loading data: {e}")

# =========================================
# CREATE
# =========================================
def show_create_operations(db_connection):
    st.markdown("## ➕ Add New Records to Database")
    record_type = st.selectbox("Select record type to add:", ["Player", "Team", "Venue", "Match"])
    if record_type == "Player":
        show_add_player_form(db_connection)
    elif record_type == "Team":
        show_add_team_form(db_connection)
    elif record_type == "Venue":
        show_add_venue_form(db_connection)
    else:
        show_add_match_form(db_connection)

# ----- Player -----
def show_add_player_form(db_connection):
    st.markdown("### 🧑‍🚀 Add Player")
    with st.form("add_player_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Name*")
            country = st.text_input("Country*")
            role = st.selectbox("Role*", ["", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        with c2:
            batting_style = st.text_input("Batting Style", placeholder="Right-hand bat")
            bowling_style = st.text_input("Bowling Style", placeholder="Right-arm offbreak")
            matches_played = st.number_input("Matches Played", min_value=0, value=0)
        with c3:
            total_runs = st.number_input("Total Runs", min_value=0, value=0)
            total_wickets = st.number_input("Total Wickets", min_value=0, value=0)
            centuries = st.number_input("Centuries (100s)", min_value=0, value=0)
            fifties = st.number_input("Fifties (50s)", min_value=0, value=0)

        c4, c5, c6 = st.columns(3)
        with c4:
            batting_average = st.number_input("Batting Average", min_value=0.0, value=0.0)
        with c5:
            bowling_average = st.number_input("Bowling Average", min_value=0.0, value=0.0)
        with c6:
            strike_rate = st.number_input("Strike Rate", min_value=0.0, value=0.0)
        economy_rate = st.number_input("Economy Rate", min_value=0.0, value=0.0)

        submitted = st.form_submit_button("➕ Add Player")
        if submitted:
            if not (name and country and role):
                st.error("Please fill required fields marked with *")
                return
            try:
                ok = db_connection.execute_update(
                    """
                    INSERT INTO players
                    (name, country, playing_role, batting_style, bowling_style,
                     total_runs, total_wickets, batting_average, bowling_average,
                     strike_rate, economy_rate, centuries, fifties, matches_played)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        name,
                        country,
                        role,
                        batting_style,
                        bowling_style,
                        int(total_runs),
                        int(total_wickets),
                        float(batting_average),
                        float(bowling_average),
                        float(strike_rate),
                        float(economy_rate),
                        int(centuries),
                        int(fifties),
                        int(matches_played),
                    ),
                )
                st.success(f"✅ Player '{name}' added successfully!" if ok else "❌ Failed to add player")
            except Exception as e:
                st.error(f"❌ Error adding player: {e}")

# ----- Team -----
def show_add_team_form(db_connection):
    st.markdown("### 🏏 Add Team")
    with st.form("add_team_form"):
        c1, c2 = st.columns(2)
        with c1:
            team_name = st.text_input("Team Name*")
            country = st.text_input("Country*")
        with c2:
            matches_played = st.number_input("Matches Played", min_value=0, value=0)
            matches_won = st.number_input("Matches Won", min_value=0, value=0)
            matches_lost = st.number_input("Matches Lost", min_value=0, value=0)
        submitted = st.form_submit_button("➕ Add Team")
        if submitted:
            if not (team_name and country):
                st.error("Please fill required fields marked with *")
                return
            try:
                win_pct = 0.0
                if matches_played > 0:
                    win_pct = round((matches_won / max(matches_played, 1)) * 100, 2)
                ok = db_connection.execute_update(
                    """
                    INSERT INTO teams
                    (team_name, country, matches_played, matches_won, matches_lost, win_percentage)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        team_name,
                        country,
                        int(matches_played),
                        int(matches_won),
                        int(matches_lost),
                        float(win_pct),
                    ),
                )
                st.success(f"✅ Team '{team_name}' added successfully!" if ok else "❌ Failed to add team")
            except Exception as e:
                st.error(f"❌ Error adding team: {e}")

# ----- Venue -----
def show_add_venue_form(db_connection):
    st.markdown("### 🏟️ Add Venue")
    with st.form("add_venue_form"):
        c1, c2 = st.columns(2)
        with c1:
            venue_name = st.text_input("Venue Name*")
            city = st.text_input("City*")
            country = st.text_input("Country*")
        with c2:
            capacity = st.number_input("Seating Capacity", min_value=0, value=0)
            established_year = st.number_input("Established Year", min_value=1800, max_value=date.today().year, value=2000)
        submitted = st.form_submit_button("➕ Add Venue")
        if submitted:
            if not (venue_name and city and country):
                st.error("Please fill required fields marked with *")
                return
            try:
                ok = db_connection.execute_update(
                    """
                    INSERT INTO venues (venue_name, city, country, capacity, established_year)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (venue_name, city, country, int(capacity), int(established_year)),
                )
                st.success(f"✅ Venue '{venue_name}' added successfully!" if ok else "❌ Failed to add venue")
            except Exception as e:
                st.error(f"❌ Error adding venue: {e}")

# ----- Match -----
def show_add_match_form(db_connection):
    st.markdown("### 🧾 Add Match")

    # lookup helpers
    teams_df = db_connection.execute_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
    venues_df = db_connection.execute_query("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")

    team_options = {"": None}
    if teams_df is not None and not teams_df.empty:
        team_options.update({row["team_name"]: int(row["team_id"]) for _, row in teams_df.iterrows()})
    venue_options = {"": None}
    if venues_df is not None and not venues_df.empty:
        venue_options.update({row["venue_name"]: int(row["venue_id"]) for _, row in venues_df.iterrows()})

    with st.form("add_match_form"):
        c1, c2 = st.columns(2)
        with c1:
            match_description = st.text_input("Match Description*", placeholder="India vs Australia - 1st Test")
            match_format = st.selectbox("Match Format*", ["", "Test", "ODI", "T20I", "T20"]) 
            match_date = st.date_input("Match Date", value=date.today())
        with c2:
            team1 = st.selectbox("Team 1*", list(team_options.keys()))
            team2 = st.selectbox("Team 2*", list(team_options.keys()))
            venue = st.selectbox("Venue*", list(venue_options.keys()))
        submitted = st.form_submit_button("➕ Add Match")
        if submitted:
            if not (match_description and match_format and team1 and team2 and venue):
                st.error("Please fill required fields marked with *")
                return
            if team1 == team2:
                st.error("Team 1 and Team 2 must be different")
                return
            try:
                ok = db_connection.execute_update(
                    """
                    INSERT INTO matches
                    (match_description, team1_id, team2_id, venue_id, match_date, match_format, status, winning_team, victory_margin)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        match_description,
                        team_options[team1],
                        team_options[team2],
                        venue_options[venue],
                        match_date,
                        match_format,
                        "Scheduled",
                        None,
                        None,
                    ),
                )
                st.success("✅ Match added successfully!" if ok else "❌ Failed to add match")
            except Exception as e:
                st.error(f"❌ Error adding match: {e}")

# =========================================
# UPDATE
# =========================================
def show_update_operations(db_connection):
    st.markdown("## ✏️ Edit Records")
    entity = st.selectbox("Select type to edit:", ["Player", "Team", "Venue", "Match"])
    if entity == "Player":
        edit_player(db_connection)
    elif entity == "Team":
        edit_team(db_connection)
    elif entity == "Venue":
        edit_venue(db_connection)
    else:
        edit_match(db_connection)

# --- Edit helpers ---
def _select_row(df: pd.DataFrame, label_col: str, id_col: str, label: str):
    if df is None or df.empty:
        st.warning(f"No {label}s available.")
        return None
    options = {row[label_col]: row[id_col] for _, row in df.iterrows()}
    key = st.selectbox(f"Select {label}:", list(options.keys()))
    return options[key]

# Player edit
def edit_player(db_connection):
    st.markdown("### Edit Player")
    df = db_connection.execute_query("SELECT * FROM players ORDER BY name")
    player_id = _select_row(df, "name", "player_id", "Player")
    if not player_id:
        return
    details = db_connection.execute_query("SELECT * FROM players WHERE player_id=%s", (int(player_id),))
    row = details.iloc[0]
    with st.form("edit_player_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Name", value=row["name"])
            country = st.text_input("Country", value=row["country"])
            role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"], index=0 if row["playing_role"] not in ["Batsman","Bowler","All-rounder","Wicket-keeper"] else ["Batsman","Bowler","All-rounder","Wicket-keeper"].index(row["playing_role"]))
        with c2:
            batting_style = st.text_input("Batting Style", value=row.get("batting_style", ""))
            bowling_style = st.text_input("Bowling Style", value=row.get("bowling_style", ""))
            matches_played = st.number_input("Matches Played", min_value=0, value=int(row.get("matches_played", 0)))
        with c3:
            total_runs = st.number_input("Total Runs", min_value=0, value=int(row.get("total_runs", 0)))
            total_wickets = st.number_input("Total Wickets", min_value=0, value=int(row.get("total_wickets", 0)))
            centuries = st.number_input("Centuries", min_value=0, value=int(row.get("centuries", 0)))
            fifties = st.number_input("Fifties", min_value=0, value=int(row.get("fifties", 0)))

        c4, c5, c6 = st.columns(3)
        with c4:
            batting_average = st.number_input("Batting Average", min_value=0.0, value=float(row.get("batting_average", 0.0)))
        with c5:
            bowling_average = st.number_input("Bowling Average", min_value=0.0, value=float(row.get("bowling_average", 0.0)))
        with c6:
            strike_rate = st.number_input("Strike Rate", min_value=0.0, value=float(row.get("strike_rate", 0.0)))
        economy_rate = st.number_input("Economy Rate", min_value=0.0, value=float(row.get("economy_rate", 0.0)))

        if st.form_submit_button("💾 Save Player"):
            try:
                ok = db_connection.execute_update(
                    """
                    UPDATE players SET
                        name=%s, country=%s, playing_role=%s, batting_style=%s, bowling_style=%s,
                        total_runs=%s, total_wickets=%s, batting_average=%s, bowling_average=%s,
                        strike_rate=%s, economy_rate=%s, centuries=%s, fifties=%s, matches_played=%s
                    WHERE player_id=%s
                    """,
                    (
                        name,
                        country,
                        role,
                        batting_style,
                        bowling_style,
                        int(total_runs),
                        int(total_wickets),
                        float(batting_average),
                        float(bowling_average),
                        float(strike_rate),
                        float(economy_rate),
                        int(centuries),
                        int(fifties),
                        int(matches_played),
                        int(player_id),
                    ),
                )
                st.success("✅ Player updated" if ok else "❌ Update failed")
            except Exception as e:
                st.error(f"❌ Error updating player: {e}")

# Team edit
def edit_team(db_connection):
    st.markdown("### Edit Team")
    df = db_connection.execute_query("SELECT * FROM teams ORDER BY team_name")
    team_id = _select_row(df, "team_name", "team_id", "Team")
    if not team_id:
        return
    row = db_connection.execute_query("SELECT * FROM teams WHERE team_id=%s", (int(team_id),)).iloc[0]
    with st.form("edit_team_form"):
        c1, c2 = st.columns(2)
        with c1:
            team_name = st.text_input("Team Name", value=row["team_name"]) 
            country = st.text_input("Country", value=row["country"]) 
        with c2:
            matches_played = st.number_input("Matches Played", min_value=0, value=int(row.get("matches_played", 0)))
            matches_won = st.number_input("Matches Won", min_value=0, value=int(row.get("matches_won", 0)))
            matches_lost = st.number_input("Matches Lost", min_value=0, value=int(row.get("matches_lost", 0)))
        if st.form_submit_button("💾 Save Team"):
            try:
                win_pct = 0.0
                if matches_played > 0:
                    win_pct = round((matches_won / max(matches_played, 1)) * 100, 2)
                ok = db_connection.execute_update(
                    """
                    UPDATE teams SET team_name=%s, country=%s, matches_played=%s,
                                     matches_won=%s, matches_lost=%s, win_percentage=%s
                    WHERE team_id=%s
                    """,
                    (
                        team_name,
                        country,
                        int(matches_played),
                        int(matches_won),
                        int(matches_lost),
                        float(win_pct),
                        int(team_id),
                    ),
                )
                st.success("✅ Team updated" if ok else "❌ Update failed")
            except Exception as e:
                st.error(f"❌ Error updating team: {e}")

# Venue edit
def edit_venue(db_connection):
    st.markdown("### Edit Venue")
    df = db_connection.execute_query("SELECT * FROM venues ORDER BY venue_name")
    venue_id = _select_row(df, "venue_name", "venue_id", "Venue")
    if not venue_id:
        return
    row = db_connection.execute_query("SELECT * FROM venues WHERE venue_id=%s", (int(venue_id),)).iloc[0]
    with st.form("edit_venue_form"):
        c1, c2 = st.columns(2)
        with c1:
            venue_name = st.text_input("Venue Name", value=row["venue_name"]) 
            city = st.text_input("City", value=row["city"]) 
            country = st.text_input("Country", value=row["country"]) 
        with c2:
            capacity = st.number_input("Seating Capacity", min_value=0, value=int(row.get("capacity", 0)))
            established_year = st.number_input(
                "Established Year", min_value=1800, max_value=date.today().year, value=int(row.get("established_year", 2000))
            )
        if st.form_submit_button("💾 Save Venue"):
            try:
                ok = db_connection.execute_update(
                    """
                    UPDATE venues SET venue_name=%s, city=%s, country=%s, capacity=%s, established_year=%s
                    WHERE venue_id=%s
                    """,
                    (
                        venue_name,
                        city,
                        country,
                        int(capacity),
                        int(established_year),
                        int(venue_id),
                    ),
                )
                st.success("✅ Venue updated" if ok else "❌ Update failed")
            except Exception as e:
                st.error(f"❌ Error updating venue: {e}")

# Match edit
def edit_match(db_connection):
    st.markdown("### Edit Match")
    df = db_connection.execute_query("SELECT match_id, match_description FROM matches ORDER BY match_id DESC")
    match_id = _select_row(df, "match_description", "match_id", "Match")
    if not match_id:
        return

    row = db_connection.execute_query("SELECT * FROM matches WHERE match_id=%s", (int(match_id),)).iloc[0]
    teams_df = db_connection.execute_query("SELECT team_id, team_name FROM teams ORDER BY team_name")
    venues_df = db_connection.execute_query("SELECT venue_id, venue_name FROM venues ORDER BY venue_name")
    team_options = {row2["team_name"]: int(row2["team_id"]) for _, row2 in teams_df.iterrows()} if teams_df is not None and not teams_df.empty else {}
    venue_options = {row2["venue_name"]: int(row2["venue_id"]) for _, row2 in venues_df.iterrows()} if venues_df is not None and not venues_df.empty else {}

    def _reverse_lookup(d, value):
        for k, v in d.items():
            if v == value:
                return k
        return list(d.keys())[0] if d else ""

    with st.form("edit_match_form"):
        c1, c2 = st.columns(2)
        with c1:
            match_description = st.text_input("Match Description", value=row.get("match_description", ""))
            match_format = st.selectbox("Match Format", ["Test", "ODI", "T20I", "T20"], index=0)
            match_date = st.date_input("Match Date", value=row.get("match_date", date.today()))
            status = st.selectbox("Status", ["Scheduled", "Completed", "Abandoned"], index=0)
        with c2:
            team1 = st.selectbox("Team 1", list(team_options.keys()), index=max(0, list(team_options.keys()).index(_reverse_lookup(team_options, row.get("team1_id"))))) if team_options else st.selectbox("Team 1", [""])
            team2 = st.selectbox("Team 2", list(team_options.keys()), index=max(0, list(team_options.keys()).index(_reverse_lookup(team_options, row.get("team2_id"))))) if team_options else st.selectbox("Team 2", [""])
            venue = st.selectbox("Venue", list(venue_options.keys()), index=max(0, list(venue_options.keys()).index(_reverse_lookup(venue_options, row.get("venue_id"))))) if venue_options else st.selectbox("Venue", [""])
            winning_team = st.text_input("Winning Team", value=row.get("winning_team", ""))
            victory_margin = st.text_input("Victory Margin", value=row.get("victory_margin", ""))

        if st.form_submit_button("💾 Save Match"):
            if team1 == team2:
                st.error("Team 1 and Team 2 must be different")
                return
            try:
                ok = db_connection.execute_update(
                    """
                    UPDATE matches SET
                        match_description=%s, team1_id=%s, team2_id=%s, venue_id=%s,
                        match_date=%s, match_format=%s, status=%s, winning_team=%s, victory_margin=%s
                    WHERE match_id=%s
                    """,
                    (
                        match_description,
                        team_options.get(team1),
                        team_options.get(team2),
                        venue_options.get(venue),
                        match_date,
                        match_format,
                        status,
                        (winning_team or None),
                        (victory_margin or None),
                        int(match_id),
                    ),
                )
                st.success("✅ Match updated" if ok else "❌ Update failed")
            except Exception as e:
                st.error(f"❌ Error updating match: {e}")

# =========================================
# DELETE
# =========================================
def show_delete_operations(db_connection):
    st.markdown("## 🗑️ Delete Records (Careful)")
    entity = st.selectbox("Select type to delete:", ["Player", "Team", "Venue", "Match"])

    if entity == "Player":
        _delete_entity(db_connection, "players", "player_id", "name", "Player")
    elif entity == "Team":
        _delete_entity(db_connection, "teams", "team_id", "team_name", "Team")
    elif entity == "Venue":
        _delete_entity(db_connection, "venues", "venue_id", "venue_name", "Venue")
    else:
        _delete_entity(db_connection, "matches", "match_id", "match_description", "Match")


def _delete_entity(db_connection, table: str, id_col: str, label_col: str, label: str):
    df = db_connection.execute_query(f"SELECT {id_col}, {label_col} FROM {table} ORDER BY 1 DESC")
    if df is None or df.empty:
        st.warning(f"No {label}s to delete.")
        return
    options = {f"{row[label_col]} (ID {row[id_col]})": int(row[id_col]) for _, row in df.iterrows()}
    choice = st.selectbox(f"Select {label} to delete:", list(options.keys()))
    chosen_id = options[choice]

    with st.expander("Preview record"):
        preview = db_connection.execute_query(f"SELECT * FROM {table} WHERE {id_col}=%s", (chosen_id,))
        st.dataframe(preview, use_container_width=True)

    confirm1 = st.checkbox("I understand this action is permanent.")
    confirm_text = st.text_input(f"Type the {label} ID to confirm deletion")

    if st.button("🚨 Delete", type="primary", use_container_width=True):
        if not confirm1 or confirm_text.strip() != str(chosen_id):
            st.error("Confirmation failed. Type the correct ID and check the box.")
            return
        try:
            ok = db_connection.execute_update(f"DELETE FROM {table} WHERE {id_col}=%s", (chosen_id,))
            st.success("✅ Deleted" if ok else "❌ Delete failed")
        except Exception as e:
            st.error(f"❌ Error deleting: {e}")

# =========================================
# BULK OPS
# =========================================
def show_bulk_operations(db_connection):
    st.markdown("## 📊 Bulk Operations")
    st.markdown("Export or import data in bulk. (Import is CSV-based; extend as needed)")

    st.subheader("Export Tables")
    table_flags = {
        "players": st.checkbox("Players", value=True),
        "teams": st.checkbox("Teams", value=True),
        "venues": st.checkbox("Venues", value=True),
        "matches": st.checkbox("Matches", value=False),
    }
    if st.button("📥 Export Selected as CSVs"):
        try:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            for t, enabled in table_flags.items():
                if not enabled:
                    continue
                df = db_connection.execute_query(f"SELECT * FROM {t}")
                if df is None or df.empty:
                    continue
                st.download_button(
                    label=f"Download {t}.csv",
                    data=df.to_csv(index=False),
                    file_name=f"{t}_{now}.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"Export failed: {e}")

    st.divider()
    st.subheader("Import CSV (single table)")
    table_for_import = st.selectbox("Target table", ["players", "teams", "venues"])
    uploaded = st.file_uploader("Upload CSV", type=["csv"]) 
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.write("Preview:")
            st.dataframe(df.head(20), use_container_width=True)
            if st.button("⬆️ Import Now"):
                inserted = 0
                if table_for_import == "players":
                    required = {"name", "country", "playing_role"}
                    if not required.issubset(df.columns):
                        st.error(f"CSV missing required columns: {required}")
                        return
                    for _, r in df.iterrows():
                        ok = db_connection.execute_update(
                            """
                            INSERT INTO players(name, country, playing_role, batting_style, bowling_style,
                                total_runs, total_wickets, batting_average, bowling_average,
                                strike_rate, economy_rate, centuries, fifties, matches_played)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            (
                                r.get("name"), r.get("country"), r.get("playing_role"),
                                r.get("batting_style"), r.get("bowling_style"),
                                int(r.get("total_runs", 0) or 0),
                                int(r.get("total_wickets", 0) or 0),
                                float(r.get("batting_average", 0.0) or 0.0),
                                float(r.get("bowling_average", 0.0) or 0.0),
                                float(r.get("strike_rate", 0.0) or 0.0),
                                float(r.get("economy_rate", 0.0) or 0.0),
                                int(r.get("centuries", 0) or 0),
                                int(r.get("fifties", 0) or 0),
                                int(r.get("matches_played", 0) or 0),
                            ),
                        )
                        inserted += 1 if ok else 0
                elif table_for_import == "teams":
                    required = {"team_name", "country"}
                    if not required.issubset(df.columns):
                        st.error(f"CSV missing required columns: {required}")
                        return
                    for _, r in df.iterrows():
                        mp = int(r.get("matches_played", 0) or 0)
                        mw = int(r.get("matches_won", 0) or 0)
                        wl = int(r.get("matches_lost", 0) or 0)
                        wp = round((mw / max(mp, 1)) * 100, 2) if mp > 0 else 0.0
                        ok = db_connection.execute_update(
                            """
                            INSERT INTO teams(team_name, country, matches_played, matches_won, matches_lost, win_percentage)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            """,
                            (r.get("team_name"), r.get("country"), mp, mw, wl, wp),
                        )
                        inserted += 1 if ok else 0
                else:  # venues
                    required = {"venue_name", "city", "country"}
                    if not required.issubset(df.columns):
                        st.error(f"CSV missing required columns: {required}")
                        return
                    for _, r in df.iterrows():
                        ok = db_connection.execute_update(
                            """
                            INSERT INTO venues(venue_name, city, country, capacity, established_year)
                            VALUES (%s,%s,%s,%s,%s)
                            """,
                            (
                                r.get("venue_name"),
                                r.get("city"),
                                r.get("country"),
                                int(r.get("capacity", 0) or 0),
                                int(r.get("established_year", 2000) or 2000),
                            ),
                        )
                        inserted += 1 if ok else 0
                st.success(f"✅ Imported {inserted} records into {table_for_import}")
        except Exception as e:
            st.error(f"Import failed: {e}")

# =========================================
# DB TOOLS / UTILITIES
# =========================================
def show_database_tools(db_connection):
    st.markdown("## 🔧 Database Tools")

    st.subheader("Record Counts")
    counts = {}
    for t in ["players", "teams", "venues", "matches"]:
        try:
            df = db_connection.execute_query(f"SELECT COUNT(*) AS cnt FROM {t}")
            counts[t] = int(df.iloc[0]["cnt"]) if df is not None and not df.empty else 0
        except Exception:
            counts[t] = 0
    st.write(counts)

    st.subheader("Quick Checks")
    if st.button("Check Foreign Keys (matches -> teams/venues)"):
        try:
            df = db_connection.execute_query(
                """
                SELECT m.match_id, m.team1_id, m.team2_id, m.venue_id
                FROM matches m
                LEFT JOIN teams t1 ON m.team1_id = t1.team_id
                LEFT JOIN teams t2 ON m.team2_id = t2.team_id
                LEFT JOIN venues v ON m.venue_id = v.venue_id
                WHERE t1.team_id IS NULL OR t2.team_id IS NULL OR v.venue_id IS NULL
                """
            )
            if df is None or df.empty:
                st.success("All foreign keys look valid ✔️")
            else:
                st.warning("Some matches have missing references:")
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Check failed: {e}")

# =========================================
# HELPERS
# =========================================
def show_data_statistics(df: pd.DataFrame):
    st.markdown("#### Data Statistics")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Records", len(df))
    with c2:
        st.metric("Total Fields", len(df.columns))
    with c3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    numeric_df = df.select_dtypes(include=["number"])
    if not numeric_df.empty:
        st.markdown("**Numeric Data Summary:**")
        st.dataframe(numeric_df.describe(), use_container_width=True)


def create_data_visualization(df: pd.DataFrame, table_name: str):
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if not len(numeric_cols):
        st.info("No numeric columns to visualize.")
        return
    viz_col = st.selectbox("Select column to visualize:", list(numeric_cols))
    fig = px.histogram(df, x=viz_col, title=f"{table_name} — {viz_col} Distribution")
    st.plotly_chart(fig, use_container_width=True)
