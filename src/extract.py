import requests
from datetime import datetime, timedelta
import os

def get_yesterdays_games():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"🔍 Buscando partidos del {yesterday} (balldontlie)")
    
    try:
        api_key = os.environ.get('BALLDONTLIE_API_KEY')
        if not api_key:
            print("❌ No se encontró la API Key")
            return []
        
        url = "https://api.balldontlie.io/v1/games"
        headers = {"Authorization": api_key}
        params = {"dates[]": yesterday}
        
        response = requests.get(url, headers=headers, params=params, timeout=60)
        
        if response.status_code == 401:
            print("⚠️ La API Key no tiene permisos para acceder a /games.")
            print("📌 Este endpoint requiere el plan ALL-STAR o superior.")
            print("📌 Cuando te suscribas, volverá a funcionar.")
            return []
        
        if response.status_code != 200:
            print(f"⚠️ Error HTTP: {response.status_code}")
            return []
        
        data = response.json()
        
        if not data.get('data'):
            print("⚠️ No hay partidos en esta fecha")
            return []
        
        games_list = []
        for game in data['data']:
            games_list.append({
                'gameId': game['id'],
                'homeTeam': {
                    'teamName': game['home_team']['full_name'],
                    'score': game['home_team_score']
                },
                'awayTeam': {
                    'teamName': game['visitor_team']['full_name'],
                    'score': game['visitor_team_score']
                },
                'period': game.get('period', 4)
            })
        
        print(f"✅ Encontrados {len(games_list)} partidos")
        return games_list
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def get_game_details(game_id):
    try:
        api_key = os.environ.get('BALLDONTLIE_API_KEY')
        if not api_key:
            return None
            
        url = f"https://api.balldontlie.io/v1/games/{game_id}"
        headers = {"Authorization": api_key}
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code == 401:
            print(f"⚠️ API Key sin permisos para el juego {game_id}")
            return None
        
        data = response.json()
        
        import pandas as pd
        boxscore_data = []
        
        boxscore_data.append({
            'PLAYER_NAME': 'Team Totals',
            'TEAM_ABBREVIATION': data['home_team']['abbreviation'],
            'PTS': data['home_team_score'],
            'AST': 0,
            'REB': 0,
            'PF': 0
        })
        boxscore_data.append({
            'PLAYER_NAME': 'Team Totals',
            'TEAM_ABBREVIATION': data['visitor_team']['abbreviation'],
            'PTS': data['visitor_team_score'],
            'AST': 0,
            'REB': 0,
            'PF': 0
        })
        
        boxscore_df = pd.DataFrame(boxscore_data)
        return {'boxscore': boxscore_df, 'playbyplay': None}
    except Exception as e:
        print(f"⚠️ Error en juego {game_id}: {e}")
        return None
