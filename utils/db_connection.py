"""
MySQL Database connection and operations for Cricbuzz LiveStats
This module handles all MySQL database connectivity and operations
"""

import mysql.connector
import pandas as pd
import os
from typing import Optional, List, Dict, Any
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        """Initialize MySQL database connection"""
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'cricket_user'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'cricket_stats'),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True
        }
        self.init_database()
    
    def get_connection(self):
        """Get MySQL database connection"""
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            st.error(f"MySQL connection error: {e}")
            return None
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Create players table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    player_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    country VARCHAR(100),
                    playing_role VARCHAR(100),
                    batting_style VARCHAR(100),
                    bowling_style VARCHAR(100),
                    total_runs INT DEFAULT 0,
                    total_wickets INT DEFAULT 0,
                    batting_average DECIMAL(5,2) DEFAULT 0.0,
                    bowling_average DECIMAL(5,2) DEFAULT 0.0,
                    strike_rate DECIMAL(5,2) DEFAULT 0.0,
                    economy_rate DECIMAL(4,2) DEFAULT 0.0,
                    centuries INT DEFAULT 0,
                    fifties INT DEFAULT 0,
                    matches_played INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_name (name),
                    INDEX idx_country (country),
                    INDEX idx_role (playing_role)
                )
            ''')
            
            # Create teams table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    team_id INT AUTO_INCREMENT PRIMARY KEY,
                    team_name VARCHAR(255) NOT NULL UNIQUE,
                    country VARCHAR(100),
                    matches_played INT DEFAULT 0,
                    matches_won INT DEFAULT 0,
                    matches_lost INT DEFAULT 0,
                    win_percentage DECIMAL(5,2) DEFAULT 0.0,
                    INDEX idx_team_name (team_name)
                )
            ''')
            
            # Create venues table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS venues (
                    venue_id INT AUTO_INCREMENT PRIMARY KEY,
                    venue_name VARCHAR(255) NOT NULL,
                    city VARCHAR(100),
                    country VARCHAR(100),
                    capacity INT,
                    established_year INT,
                    INDEX idx_venue_name (venue_name),
                    INDEX idx_country (country)
                )
            ''')
            
            # Create matches table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    match_id INT AUTO_INCREMENT PRIMARY KEY,
                    cricbuzz_match_id INT UNIQUE,
                    match_description TEXT,
                    team1_id INT,
                    team2_id INT,
                    venue_id INT,
                    match_date DATE,
                    match_format VARCHAR(50),
                    toss_winner VARCHAR(255),
                    toss_decision VARCHAR(50),
                    winning_team VARCHAR(255),
                    victory_margin VARCHAR(100),
                    match_status VARCHAR(50),
                    series_name VARCHAR(255),
                    current_status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
                    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
                    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
                    INDEX idx_match_date (match_date),
                    INDEX idx_format (match_format),
                    INDEX idx_status (match_status)
                )
            ''')
            
            cursor.close()
            
            # Insert sample data if tables are empty
            self.insert_initial_data()
            
        except mysql.connector.Error as e:
            st.error(f"Database initialization error: {e}")
        finally:
            if conn.is_connected():
                conn.close()
    
    def insert_initial_data(self):
        """Insert initial sample data"""
        conn = self.get_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Check if data exists
            cursor.execute("SELECT COUNT(*) FROM players")
            if cursor.fetchone()[0] > 0:
                cursor.close()
                return
            
            # Insert sample teams first
            teams_data = [
                ('India', 'India', 150, 85, 65, 56.7),
                ('Australia', 'Australia', 140, 78, 62, 55.7),
                ('England', 'England', 130, 72, 58, 55.4),
                ('Pakistan', 'Pakistan', 125, 68, 57, 54.4),
                ('New Zealand', 'New Zealand', 120, 65, 55, 54.2),
                ('South Africa', 'South Africa', 115, 62, 53, 53.9),
                ('West Indies', 'West Indies', 110, 58, 52, 52.7),
                ('Sri Lanka', 'Sri Lanka', 105, 55, 50, 52.4)
            ]
            
            cursor.executemany('''
                INSERT INTO teams (team_name, country, matches_played, matches_won, matches_lost, win_percentage)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', teams_data)
            
            # Insert sample venues
            venues_data = [
                ('Wankhede Stadium', 'Mumbai', 'India', 33108, 1974),
                ('Lord\'s', 'London', 'England', 30000, 1814),
                ('MCG', 'Melbourne', 'Australia', 100024, 1853),
                ('Eden Gardens', 'Kolkata', 'India', 66000, 1864),
                ('The Oval', 'London', 'England', 25000, 1845),
                ('SCG', 'Sydney', 'Australia', 48000, 1848),
                ('Old Trafford', 'Manchester', 'England', 26000, 1857),
                ('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000, 1959)
            ]
            
            cursor.executemany('''
                INSERT INTO venues (venue_name, city, country, capacity, established_year)
                VALUES (%s, %s, %s, %s, %s)
            ''', venues_data)
            
            # Insert sample players
            players_data = [
                ('Virat Kohli', 'India', 'Batsman', 'Right-handed', 'Right-arm medium', 15000, 4, 50.5, 25.0, 92.5, 6.5, 50, 65, 250),
                ('Rohit Sharma', 'India', 'Batsman', 'Right-handed', 'Right-arm off-break', 14000, 8, 48.8, 30.2, 88.2, 5.8, 45, 70, 240),
                ('Jasprit Bumrah', 'India', 'Bowler', 'Right-handed', 'Right-arm fast', 800, 150, 15.5, 22.8, 85.4, 4.2, 0, 2, 120),
                ('Babar Azam', 'Pakistan', 'Batsman', 'Right-handed', 'Right-arm off-break', 12000, 2, 52.2, 40.0, 86.8, 5.5, 35, 55, 200),
                ('Kane Williamson', 'New Zealand', 'Batsman', 'Right-handed', 'Right-arm off-break', 11500, 5, 49.8, 35.6, 78.5, 4.8, 28, 62, 180),
                ('Steve Smith', 'Australia', 'Batsman', 'Right-handed', 'Right-arm leg-break', 13000, 12, 51.2, 28.4, 82.1, 5.2, 42, 58, 220),
                ('Pat Cummins', 'Australia', 'Bowler', 'Right-handed', 'Right-arm fast', 1200, 180, 18.2, 21.5, 95.2, 4.8, 1, 5, 150),
                ('Ben Stokes', 'England', 'All-rounder', 'Left-handed', 'Right-arm fast-medium', 8500, 95, 38.5, 28.8, 85.6, 5.1, 15, 45, 180),
                ('Trent Boult', 'New Zealand', 'Bowler', 'Left-handed', 'Left-arm fast-medium', 900, 165, 16.8, 24.2, 88.5, 4.6, 0, 3, 140),
                ('David Warner', 'Australia', 'Batsman', 'Left-handed', '', 12500, 0, 44.8, 0, 92.8, 0, 38, 68, 210)
            ]
            
            cursor.executemany('''
                INSERT INTO players (name, country, playing_role, batting_style, bowling_style, 
                                   total_runs, total_wickets, batting_average, bowling_average, 
                                   strike_rate, economy_rate, centuries, fifties, matches_played)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', players_data)
            
            conn.commit()
            cursor.close()
            
        except mysql.connector.Error as e:
            st.error(f"Error inserting initial data: {e}")
        finally:
            if conn.is_connected():
                conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Execute SELECT query and return DataFrame"""
        conn = self.get_connection()
        if not conn:
            return pd.DataFrame()
        
        try:
            if params:
                df = pd.read_sql(query, conn, params=params)
            else:
                df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            st.error(f"Query execution error: {e}")
            return pd.DataFrame()
        finally:
            if conn.is_connected():
                conn.close()
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute INSERT/UPDATE/DELETE query"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            st.error(f"Update query error: {e}")
            return False
        finally:
            if conn.is_connected():
                conn.close()
    
    def get_table_data(self, table_name: str, limit: int = 100) -> pd.DataFrame:
        """Get all data from a specific table"""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def get_player_by_id(self, player_id: int) -> dict:
        """Get player details by ID"""
        query = "SELECT * FROM players WHERE player_id = %s"
        df = self.execute_query(query, (player_id,))
        if not df.empty:
            return df.iloc[0].to_dict()
        return {}
    
    def add_player(self, player_data: dict) -> bool:
        """Add new player to database"""
        query = '''
            INSERT INTO players (name, country, playing_role, batting_style, bowling_style,
                               total_runs, total_wickets, batting_average, bowling_average,
                               strike_rate, economy_rate, centuries, fifties, matches_played)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (
            player_data.get('name', ''),
            player_data.get('country', ''),
            player_data.get('playing_role', ''),
            player_data.get('batting_style', ''),
            player_data.get('bowling_style', ''),
            player_data.get('total_runs', 0),
            player_data.get('total_wickets', 0),
            player_data.get('batting_average', 0.0),
            player_data.get('bowling_average', 0.0),
            player_data.get('strike_rate', 0.0),
            player_data.get('economy_rate', 0.0),
            player_data.get('centuries', 0),
            player_data.get('fifties', 0),
            player_data.get('matches_played', 0)
        )
        return self.execute_update(query, params)
    
    def update_player(self, player_id: int, player_data: dict) -> bool:
        """Update existing player data"""
        query = '''
            UPDATE players SET 
                name=%s, country=%s, playing_role=%s, batting_style=%s, bowling_style=%s,
                total_runs=%s, total_wickets=%s, batting_average=%s, bowling_average=%s,
                strike_rate=%s, economy_rate=%s, centuries=%s, fifties=%s, matches_played=%s
            WHERE player_id=%s
        '''
        params = (
            player_data.get('name', ''),
            player_data.get('country', ''),
            player_data.get('playing_role', ''),
            player_data.get('batting_style', ''),
            player_data.get('bowling_style', ''),
            player_data.get('total_runs', 0),
            player_data.get('total_wickets', 0),
            player_data.get('batting_average', 0.0),
            player_data.get('bowling_average', 0.0),
            player_data.get('strike_rate', 0.0),
            player_data.get('economy_rate', 0.0),
            player_data.get('centuries', 0),
            player_data.get('fifties', 0),
            player_data.get('matches_played', 0),
            player_id
        )
        return self.execute_update(query, params)
    
    def delete_player(self, player_id: int) -> bool:
        """Delete player from database"""
        query = "DELETE FROM players WHERE player_id = %s"
        return self.execute_update(query, (player_id,))
    
    def insert_real_match_data(self, match_data: dict) -> bool:
        """Insert real match data from API"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Insert match data
            match_query = '''
                INSERT INTO matches (cricbuzz_match_id, match_description, match_format, 
                                   match_date, series_name, current_status, match_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                current_status = VALUES(current_status),
                match_status = VALUES(match_status)
            '''
            
            params = (
                match_data.get('match_id'),
                match_data.get('description', ''),
                match_data.get('format', ''),
                match_data.get('date', '2024-08-29'),
                match_data.get('series', ''),
                match_data.get('status', ''),
                match_data.get('state', 'Unknown')
            )
            
            cursor.execute(match_query, params)
            conn.commit()
            cursor.close()
            return True
            
        except mysql.connector.Error as e:
            st.error(f"Error inserting match data: {e}")
            return False
        finally:
            if conn.is_connected():
                conn.close()
    
    def get_real_matches_from_db(self) -> pd.DataFrame:
        """Get real matches stored in database"""
        query = '''
            SELECT cricbuzz_match_id, match_description, match_format, 
                   series_name, current_status, match_date
            FROM matches 
            WHERE cricbuzz_match_id IS NOT NULL
            ORDER BY match_date DESC, match_id DESC
            LIMIT 20
        '''
        return self.execute_query(query)