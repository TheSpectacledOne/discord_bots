# Module imports
# -----------------------------------------------------------------------------


import discord
import os
import sys

from discord.ext import commands


# Constants
# -----------------------------------------------------------------------------


# 8MB max
MAX_MEME_SIZE = 8 * 1024 * 1024


# Function definitions
# -----------------------------------------------------------------------------


def get_size(file_path: str):
    return os.path.getsize(file_path)


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


def read_token(file_path: str) -> str:
    with open(file_path, "r") as fh:
        data = fh.read()
    return data.strip()


def under_8MB(cur_size, file_size):
    global MAX_MEME_SIZE
    if file_size + cur_size < MAX_MEME_SIZE:
        return True
    else:
        return False


# Bot handling
# -----------------------------------------------------------------------------


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


# Main function
# -----------------------------------------------------------------------------


def main():
    global bot
    token = read_token(sys.argv[1])  # Stored in discord_bot_token.txt
    bot.run(token)


# Entrypoint
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
