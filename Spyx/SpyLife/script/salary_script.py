import json, time

while True:
    with open("./db/jobers.json") as json_file:
        jobersData = json.load(json_file)

    with open("./db/player.json") as json_file:
        playerData = json.load(json_file)

    for key, value in jobersData.items():
        # Assurez-vous que playerData est un dictionnaire
        if isinstance(playerData, dict) and key in playerData:
            portfolio = playerData[key]["money"]
            salary = value["salary"]

            new_account = portfolio + salary

            playerData[key]["money"] = new_account

            print(key, playerData[key])

            with open("./db/player.json", "w") as money_json_file:
                json.dump(playerData, money_json_file)

    time.sleep(60*60)
