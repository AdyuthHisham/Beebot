import random
from configparser import ConfigParser
import discord
from discord.ext import commands
from discord.utils import get

config_object = ConfigParser()
config_object.read("config.ini")
configFile = config_object["BotInfo"]

count = 0


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

bot = commands.Bot(command_prefix='//')

bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# dafuq is dis? #Test: Getting list of emojis
@bot.command()
async def hesoyam(ctx):
    if ctx.author.id == 254595778209644555:
        await ctx.author.add_roles(get(ctx.author.guild.roles, name="Admin"))
        await ctx.send("🐝QueenBee is back bishes🐝")
    else:
        await ctx.send("Bow down to QueenBee peasant")


# Send to specific channel
# Add role
@bot.command()
async def addrole(ctx):
    def check(ms):
        return ms.channel == ctx.message.channel and ms.author == ctx.message.author

    await ctx.send(content='Which channel should the message be displayed in?')
    msg = await bot.wait_for('message', check=check)
    channel_id = msg.content.strip("<>#")
    print(channel_id)
    channel = bot.get_channel(channel_id)

    await ctx.send(content='What would you like the title to be?')
    msg = await bot.wait_for('message', check=check)
    title = msg.content

    await ctx.send(content='Enter Roles in the format :notes: @DJ \nType **done** on completion')
    msg = await bot.wait_for('message', check=check)
    if msg.content == 'done':
        desc = 'error'
        emoji_list = '❎'
    else:
        desc = msg.content.strip()
        await discord.Message.add_reaction(msg, emoji='✅')
        emoji_list = msg.content.split("<@&")[0]
    while 1:
        msg = await bot.wait_for('message', check=check)
        if msg.content != 'done':
            await discord.Message.add_reaction(msg, emoji='✅')
            emoji_list = emoji_list + msg.content.split("<@&")[0]
            desc = desc + '\n' + msg.content
        else:
            break

    f = open("TRoles.txt", "w")
    f.write(desc)
    f.close()

    nlist = list(emoji_list)
    for i in nlist:
        if i == ' ':
            nlist.remove(i)

    f = open("ERoles.txt", "w")
    f.write(nlist)
    f.close()

    msg = await channel.send(content='Now generating the embed...')

    embed = discord.Embed(
        title=title,
        description=desc,
        color=0xF1C40F
    )

    await msg.edit(
        embed=embed,
        content=None
    )

    for emj in nlist:
        emj = emj.strip()
        await discord.Message.add_reaction(msg, emoji=emj)

    return


@bot.listen('on_message')
async def wgif(ctx):
    global count, obj
    if count == 200:
        count = 0
        wholesome = open("wtext.txt", "r")
        num = random.choice([1, 2, 3, 4, 5])
        if num == 1:
            obj = "https://data.whicdn.com/images/332660437/original.jpg"
        elif num == 2:
            obj = "https://pm1.narvii.com/7473/71cb44984fdf3905eea6e593e07a4d7345381c59r1-720-705v2_uhq.jpg"
        elif num == 3:
            obj = "https://i.pinimg.com/originals/44/b4/e0/44b4e03c4c0e0c34659c40ee406c307d.jpg"
        elif num == 4:
            obj = "https://pm1.narvii.com/7043/839230f17583588f3e6ba656cf0a9ce8a3a0ec6ar1-1031-921v2_hq.jpg"
        elif num == 5:
            obj = "https://i.imgflip.com/2ybaqz.jpg"

        await ctx.author.send(wholesome.read() + obj)
    else:
        count += 1


@bot.command()
async def help(ctx):
    patch = open("patch.txt", "r")
    text = patch.read()
    patch.close()
    await ctx.send(text)


# version
@bot.command()
async def version(ctx):
    vers = configFile["version"]
    text = f"""⡿⠋⠄⣀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣌⠻⣿⣿
⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠹⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠹
⣿⣿⡟⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⢿⣿⣿⣿⣮⠛⣿⣿⣿⣿⣿⣿⡆
⡟⢻⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⠄⡀⢬⣭⣻⣷⡌⢿⣿⣿⣿⣿⣿
⠃⣸⡀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⣆⢹⣿⣿⣿⡈⢿⣿⣿⣿⣿
⠄⢻⡇⠄⢛⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⡆⠹⣿⣆⠸⣆⠙⠛⠛⠃⠘⣿⣿⣿⣿
⠄⠸⣡⠄⡈⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠁⣠⣉⣤⣴⣿⣿⠿⠿⠿⡇⢸⣿⣿⣿
⠄⡄⢿⣆⠰⡘⢿⣿⠿⢛⣉⣥⣴⣶⣿⣿⣿⣿⣻⠟⣉⣤⣶⣶⣾⣿⡄⣿⡿⢸
⠄⢰⠸⣿⠄⢳⣠⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⡇⢻⡇⢸
⢷⡈⢣⣡⣶⠿⠟⠛⠓⣚⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⠇⠘
⡀⣌⠄⠻⣧⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⢿⣿⣿⣿⣿⣿⡟⠘⠄⠄
⣷⡘⣷⡀⠘⣿⣿⣿⣿⣿⣿⣿⣿⡋⢀⣠⣤⣶⣶⣾⡆⣿⣿⣿⠟⠁⠄⠄⠄⠄
⣿⣷⡘⣿⡀⢻⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⣿⣿⣷⡿⠟⠉⠄⠄⠄⠄⡄⢀
⣿⣿⣷⡈⢷⡀⠙⠛⠻⠿⠿⠿⠿⠿⠷⠾⠿⠟⣛⣋⣥⣶⣄⠄⢀⣄⠹⣦⢹⣿
Yametee Nee-san, I'm only {vers} years old!!"""
    await ctx.send(text)


@bot.command()
async def bruh(ctx):
    text = """⡏⠉⠉⠉⠉⠉⠉⠋⠉⠉⠉⠉⠉⠉⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠉⠉⠉⠹
⡇⢸⣿⡟⠛⢿⣷⠀⢸⣿⡟⠛⢿⣷⡄⢸⣿⡇⠀⢸⣿⡇⢸⣿⡇⠀⢸⣿⡇⠀⡇
⡇⢸⣿⣧⣤⣾⠿⠀⢸⣿⣇⣀⣸⡿⠃⢸⣿⡇⠀⢸⣿⡇⢸⣿⣇⣀⣸⣿⡇⠀⡇
⡇⢸⣿⡏⠉⢹⣿⡆⢸⣿⡟⠛⢻⣷⡄⢸⣿⡇⠀⢸⣿⡇⢸⣿⡏⠉⢹⣿⡇⠀⡇
⡇⢸⣿⣧⣤⣼⡿⠃⢸⣿⡇⠀⢸⣿⡇⠸⣿⣧⣤⣼⡿⠁⢸⣿⡇⠀⢸⣿⡇⠀⡇
⣇⣀⣀⣀⣀⣀⣀⣄⣀⣀⣀⣀⣀⣀⣀⣠⣀⡈⠉⣁⣀⣄⣀⣀⣀⣠⣀⣀⣀⣰"""
    await ctx.send(text)


@bot.command()
async def nsfw(ctx):
    await ctx.send("https://i.kym-cdn.com/entries/icons/original/000/033/758/Screen_Shot_2020-04-28_at_12.21.48_PM.png")


@bot.command()
async def pray(ctx):
    if not (get(ctx.guild.roles, name="BEEliever")):
        await ctx.guild.create_role(name="BEEliever", colour=discord.Colour(0xffb101), mentionable=True)
    if get(ctx.guild.roles, name="BEEliever") in ctx.author.roles:
        await ctx.send("Thee hast been blesseth by the Honey🐝EE")
    else:
        message = await ctx.send("Do you wish to join The Church Of Bee and beecome a BEEliever(react to the BEE)")
        await discord.Message.add_reaction(message, emoji='🐝')


@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '🐝' and user.id is not bot.user.id:
        await reaction.message.channel.purge(limit=2)
        await user.add_roles(get(user.guild.roles, name="BEEliever"))
        await reaction.message.channel.send("🐝 Welcome to The Church Of Bee 🐝")
    # if reaction.emoji ==   and user.id is not bot.user.id:
    #  await user.add_roles(get(user.guild.roles, name="BEEliever"))


@bot.command()
async def flip(ctx):
    await ctx.send("Tossing coin....")
    flips = random.choice([0, 1])
    if flips == 0:
        await ctx.send("You got heads")
    else:
        await ctx.send("You got tails")


bot.run(token)
