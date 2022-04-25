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
    """Prepare a list of lists of files to upload

    Assumes all files in the target directory are to be uploaded.

    @param dir_path Path to the target directory
    """
    global MAX_MEME_SIZE
    files_in_dir = []
    output = []
    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        # Skip directories
        if os.path.isfile(full_path):
            # Skip large files
            if os.path.getsize(full_path) <= MAX_MEME_SIZE:
                files_in_dir.append(full_path)
    while bool(len(files_in_dir)):
        output.append(files_in_dir[0:10])  # Hard-coded chunk size
        files_in_dir = files_in_dir[10:]
    return output


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
