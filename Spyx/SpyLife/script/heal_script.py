import json, time

while True:
    with open('./db/player.json', 'r') as f:
        players = json.load(f)

    for key, value in players.items():
        if players[key]['food'] and players[key]['drink'] >= 0:
            players[key]['food'] -= 2
            players[key]['drink'] -= 2
            if players[key]['heal'] < 100:
                players[key]['heal'] += 1
                print(key + " heals " + str(players[key]['heal']))
            with open('./db/player.json', 'w') as f:
                json.dump(players, f, indent=4)
            print(key + " Loses food")
            break 
        else:
            if players[key]['food'] <= 0:
                players[key]['food'] = 0
                print(key + " is out of food")
                players[key]['heal'] -= 4
                with open('./db/player.json', 'w') as f:
                    json.dump(players, f, indent=4)
            if players[key]['drink'] <= 0:
                players[key]['drink'] = 0
                print(key + " is out of drink")
                players[key]['heal'] -= 4
                with open('./db/player.json', "w") as f:
                    json.dump(players, f, indent=4)
            
        if players[key]['heal'] <= 0:
            players[key]['heal'] = 0
            with open('./db/player.json', 'w') as f:
                json.dump(players, f, indent=4)
            print(key + " is died")
    
    time.sleep(300)