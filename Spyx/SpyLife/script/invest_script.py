import json, random, time

while True:
    # Charger le fichier JSON
    with open('./db/invest.json', 'r') as json_file:
        data = json.load(json_file)

    for key, value in data.items():
        crypto_fluctuation = random.uniform(-0.015, 0.0175)  # Fluctuation aléatoire entre -15% et 17.5%
        new_invest_value = value * (1 + crypto_fluctuation)
        new_invest_value = round(new_invest_value, 2)  # Arrondir à 2 chiffres après la virgule

        data[key] = new_invest_value

        print(f"Investment value for {key}: {new_invest_value}")
    
    with open("./db/invest.json", "w") as configjsonFile:
        json.dump(data, configjsonFile, indent=4)

    time.sleep(60) 
