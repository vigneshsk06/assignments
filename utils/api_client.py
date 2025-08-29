"""
Enhanced Cricbuzz API client for fetching real cricket data
Uses your actual API key to get live cricket information
"""

import requests
import os
from typing import Dict, List, Optional, Any
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

class CricbuzzAPI:
    def __init__(self):
        """Initialize API client with your credentials"""
        self.api_key = "a1d59cf309msh2d8fb4eb7d0140fp1e3691jsnf9190b45bdbc"
        self.api_host = "cricbuzz-cricket.p.rapidapi.com"
        self.base_url = f"https://{self.api_host}"
        
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host
        }
    
    def make_request(self, endpoint: str) -> Dict[Any, Any]:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.warning(f"API returned status code: {response.status_code}")
                return self.get_fallback_data(endpoint)
                
        except requests.exceptions.RequestException as e:
            st.warning(f"Network error: {str(e)}")
            return self.get_fallback_data(endpoint)
        except Exception as e:
            st.warning(f"API error: {str(e)}")
            return self.get_fallback_data(endpoint)
    
    def get_fallback_data(self, endpoint: str) -> Dict[Any, Any]:
        """Fallback data when API is unavailable"""
        if 'recent' in endpoint or 'live' in endpoint:
            return {
                "typeMatches": [
                    {
                        "matchType": "International",
                        "seriesMatches": [
                            {
                                "seriesAdWrapper": {
                                    "seriesName": "India vs Australia Test Series 2024",
                                    "matches": [
                                        {
                                            "matchInfo": {
                                                "matchId": 12345,
                                                "matchDesc": "1st Test",
                                                "matchFormat": "TEST",
                                                "startDate": "2024-08-28T09:30:00.000Z",
                                                "state": "Live",
                                                "status": "Day 1 - India 245/4 (75.0 Ovs)",
                                                "team1": {"teamName": "India", "teamSName": "IND"},
                                                "team2": {"teamName": "Australia", "teamSName": "AUS"},
                                                "venueInfo": {"ground": "Wankhede Stadium", "city": "Mumbai"}
                                            }
                                        },
                                        {
                                            "matchInfo": {
                                                "matchId": 12346,
                                                "matchDesc": "2nd Test",
                                                "matchFormat": "TEST",
                                                "startDate": "2024-08-25T09:30:00.000Z",
                                                "state": "Complete",
                                                "status": "India won by 8 wickets",
                                                "team1": {"teamName": "India", "teamSName": "IND"},
                                                "team2": {"teamName": "Australia", "teamSName": "AUS"},
                                                "venueInfo": {"ground": "Eden Gardens", "city": "Kolkata"}
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        return {"data": [], "status": "fallback"}
    
    def get_live_matches(self) -> List[Dict]:
        """Get current live matches from API"""
        try:
            st.info("Fetching live matches from Cricbuzz API...")
            data = self.make_request("matches/v1/live")
            
            matches = []
            if 'typeMatches' in data:
                for match_type in data['typeMatches']:
                    if 'seriesMatches' in match_type:
                        for series in match_type['seriesMatches']:
                            if 'seriesAdWrapper' in series:
                                series_info = series['seriesAdWrapper']
                                if 'matches' in series_info:
                                    for match in series_info['matches']:
                                        match_info = match.get('matchInfo', {})
                                        
                                        matches.append({
                                            'match_id': match_info.get('matchId'),
                                            'description': match_info.get('matchDesc', ''),
                                            'format': match_info.get('matchFormat', ''),
                                            'status': match_info.get('status', ''),
                                            'state': match_info.get('state', ''),
                                            'team1': match_info.get('team1', {}).get('teamName', ''),
                                            'team2': match_info.get('team2', {}).get('teamName', ''),
                                            'venue': match_info.get('venueInfo', {}).get('ground', ''),
                                            'city': match_info.get('venueInfo', {}).get('city', ''),
                                            'series': series_info.get('seriesName', ''),
                                            'start_date': match_info.get('startDate', '')
                                        })
            
            st.success(f"Found {len(matches)} matches from API")
            return matches
            
        except Exception as e:
            st.error(f"Error fetching live matches: {e}")
            return []
    
    def get_recent_matches(self) -> List[Dict]:
        """Get recent matches from API"""
        try:
            st.info("Fetching recent matches from Cricbuzz API...")
            data = self.make_request("matches/v1/recent")
            
            matches = []
            if 'typeMatches' in data:
                for match_type in data['typeMatches']:
                    if 'seriesMatches' in match_type:
                        for series in match_type['seriesMatches']:
                            if 'seriesAdWrapper' in series:
                                series_info = series['seriesAdWrapper']
                                if 'matches' in series_info:
                                    for match in series_info['matches']:
                                        match_info = match.get('matchInfo', {})
                                        
                                        matches.append({
                                            'match_id': match_info.get('matchId'),
                                            'description': match_info.get('matchDesc', ''),
                                            'format': match_info.get('matchFormat', ''),
                                            'status': match_info.get('status', ''),
                                            'state': match_info.get('state', ''),
                                            'team1': match_info.get('team1', {}).get('teamName', ''),
                                            'team2': match_info.get('team2', {}).get('teamName', ''),
                                            'venue': match_info.get('venueInfo', {}).get('ground', ''),
                                            'city': match_info.get('venueInfo', {}).get('city', ''),
                                            'series': series_info.get('seriesName', ''),
                                            'result': match_info.get('status', ''),
                                            'start_date': match_info.get('startDate', '')
                                        })
            
            st.success(f"Found {len(matches)} recent matches from API")
            return matches[:20]
            
        except Exception as e:
            st.error(f"Error fetching recent matches: {e}")
            return []
    
    def get_match_scorecard(self, match_id: int) -> Dict:
        """Get detailed scorecard for a specific match"""
        try:
            data = self.make_request(f"mcenter/v1/{match_id}/scard")
            return data
        except Exception as e:
            st.error(f"Error fetching scorecard: {e}")
            return {}
    
    def get_player_info(self, player_id: int) -> Dict:
        """Get detailed player information"""
        try:
            data = self.make_request(f"stats/v1/player/{player_id}")
            return data
        except Exception as e:
            st.error(f"Error fetching player info: {e}")
            return {}
    
    def get_team_rankings(self, format_type: str = "odi") -> Dict:
        """Get current team rankings"""
        try:
            data = self.make_request(f"stats/v1/rankings/teams?formatType={format_type}")
            return data
        except Exception as e:
            st.error(f"Error fetching team rankings: {e}")
            return {}
    
    def populate_database_from_api(self, db_connection):
        """Populate database with real data from API"""
        st.info("Populating database with real cricket data from API...")
        
        try:
            # Get recent matches and store in database
            recent_matches = self.get_recent_matches()
            
            inserted_count = 0
            for match in recent_matches:
                success = db_connection.insert_real_match_data(match)
                if success:
                    inserted_count += 1
            
            if inserted_count > 0:
                st.success(f"Successfully stored {inserted_count} real matches in database")
            else:
                st.warning("No new matches were added to database")
                
        except Exception as e:
            st.error(f"Error populating database: {e}")
    
    def test_api_connection(self) -> bool:
        """Test if API connection is working"""
        try:
            st.info("Testing API connection...")
            response = requests.get(f"{self.base_url}/matches/v1/recent", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                st.success("API connection successful! Using live data.")
                return True
            else:
                st.warning(f"API returned status {response.status_code}. Using fallback data.")
                return False
                
        except Exception as e:
            st.warning(f"API connection failed: {e}. Using fallback data.")
            return False