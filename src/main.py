from extract import get_yesterdays_games, get_game_details
from rating import GameRating
import json
from datetime import datetime

def main():
    print(f"🏀 ANALIZANDO PARTIDOS NBA")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    games = get_yesterdays_games()
    
    if not games:
        print("❌ No hay partidos")
        return
    
    rankings = []
    
    for game in games:
        home = game['homeTeam']['teamName']
        away = game['awayTeam']['teamName']
        print(f"📊 {away} @ {home}")
        
        details = get_game_details(game['gameId'])
        
        if details:
            rating = GameRating(game, details['boxscore'], details['playbyplay']).get_total_rating()
            rankings.append({
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'local': home,
                'visitante': away,
                'resultado': f"{away} {game['awayTeam']['score']} - {game['homeTeam']['score']} {home}",
                'puntuacion': rating['total'],
                'competitividad': rating['competitividad'],
                'clutch': rating['clutch'],
                'estrellas': rating['estrellas'],
                'intensidad': rating['intensidad'],
                'recomendacion': rating['recomendacion']
            })
            print(f"   ⭐ {rating['total']}/100 - {rating['recomendacion']}")
    
    rankings.sort(key=lambda x: x['puntuacion'], reverse=True)
    
    with open('ranking.json', 'w', encoding='utf-8') as f:
        json.dump(rankings, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 50)
    print("🏆 TOP 5 PARTIDOS")
    print("=" * 50)
    
    for i, game in enumerate(rankings[:5], 1):
        print(f"\n{i}. {game['visitante']} @ {game['local']}")
        print(f"   {game['resultado']}")
        print(f"   ⭐ {game['puntuacion']}/100 - {game['recomendacion']}")
    
    print(f"\n✅ Guardado en ranking.json")

if __name__ == "__main__":
    main()
