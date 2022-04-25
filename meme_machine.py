import os, sys
import discord
from discord.ext import commands

# 8MB max
max_meme_size = 8*1024*1024

def read_token(file_path: str) -> str:
    with open(file_path, "r") as fh:
        data = fh.read()
    return data.strip()

def get_size(file_path: str):
    return os.path.getsize(file_path)

def under_8MB(cur_size, file_size):
    global max_meme_size
    if file_size + cur_size < max_meme_size:
        return True
    else:
        return False

def make_upload_packages(dir_path):
    files_in_dir = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
    upload_packages = [[]]
    cur_size = 0
    index = 0
    
    for file in files_in_dir:
        file_size = get_size(file)
        if not under_8MB(0, file_size):
            continue

        if not under_8MB(cur_size, file_size) or len(upload_packages[index]) >= 10:
            index += 1
            cur_size = 0
            upload_packages.append([])

        upload_packages[index].append(discord.File(file))
        cur_size += file_size

    if len(upload_packages[index]) == 0:
        upload_packages = upload_packages[:-1]

    return upload_packages

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print("{0.user}, ready to meme!".format(bot))
    #await ctx.send("{0.user}, ready to meme!".format(bot))

@bot.command()
async def test(ctx):
    await ctx.send(file=discord.File(sys.argv[2]))

@bot.command()
async def meme(ctx, meme_type):
    if meme_type == "meme":
        memes = make_upload_packages(sys.argv[3])
    elif meme_type == "jojo":
        memes = make_upload_packages(sys.argv[4])
    else:
        await ctx.send("Where are your memes?")
        return
    
    for meme in memes:
        await ctx.send(files=meme)

token = read_token(sys.argv[1]) # Stored in discord_bot_token.txt
bot.run(token)