import random

def serve(server):
    
    if server == 1:
        print("Your Serve")
        serve_type = input("Select your serve (Power, Curve, Safe): ").lower()[0]

    elif server == 2:
        print("Opponents Serve")
        serve_type_number = random.randint(1,3)
        if serve_type_number == 1:
            serve_type = "p"
        elif serve_type_number == 2:
            serve_type = "c"
        else:
            serve_type = "s"
    return serve_type


def return_serve(serve_number, serve_type, difficulty):
    if serve_number == 1:
        if serve_type == "p":
            in_probability = 0.7
            return_probability = difficulty/10 * in_probability
            random1 = random.uniform(0,1)
            if return_probability > random1:
                print("Serve returned")
                return 1    #1 indicates players rally shot
            else:
                print("""
                    ▄████████  ▄████████    ▄████████
                    ███    ███ ███    ███   ███    ███
                    ███    ███ ███    █▀    ███    █▀ 
                    ███    ███ ███         ▄███▄▄▄    
                    ▀███████████ ███        ▀▀███▀▀▀    
                    ███    ███ ███    █▄    ███    █▄ 
                    ███    ███ ███    ███   ███    ███
                    ███    █▀  ████████▀    ██████████

                    """)
                return 2    # indicates add point to player
        
        elif serve_type == "c":
            in_probability = 0.95
            return_probability = difficulty/10 * in_probability
            random1 = random.uniform(0,1)
            if return_probability > random1:
                print("Serve returned")
                return 1    #1 indicates players rally shot
            else:
                print("""
                    ▄████████  ▄████████    ▄████████
                    ███    ███ ███    ███   ███    ███
                    ███    ███ ███    █▀    ███    █▀ 
                    ███    ███ ███         ▄███▄▄▄    
                    ▀███████████ ███        ▀▀███▀▀▀    
                    ███    ███ ███    █▄    ███    █▄ 
                    ███    ███ ███    ███   ███    ███
                    ███    █▀  ████████▀    ██████████

                    """)
                return 2    # indicates add point to player
            
        elif serve_type == "s":
            in_probability = 0.99
            return_probability = difficulty/10 * in_probability
            random1 = random.uniform(0,1)
            if return_probability > random1:
                print("Serve returned")
                return 1    #1 indicates players rally shot
            else:
                print("""\
                    ▄████████  ▄████████    ▄████████
                    ███    ███ ███    ███   ███    ███
                    ███    ███ ███    █▀    ███    █▀ 
                    ███    ███ ███         ▄███▄▄▄    
                    ▀███████████ ███        ▀▀███▀▀▀    
                    ███    ███ ███    █▄    ███    █▄ 
                    ███    ███ ███    ███   ███    ███
                    ███    █▀  ████████▀    ██████████

                    """)
                return 2    # indicates add point to player


    elif serve_number == 2:
        return_type = input("Choose your return shot (Hard, Soft): ").lower()[0]
        if return_type == "h":
            return_probability = 1 - difficulty/12
            random2 = random.uniform(0,1)
            if return_probability > random2:
                print("You have returned the serve")
                return 3    # indicates opponents rally shot
            else:
                print("You missed!")
                return 4    # indicates add point to opponent
        
        elif return_type == "s":
            return_probability = 1 - difficulty/20
            random2 = random.uniform(0,1)
            if return_probability > random2:
                print("You have returned the serve")
                return 3    # indicates opponents rally shot
            else:
                print("You missed!")
                return 4    # indicates add point to opponent
        

def rally(turn, difficulty):
    if turn == 1:
        shot_type = input("Choose shot type (Hard, Soft): ").lower()[0]
        if shot_type == "h":
            in_probability = 1 - difficulty/25
            return_probability = difficulty/18
        elif shot_type == "s":
            in_probability = 1 - difficulty/30
            return_probability = difficulty/13
        random2 = random.uniform(0,1)
        if return_probability > random2 and in_probability > random2:
            print("Your shot was returned")
            final_outcome = rally(1,difficulty)    # indicates another rally shot
            return final_outcome
        elif in_probability < random2:
            print("You missed the shot")
            final_outcome = 1
            return final_outcome
        elif return_probability < random2 and in_probability > random2:
            print("You won the point")
            final_outcome = 2
            return 2
    
    elif turn == 3:
        return_shot_number = random.randint(1,2)
        if return_shot_number == 1:
            return_type = "h"
        elif return_shot_number == 2:
            return_type = "s"

        if return_type == "h":
            winner_probability = difficulty/20
            random3 = random.uniform(0,1)
            if winner_probability > random3:
                print("Opponent hit a winner")
                final_outcome = 1
                return final_outcome
            else:
                print("Opponent returned, your shot")
                final_outcome = rally(1,difficulty)
                return final_outcome
        
        if return_type == "s":
            winner_probability = difficulty/15
            random4 = random.uniform(0,1)
            if winner_probability > random4:
                print("Opponent hit a winner")
                final_outcome = 1
                return final_outcome
            else:
                print("Opponent returned, your shot")
                final_outcome = rally(1,difficulty)
                return final_outcome

def point_scorer(outcome, difficulty, players_points, opponents_points):
    if outcome == 1:
        final_outcome = rally(outcome, difficulty)
        if final_outcome == 1:
            opponents_points += 1
        elif final_outcome == 2:
            players_points += 1

    elif outcome == 2:
        players_points += 1

    elif outcome == 3:
        final_outcome = rally(outcome, difficulty)
        if final_outcome == 1:
            opponents_points += 1
        elif final_outcome == 2:
            players_points += 1

    elif outcome == 4:
        opponents_points += 1
    
    return players_points, opponents_points


def score(players_points, opponents_points, players_score, opponents_score, players_games, opponents_games, server):
    if players_points == 0:
        players_score = 0
    elif players_points == 1:
        players_score = 15
    elif players_points == 2:
        players_score = 30
    elif players_points == 3:
        players_score = 40
    elif players_points == 4:
        players_games += 1
        players_points = 0
        players_score = 0
        opponents_points = 0
        opponents_score = 0
        print(F"{players_games}:{opponents_games} games won")
        if server == 1:
            server = 2
        elif server == 2:
            server = 1

    
    if opponents_points == 0:
        opponents_score = 0
    elif opponents_points == 1:
        opponents_score = 15
    elif opponents_points == 2:
        opponents_score = 30
    elif opponents_points == 3:
        opponents_score = 40
    elif opponents_points == 4:
        opponents_games += 1
        players_points = 0
        players_score = 0
        opponents_points = 0
        opponents_score = 0
        print(F"{players_games}:{opponents_games} games won")
        if server == 1:
            server = 2
        elif server == 2:
            server = 1
    
    print(F"{players_score}:{opponents_score}")
    return players_points, opponents_points, players_score, opponents_score, server, players_games, opponents_games



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