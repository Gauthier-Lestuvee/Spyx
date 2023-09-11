import discord, json, datetime, random, asyncio, time
from discord.ext import commands

#Lecture de la DB JSON
with open("./db/db.json", "r") as configjsonFile:
    configData = json.load(configjsonFile)

with open('./db/store.json', 'r', encoding='utf-8') as json_file:
    priceData = json.load(json_file)

with open('./db/real_estate.json', 'r') as configjsonFile:
    houseData = json.load(configjsonFile)

intents = discord.Intents.all()

#Daclaration du bot
Client = commands.Bot(command_prefix=configData['prefix'], intents=intents, help_command=None)


@Client.event
async def on_ready():
    print('I am started / -', f'- \ Logged on -> {Client.user} | I\'m developed by Koro aka kx._ro on discord.')
    #How many server as connected
    print(f'Connected to {len(Client.guilds)} servers')
    #How many users as connected
    print(f'Connected to {len(Client.users)} users')
    #Client presence
    await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=configData['prefix']+"help"), status=discord.Status.idle)


@Client.event
async def on_member_join(member):
    welcome_channel_id = configData["welc_id"]
    welcome_message = f"Bienvenue sur le serveur, {member.mention}! Vous commencez une nouvelle vie avec un an d'argent de poche."

    # Fetch the welcome channel and reply the welcome message
    welcome_channel = Client.get_channel(welcome_channel_id)
    if welcome_channel:
        await welcome_channel.reply(welcome_message)


#Suppression de commande "help"
@Client.command(name='/commands', description='Show available commands.', aliases=['commands', 'help'])
async def show_commands(ctx):
    embed = discord.Embed(
        title="Available Commands",
        color=discord.Color.yellow()
    )
    
    for command in Client.commands:
        embed.add_field(name=f"> {command.name}", value=command.description, inline=False)
    
    await ctx.reply(embed=embed)
    print('[LOGS]- The help command has been executed.')


with open('./db/craft.json', 'r', encoding='utf-8') as configjsonFile:
    craftData = json.load(configjsonFile)

with open('./db/inventory.json', 'r') as configjsonFile:
    inventoryData = json.load(configjsonFile)

class craftView(discord.ui.View):
    def __init__(self):
        super().__init__()

    
    @discord.ui.select(
        placeholder="Craft disponible",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=product_name,
                description=f"Ce craft avec {product_data[0]['required']} | Ce vend {product_data[0]['price']}€",
                emoji=product_data[0]['emoji']
            )
            for product_name, product_data in craftData.items()
        ]
    )
    async def callback(self, interaction: discord.Interaction, select):
        
        with open('./db/craft.json', 'r', encoding='utf-8') as configjsonFile:
            craftData = json.load(configjsonFile)

        with open('./db/inventory.json', 'r', encoding='utf-8') as configjsonFile:
            inventoryData = json.load(configjsonFile)
        
        user_display_name = interaction.user.name
        selected_product_name = select.values[0]

        # Dans la fonction callback de la classe craftView
        user_inventory = inventoryData.get(user_display_name, [])

        # Trouver les informations sur le produit sélectionné
        selected_product_info = None
        for product_info in craftData.values():
            if product_info[0]["name"] == selected_product_name:
                selected_product_info = product_info
                break
            
        if selected_product_info is None:
            await interaction.response.send_message("Le produit sélectionné n'existe pas.", ephemeral=True)
            return

        with open('./db/store.json', 'r', encoding='utf-8') as configjsonFile:
            storeData = json.load(configjsonFile)
        
        # Vérifier si l'utilisateur a les ressources nécessaires pour crafter
        print(user_display_name)
        missing_items = []
        for required_item in selected_product_info[0]["required"]:
            found = False
            for inventory_item in user_inventory:
                if inventory_item["name"] == required_item:
                    found = True
                    user_inventory.remove(inventory_item)  # Supprimer l'élément de l'inventaire
                    
                    break
            if not found:
                missing_items.append(required_item)
        update_inventories = {
                        "name": selected_product_name,
                        "price": priceData[f"{selected_product_name}"]["price"],
                        "type": priceData[f"{selected_product_name}"]["type"]
                    }
        user_inventory.append(update_inventories)
        if missing_items:
            missing_items_formatted = ", ".join(missing_items)
            await interaction.response.send_message(f"Vous n'avez pas les ressources nécessaires pour crafter cela. Vous avez besoin de: {missing_items_formatted}.", ephemeral=True)
            return
        
        # Enlever les ressources nécessaires de l'inventaire de l'utilisateur
        for required_item in selected_product_info[0]["required"]:
            for inventory_item in user_inventory:
                if inventory_item["name"] == required_item:
                    user_inventory.remove(inventory_item)
                    break
                
        # Enregistrer les modifications dans les fichiers JSON
        with open('./db/inventory.json', 'w') as configjsonFile:
            json.dump(inventoryData, configjsonFile, indent=4)

        await interaction.response.send_message(f"Vous avez crafté 1 {selected_product_name}.", ephemeral=True)


# Naissance de joueur

@Client.command(name="/birth", description="Commencer une nouvelle vie", aliases=["birth"])
async def birth(ctx):
    with open("./db/player.json", "r") as configjsonFile:
        playerData = json.load(configjsonFile)

    if ctx.author.name not in playerData:
        playerData[ctx.author.name] = {
            "heal": 100,
            "drink": 100,
            "food": 100,
            "level": 0,
            "xp": 0,
            "money": 540
        }
        
        with open("./db/player.json", "w") as configjsonFile:
            json.dump(playerData, configjsonFile, indent=4)
    else:
        embed = discord.Embed(
            title="Impossible de créer une nouvelle vie",
            description="Vous avez déjà créé une vie. Contacter le staff pour en obtenir une nouvelle.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)
        return
        
    embed = discord.Embed(
        title="Une nouvelle vie ?",
        description=f"Bienvenue sur le serveur {ctx.author.name} ! Vous commencez une nouvelle vie avec un an d'argent de poche.",
        color=discord.Color.yellow()
    )
    await ctx.reply(embed=embed)

#player info
@Client.command(name="/player", description="Permet de voir les informations de votre joueur.", aliases=["player"])
async def player_info(ctx):
    with open('./db/player.json', 'r') as configjsonFile:
        playerData = json.load(configjsonFile)

    embed = discord.Embed(
        title="Information de " + ctx.author.name,
        description="**Votre santé :** " + str(playerData[ctx.author.name]["heal"]) + "/100 \n\n **Votre faim : **" + str(playerData[ctx.author.name]["food"]) + "/100 \n\n **Votre soif : **" + str(playerData[ctx.author.name]["drink"]) + "/100 \n\n **Votre argent : **" + str(playerData[ctx.author.name]["money"]) + "€",
        color=discord.Color.yellow()
    )
    await ctx.reply(embed=embed)

# Boire
@Client.command(name="/boire <PRODUIT>", description="Permet de boire", aliases=["boire"])
async def boire(ctx, produit):
    with open('./db/inventory.json', 'r', encoding='utf-8') as configjsonFile:
        inventoryData = json.load(configjsonFile)
    
    with open('./db/inventory.json', 'r', encoding='utf-8') as configjsonFile:
        playerData = json.load(configjsonFile)

    with open('./db/store.json', 'r', encoding='utf-8') as configjsonFile:
        storeData = json.load(configjsonFile)
     # Récupérez le nom de l'utilisateur qui a tapé la commande
    user_name = ctx.author.name

    # Vérifiez si l'utilisateur existe dans le fichier JSON
    if user_name not in inventoryData:
        await ctx.send("Vous ne possédez pas d'inventaire.")
        return

    # Accédez à l'inventaire de l'utilisateur
    user_inventory = inventoryData[user_name]

    # Recherchez et supprimez l'élément dans l'inventaire de l'utilisateur
    found = False
    for item in user_inventory:
        if item["name"] == produit and item["type"] == "drinks":
            user_inventory.remove(item)
            found = True
            break

    # Sauvegardez les modifications dans le fichier JSON
    with open('./db/inventory.json', 'w', encoding='utf-8') as json_file:
        json.dump(inventoryData, json_file, ensure_ascii=False, indent=4)

    if found:
        embed = discord.Embed(
            title="Vous avez retiré 1 " + produit + ".",
            description="Vous avez bu 1 " + produit + ".",
            color=discord.Color.yellow()
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title="Vous n'avez pas de " + produit + ".",
            description="Vous pouvez l'acheter avec " + configData["prefix"] + "store",
            color=discord.Color.yellow()
        )
        await ctx.reply(embed=embed)

# Dans votre commande craft
@commands.command(name="/craft", description="Permet de créer de nouveaux produits.", aliases=["crft", "craft"])
async def craft(ctx):
    with open('./db/jobers.json', 'r', encoding='utf-8') as configjsonFile:
        joberData = json.load(configjsonFile)
    if ctx.author.name not in joberData:
        await ctx.reply("Vous devez être marchand de nourriture pour crafter.")
    elif joberData[ctx.author.name]["jobs"] == "food_seller":
        embed = discord.Embed(
            title='Craft',
            description=f'{ctx.author.name} entre dans l\'atelier de fabrication.',
            color=discord.Color.yellow()
        )
        await ctx.reply(embed=embed, view=craftView())
    else:
        await ctx.reply("Vous devez être marchand de nourriture pour crafter.")

Client.add_command(craft)


#Investissement
@Client.command(name="/invest <montant>", description="Permet de commencer a investir dans différentes choses.", aliases=["investir", "invest"])
async def invest(ctx, money_invest: int):
    
    with open('./db/player.json', 'r') as configjsonFile:
        playerData = json.load(configjsonFile)
        
    with open('./db/invest.json', 'r') as configjsonFile:
        investData = json.load(configjsonFile)
    
    user_money = playerData[ctx.author.name]["money"]
    
    if money_invest == "":
        await ctx.reply("Il faut un montant pour investir !")
        return
    else:
        if money_invest <= 0:
            await ctx.reply("Vous ne pouvez pas investir cette argent !")
            return
        else:
            if user_money <= 0:
                await ctx.reply('Votre compte en banque est négatif. Vous ne pouvez pas investir')
                return  
            else:
                if user_money <= money_invest:
                    await ctx.reply('Vous n\'avez pas assez d\'argent pour investir')
                    return
                else:
                    if ctx.author.name not in investData:
                        investData[ctx.author.name] = 0

                    investData[ctx.author.name] = investData[ctx.author.name] + money_invest
                    playerData[ctx.author.name]["money"] = user_money - money_invest

                    with open("./db/player.json", "w") as configjsonFile:
                        json.dump(playerData, configjsonFile, indent=4)

                    with open("./db/invest.json", "w") as configjsonFile:
                        json.dump(investData, configjsonFile, indent=4)
                
            
    
    embed = discord.Embed(
        title="Investissement",
        description=f"{ctx.author.name} a investi {money_invest}€",
        color=discord.Color.yellow()
    )

    await ctx.reply(embed=embed)


@Client.command(name="/look_invest", description="Permet de voir le montant d'investissement.", aliases=["see_invest", "look_invest", "li"])
async def look_invest(ctx):
    
    with open('./db/player.json', 'r') as configjsonFile:
        playerData = json.load(configjsonFile)
    
    user_money = playerData[ctx.author.name]["money"]
    
    # Load the latest investData from the JSON file
    with open("./db/invest.json", "r") as investjsonFile:
        investData = json.load(investjsonFile)
    user_money = playerData[ctx.author.name]["money"]
    
    # Load the latest investData from the JSON file
    with open("./db/invest.json", "r") as investjsonFile:
        investData = json.load(investjsonFile)

    user_invest_amount = investData.get(ctx.author.name, 0)
    
    if user_money == 0:
        await ctx.reply("Vous n'avez aucun montant d'investissement!")
        return
    else:
        embed = discord.Embed(
            title="Investissement",
            color=discord.Color.yellow()
        )
        embed.add_field(name=f"Montant d'investissement de {ctx.author.name}", value=f"{user_invest_amount}€", inline=False)
        await ctx.reply(embed=embed)


@Client.command(name="/sell_invest", description="Permet de vendre le montant d'invest", aliases=["sell_invest", "sinvest", "si"])
async def sell_invest(ctx):
    
    with open("./db/player.json", "r") as configjsonFile:
        playerData = json.load(configjsonFile)
    
    with open("./db/invest.json", "r") as configjsonFile:
        investData = json.load(configjsonFile)
    
    playerData[ctx.author.name]["money"] = playerData[ctx.author.name]["money"] + investData[ctx.author.name]
    
    with open("./db/player.json", "w") as configjsonFile:
        json.dump(playerData, configjsonFile, indent=4)
        
    
    embed = discord.Embed(
        title="Investissement",
        description=f"{ctx.author.name} a retirer son investissement et empoche {investData[ctx.author.name]}€",
        color=discord.Color.yellow()
    )
    
    investData[ctx.author.name] = 0
    
    with open("./db/invest.json", "w") as configjsonFile:
        json.dump(investData, configjsonFile, indent=4)
    
    await ctx.reply(embed=embed)


# Définissez la commande "store"
@commands.command(name="/store", description="Permet d'accéder au magasin pour acheter des produits.", aliases=["store", "magasin"])
async def store(ctx):
    
    embed = discord.Embed(
        title='Magasin',
        description=f'{ctx.author.name} entre dans le magasin',
        color=discord.Color.yellow()
    )
    await ctx.reply(embed=embed, view=StoreView())


# Créez une classe pour la vue du magasin
class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(
        placeholder="Ouvrir le magasin",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=product_data["name"],
                description=f"{product_data['description']} - {product_data['price']}€",
                emoji=product_data['emoji']
            )
            for product_data in priceData.values()
        ]
    )
    async def callback(self, interaction: discord.Interaction, select):
        with open('./db/inventory.json', 'r') as configjsonFile:
            inventoryData = json.load(configjsonFile)
    
        with open('./db/player.json', 'r') as configjsonFile:
            playerData = json.load(configjsonFile)
        
        
        user_display_name = interaction.user.name
        selected_product_name = select.values[0]

        if playerData[user_display_name]["money"] < priceData[f"{selected_product_name}"]["price"]:
            await interaction.response.send_message("Vous n'avez pas assez d'argent pour acheter cela.", ephemeral=True)
            return

        # Mettez à jour l'inventaire de l'utilisateur et l'argent
        
        update_inventories = {
            "name": selected_product_name,
            "price": priceData[f"{selected_product_name}"]["price"],
            "type": priceData[f"{selected_product_name}"]["type"]
        }
        
        if user_display_name not in inventoryData:
            inventoryData[user_display_name] = []
        inventoryData[user_display_name].append(update_inventories)
        playerData[user_display_name]["money"] -= priceData[selected_product_name]["price"]

        # Enregistrez les modifications dans les fichiers JSON
        with open('./db/inventory.json', 'w') as configjsonFile:
            json.dump(inventoryData, configjsonFile, indent=4)

        with open('./db/player.json', 'w') as configjsonFile:
            json.dump(playerData, configjsonFile, indent=4)

        await interaction.response.send_message(f"Vous avez acheté 1 {selected_product_name}", ephemeral=True)

Client.add_command(store)



#Inventaire
@Client.command(name="/inventory", description="Permet de voir son inventaire.", aliases=["inv", "poche", "inventory"])
async def inventory(ctx):
    with open("./db/inventory.json", "r") as configjsonFile:
        inventoryData = json.load(configjsonFile)

    user_inventory = inventoryData.get(ctx.author.name, [])

    item_counts = {}
    for item_entry in user_inventory:
        item = item_entry['name']
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    embed = discord.Embed(
        title=f"Inventaire de {ctx.author.display_name}",
        description="Voici ton inventaire :",
        color=discord.Color.yellow()
    )

    for item, count in item_counts.items():
        embed.add_field(name=item, value=f"{count}x", inline=False)

    await ctx.reply(embed=embed)


@Client.command(name="/propriety", description="Permet d'ouvrir l'inventaire du joueur.", aliases=["prpt", "myhouse", "propriety"])
async def propriety(ctx):
    with open("./db/propriety.json", "r") as configjsonFile:
        proprietyData = json.load(configjsonFile)
    
    list_name = ctx.author.name
    
    propriety_counts = {}

    for propriety in proprietyData.get(list_name, []):
        if propriety in propriety_counts:
            propriety_counts[propriety] += 1
        else:
            propriety_counts[propriety] = 1

    embed = discord.Embed(
        title = f"Prorpriété de {list_name}",
        description="Voici tes propriétés :",
        color=discord.Color.yellow()
    )
    
    for propriety, count in propriety_counts.items():        
        embed.add_field(name=propriety, value=f"{count}", inline=False)
    
    await ctx.reply(embed=embed)


#Affichage Money
@Client.command(name="/money", description="Affiche l\'argent disponible sur votre compte.", aliases=["balance", "bank", "banque", "portfolio", "money", "currency"])
async def bank(ctx):
    with open("./db/player.json", "r") as configjsonfile:
        playerData = json.load(configjsonfile)

    if ctx.author.name not in playerData:
        playerData[ctx.author.name]["money"] = 540
        with open("./db/player.json", "w") as configjsonFile:
            json.dump(playerData, configjsonFile, indent=4)
    user_money = playerData[ctx.author.name]["money"]
    round_user_money = round(user_money, 2)
    
    embed = discord.Embed(
        title=f"Portefeuille de {ctx.author.name}",
        description=f"> {round_user_money} €",
        color=discord.Color.green()
    )
    
    await ctx.reply(embed=embed)


#Job
@Client.command(name="/job <job_name>", description="Permet de choisir un job.", aliases=["job"])
async def job(ctx, job_name):
    with open("./db/jobs.json", "r", encoding='utf-8') as configjsonFile:
        jobsData = json.load(configjsonFile)
    
    with open("./db/jobers.json", "r", encoding='utf-8') as configjsonFile:
        jobersData = json.load(configjsonFile)

    with open("./db/player.json", "r") as configjson:
        playerData = json.load(configjson)

    if job_name not in jobsData:
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"Le job {job_name} n'existe pas.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {job_name} n\'existe pas.')
    
    else :
        if ctx.author.name not in jobersData:
            jobersData[ctx.author.name] = []
        if playerData[ctx.author.name]["level"] >= jobsData[f"{job_name}"]["level"]:
            update_jobers = {
                    "jobs": jobsData[f"{job_name}"]["name"],
                    "salary": jobsData[f"{job_name}"]["salary"],
                    "mission": jobsData[f"{job_name}"]["mission"],
                    "level_reward": jobsData[f"{job_name}"]["level_reward"],
            }


            jobersData[ctx.author.name] = update_jobers

            with open("./db/jobers.json", "w") as configjsonFile:
                json.dump(jobersData, configjsonFile, indent=4)

            embed = discord.Embed(
                title=f"{ctx.author.name} a choisi le job {job_name}",
                description = jobsData.get(job_name, {}).get("jobs", {}) + "\n Hauteur des missions : " + str(jobsData.get(job_name, {}).get("mission", "Pas de mission")) + "€",
                color=discord.Color.yellow(),
            )
            await ctx.reply(embed=embed)
            print(f'[LOGS]- {job_name} choisi pour {ctx.author.name}.')
        
        else:
            embed = discord.Embed(
                title=f"Une erreur est survenue",
                description = f"Vous n'avez pas assez de niveau : {str(jobsData[f'{job_name}']['level'])}",
                color=discord.Color.red(),
            )
            await ctx.reply(embed=embed)


@Client.command(name="/job_list", description="Permet de voir les jobs disponibles.", aliases=["job_list", "jl"])
async def job_list(ctx):
    with open("./db/jobs.json", "r", encoding='utf-8') as configjsonFile:
        jobsData = json.load(configjsonFile)

    jobs_names = []

    for job in jobsData.values():
        jobs_names.append(job["name"])

    embed = discord.Embed(
        title=f"Liste des jobs disponibles",
        color=discord.Color.yellow(),
    )

    for name in jobsData.keys():
        embed.add_field(name=f"Poste: {name}", value=f"Métier: {jobsData[name]['jobs']} \n Salaire: {jobsData[name]['salary']}€", inline=False)

    embed.set_footer(text=f"{len(jobs_names)} jobs disponibles. Pour choisir un job, veuillez utiliser la commande '/jobs <POSTE>'.")

    await ctx.reply(embed=embed)

#Job+ (4.99€)
@Client.command(name="/missions", description="Faire des missions suplementaire pour obtenir des primes", aliases=["mission", "missions"])
async def missions(ctx):
    
    with open("./db/player.json") as jsonconfigFile:
        playerData = json.load(jsonconfigFile)
    
    with open("./db/jobers.json", "r") as configjsonFile:
        joberData = json.load(configjsonFile)
        
    if ctx.author.name not in joberData:
        embed = discord.Embed(
            title=f"Missions en cours...",
            description=f"Vous effectuer une mission d'interet général",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)

        playerData[ctx.author.name] += 0.5
        playerData[ctx.author.name]["money"] += 50

    elif joberData[ctx.author.name]["jobs"] == "scientist":
        embed = discord.Embed(
            title="Mission en cours ...",
            description=f"{ctx.author.name} a entrain de faire des expériences.",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)

        playerData[ctx.author.name]["money"] += joberData[ctx.author.name]["mission"]
        playerData[ctx.author.name]["level"] += joberData[ctx.author.name]["level_reward"]

    elif joberData[ctx.author.name]["jobs"] == "engineer":
        embed = discord.Embed(
            title="Mission en cours...",
            description=f"{ctx.author.name} a résolu des problèmes.",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)
        
        playerData[ctx.author.name]["money"] += joberData[ctx.author.name]["mission"]
        playerData[ctx.author.name]["level"] += joberData[ctx.author.name]["level_reward"]
    
    elif joberData[ctx.author.name]["jobs"] == "farmer":
        embed = discord.Embed(
            title="Mission en cours...",
            description=f"{ctx.author.name} a entrain de labourer la terre.",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)
        
        playerData[ctx.author.name]["money"] += joberData[ctx.author.name]["mission"]
        playerData[ctx.author.name]["level"] += joberData[ctx.author.name]["level_reward"]
    
    elif joberData[ctx.author.name]["jobs"] == "mechanic":
        embed = discord.Embed(
            title="Mission en cours...",
            description=f"{ctx.author.name} a vendu des pièces automobile.",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)
        
        playerData[ctx.author.name]["money"] += joberData[ctx.author.name]["mission"]
        playerData[ctx.author.name]["level"] += joberData[ctx.author.name]["level_reward"]

    elif joberData[ctx.author.name]["jobs"] == "doctor":
        embed = discord.Embed(
            title="Mission en cours...",
            description=f"{ctx.author.name} a effectuer des visites a domicile.",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)

        playerData[ctx.author.name]["money"] += joberData[ctx.author.name]["mission"]
        playerData[ctx.author.name]["level"] += joberData[ctx.author.name]["level_reward"]

    elif joberData[ctx.author.name]["jobs"] == "car_dealer":
        embed = discord.Embed(
            title="Mission en cours...",
            description=f"{ctx.author.name} a livré des véhicules.",
            color=discord.Color.blue(),
        )
        await ctx.reply(embed=embed)

        playerData[ctx.author.name]["money"] += joberData[ctx.author.name]["mission"]
        playerData[ctx.author.name]["level"] += joberData[ctx.author.name]["level_reward"]
    
    with open("./db/player.json", "w") as configjsonFile:
        json.dump(playerData, configjsonFile, indent=4)


#Error command
@Client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"La commande {error} n'existe pas.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"Il manque un parametre essentiel a la commande.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"Vous n'avez pas la permission d'utiliser cette commande.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"Echec de vérification de l'utilisateur.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"Le membre {error.name} n'existe pas.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f"[LOGS]- {error}.")
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title=f"Une erreur est survenue",
            description=f"Une erreur est survenue lors de l'exécution de cette commande.",
            color=discord.Color.red(),
        )
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')

#Start du bot
Client.run(configData['token'])