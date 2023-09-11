import discord, json
from discord.ext import commands

with open('./DB/config.json', 'r') as f:
    configData = json.load(f)

Client = commands.Bot(command_prefix=configData['prefix'], intents=discord.Intents.all(), help_command=None)

@Client.event
async def on_ready():
    print(f'Logged in as {Client.user}')
    await Client.change_presence(status=discord.Status.online, activity=discord.Game(name=configData['status']))

@Client.command(name='!commands', description='Show available commands.', aliases=['commands', 'help'])
async def show_commands(ctx):
    embed = discord.Embed(
        title="Available Commands",
        color=discord.Color.yellow()
    )

    embed.set_thumbnail(url=configData["SysopIcon"])
    
    for command in Client.commands:
        embed.add_field(name=f"> {command.name}", value=command.description, inline=False)
    
    await ctx.reply(embed=embed)
    print('[LOGS]- The help command has been executed.')

#Latency command
@Client.command(name='!ping', description='See the bot\'s reaction time.', aliases=["ping"])
async def ping(ctx):
    ping = round(Client.latency * 1000)
    embed = discord.Embed(
        title='Pong!',
        description=f'Pong! \n Reacted in {ping}ms',
        color=discord.Color.yellow()
    )
    embed.set_thumbnail(url=configData["SysopIcon"])
    await ctx.reply(embed=embed)
    print('[LOGS]- The ping command has been executed.')
        
#kick command

@Client.command(name='!kick', description='Kick a user from the server.', aliases=["kick"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(
        title=f"{member.name} has been kicked!",
        description=f"Reason: {reason}",
        color=discord.Color.red(),
    )
    embed.set_thumbnail(url=configData["SysopIcon"])
    embed.set_footer(f"This bot has developed by kx._ro")
    await ctx.reply(embed=embed)
    print(f'[LOGS]- {member.name} has been kicked.')


#Ban commands
@Client.command(name='!ban', description='Ban a member from the server.', aliases=["ban"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title=f"{member.name} has been banned!",
        description=f"Reason: {reason}",
        color=discord.Color.red(),
    )
    embed.set_thumbnail(url=configData["SysopIcon"])
    await ctx.reply(embed=embed)
    print(f'[LOGS]- {member.name} has been banned.')

#Unban command
@Client.command(name='!unban', description='Unban a member from the server.', aliases=["unban"])
@commands.has_permissions(ban_members=True)
async def unban(ctx, member_id: int, *, reason=None):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if ban_entry.user.id == member_id:
            await ctx.guild.unban(ban_entry.user, reason=reason)
            embed = discord.Embed(
                title=f"{ban_entry.user.name} has been unbanned!",
                description=f"Reason: {reason}",
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url=configData["SysopIcon"])
            await ctx.reply(embed=embed)
            print(f'[LOGS]- {ban_entry.user.name} has been unbanned.')
            return
    
    await ctx.reply("Member not found in ban list.")

#mute command
@Client.command(name='!mute', description='Mute a member in the server.')
@commands.has_permissions(manage_roles=True)  # Requires manage_roles permission
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    
    if not muted_role:
        # Create the "Muted" role if it doesn't exist
        muted_role = await ctx.guild.create_role(name='Muted', reason='Creating the Muted role')
        
        # Set the permissions for the "Muted" role as needed
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False)
    
    await member.add_roles(muted_role, reason=reason)
    
    embed = discord.Embed(
        title=f"{member.name} has been muted!",
        description=f"Reason: {reason}",
        color=discord.Color.red(),
    )
    embed.set_thumbnail(url=configData["SysopIcon"])
    await ctx.reply(embed=embed)
    print(f'[LOGS]- {member.name} has been muted.')

#Unmute command

@Client.command(name='!unmute', description='Unmute a member in the server.')
@commands.has_permissions(manage_roles=True)  # Requires manage_roles permission
async def unmute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    
    if muted_role in member.roles:
        await member.remove_roles(muted_role, reason=reason)
        embed = discord.Embed(
            title=f"{member.name} has been unmuted!",
            description=f"Reason: {reason}",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {member.name} has been unmuted.')

#Error command
@Client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title=f"Error occurred",
            description=f"{error}",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title=f"Error occurred",
            description=f"{error}",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title=f"Error occurred",
            description=f"{error}",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title=f"Error occurred",
            description=f"{error}",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(
            title=f"Error occurred",
            description=f"{error}",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f"[LOGS]- {error}.")
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title=f"Error occurred",
            description=f"{error}",
            color=discord.Color.red(),
        )
        embed.set_thumbnail(url=configData["SysopIcon"])
        await ctx.reply(embed=embed)
        print(f'[LOGS]- {error}.')
        
    
Client.run(configData['token'])