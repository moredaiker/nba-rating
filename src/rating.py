import pandas as pd

class GameRating:
    def __init__(self, game_info, boxscore_df, pbp_df):
        self.game = game_info
        self.boxscore = boxscore_df if boxscore_df is not None else pd.DataFrame()
        
        self.home_score = game_info.get('homeTeam', {}).get('score', 0)
        self.away_score = game_info.get('awayTeam', {}).get('score', 0)
        self.margin = abs(self.home_score - self.away_score)
    
    def competitiveness_score(self):
        margin_score = max(0, 1 - (self.margin / 20))
        return round(margin_score * 100, 1)
    
    def clutch_score(self):
        is_overtime = 1 if self.game.get('period', 4) > 4 else 0
        if is_overtime:
            return 80.0
        elif self.margin < 5:
            return 70.0
        elif self.margin < 10:
            return 50.0
        else:
            return 20.0
    
    def star_power_score(self):
        if self.boxscore.empty:
            return 30.0
        
        score = 0
        for _, player in self.boxscore.iterrows():
            if player.get('PLAYER_NAME') in ['Team Totals', None, '']:
                continue
            
            points = player.get('PTS', 0)
            assists = player.get('AST', 0)
            rebounds = player.get('REB', 0)
            
            if points and points >= 40:
                score += 30
            elif points and points >= 30:
                score += 15
            if points and assists and rebounds and points >= 10 and assists >= 10 and rebounds >= 10:
                score += 20
        
        return min(100, score)
    
    def intensity_score(self):
        if self.boxscore.empty:
            return 50.0
        
        total_fouls = 0
        if 'PF' in self.boxscore.columns:
            player_fouls = self.boxscore[
                (self.boxscore['PLAYER_NAME'].notna()) & 
                (self.boxscore['PLAYER_NAME'] != 'Team Totals')
            ]['PF'].sum()
            total_fouls = player_fouls if pd.notna(player_fouls) else 0
        
        if total_fouls < 30:
            return 80.0
        elif total_fouls < 45:
            return 50.0
        else:
            return 30.0
    
    def get_total_rating(self):
        comp = self.competitiveness_score() / 100
        clut = self.clutch_score() / 100
        star = self.star_power_score() / 100
        intensity = self.intensity_score() / 100
        
        total = (comp * 0.40) + (clut * 0.30) + (star * 0.20) + (intensity * 0.10)
        
        if total >= 0.8:
            recommendation = "🔥 IMPRESCINDIBLE"
        elif total >= 0.65:
            recommendation = "✅ MUY BUENO"
        elif total >= 0.5:
            recommendation = "👍 ACEPTABLE"
        else:
            recommendation = "⏭️ PRESCINDIBLE"
        
        return {
            'total': round(total * 100, 1),
            'competitividad': round(comp * 100, 1),
            'clutch': round(clut * 100, 1),
            'estrellas': round(star * 100, 1),
            'intensidad': round(intensity * 100, 1),
            'recomendacion': recommendation
        }
