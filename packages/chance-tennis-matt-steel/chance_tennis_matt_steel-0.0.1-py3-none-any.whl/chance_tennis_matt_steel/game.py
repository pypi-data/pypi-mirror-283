import random
from functions import serve, return_serve, point_scorer, score

def game(difficulty):

    print("""
   ▄████████    ▄█    █▄       ▄████████ ███▄▄▄▄    ▄████████    ▄████████
███    ███   ███    ███     ███    ███ ███▀▀▀██▄ ███    ███   ███    ███
███    █▀    ███    ███     ███    ███ ███   ███ ███    █▀    ███    █▀ 
███         ▄███▄▄▄▄███▄▄   ███    ███ ███   ███ ███         ▄███▄▄▄    
███        ▀▀███▀▀▀▀███▀  ▀███████████ ███   ███ ███        ▀▀███▀▀▀    
███    █▄    ███    ███     ███    ███ ███   ███ ███    █▄    ███    █▄ 
███    ███   ███    ███     ███    ███ ███   ███ ███    ███   ███    ███
████████▀    ███    █▀      ███    █▀   ▀█   █▀  ████████▀    ██████████
                                                                        
    ███        ▄████████ ███▄▄▄▄   ███▄▄▄▄    ▄█     ▄████████          
▀█████████▄   ███    ███ ███▀▀▀██▄ ███▀▀▀██▄ ███    ███    ███          
   ▀███▀▀██   ███    █▀  ███   ███ ███   ███ ███▌   ███    █▀           
    ███   ▀  ▄███▄▄▄     ███   ███ ███   ███ ███▌   ███                 
    ███     ▀▀███▀▀▀     ███   ███ ███   ███ ███▌ ▀███████████          
    ███       ███    █▄  ███   ███ ███   ███ ███           ███          
    ███       ███    ███ ███   ███ ███   ███ ███     ▄█    ███          
   ▄████▀     ██████████  ▀█   █▀   ▀█   █▀  █▀    ▄████████▀           

          """)

    
    players_points = 0
    opponents_points = 0
    players_score = 0
    opponents_score = 0
    players_games = 0
    opponents_games = 0
    server = random.randint (1,2)
    
    while players_games < 6 and opponents_games < 6:
        serve_type = serve(server)
        outcome = return_serve(server, serve_type, difficulty)
        
        players_points, opponents_points = point_scorer(outcome, difficulty, players_points, opponents_points)

        players_points, opponents_points, players_score, opponents_score, server, players_games, opponents_games = score(players_points, opponents_points, players_score, opponents_score, players_games, opponents_games, server)

        
    

