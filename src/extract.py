def get_game_details(game_id):
    try:
        api_key = os.environ.get('BALLDONTLIE_API_KEY')
        if not api_key:
            return None
            
        url = f"https://api.balldontlie.io/v1/games/{game_id}"
        headers = {"Authorization": api_key}
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code == 401:
            print(f"⚠️ API Key sin permisos para el juego {game_id}. Requiere plan ALL-STAR")
            return None
        
        if response.status_code != 200:
            print(f"⚠️ Error HTTP {response.status_code} para juego {game_id}")
            return None
        
        data = response.json()
        
        # Verificar que la respuesta contiene los datos esperados
        if not data or 'home_team' not in data:
            print(f"⚠️ Datos incompletos para juego {game_id}")
            return None
        
        import pandas as pd
        boxscore_data = []
        
        boxscore_data.append({
            'PLAYER_NAME': 'Team Totals',
            'TEAM_ABBREVIATION': data.get('home_team', {}).get('abbreviation', 'HOM'),
            'PTS': data.get('home_team_score', 0),
            'AST': 0,
            'REB': 0,
            'PF': 0
        })
        boxscore_data.append({
            'PLAYER_NAME': 'Team Totals',
            'TEAM_ABBREVIATION': data.get('visitor_team', {}).get('abbreviation', 'VIS'),
            'PTS': data.get('visitor_team_score', 0),
            'AST': 0,
            'REB': 0,
            'PF': 0
        })
        
        boxscore_df = pd.DataFrame(boxscore_data)
        return {'boxscore': boxscore_df, 'playbyplay': None}
        
    except Exception as e:
        print(f"⚠️ Error en juego {game_id}: {e}")
        return None
