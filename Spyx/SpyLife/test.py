import json

# Votre JSON
with open('./db/inventory.json', 'r') as f:
    data = json.load(f)

user_to_process = "kx._ro"

# Liste pour stocker les noms et les types des éléments de type "drinks" pour l'utilisateur spécifié
drinks_info_list = []

# Accédez aux éléments de l'utilisateur spécifié
user_items = data.get(user_to_process, [])

# Parcourez les éléments et ajoutez les noms et les types des éléments de type "drinks" à la liste
for item in user_items:
    if item["type"] == "drinks":
        drinks_info_list.append({"name": item["name"], "type": item["type"]})

# Affichez la liste des noms et des types des éléments de type "drinks" pour cet utilisateur
for drink_info in drinks_info_list:
    print(drink_info)