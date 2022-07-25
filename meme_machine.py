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


def make_upload_packages(dir_path: str) -> list:
    """Prepare a list of lists of files to upload

    Assumes all files in the target directory are to be uploaded.  Sets a cap
    of 8MB per chunk.  Trims files > 8MB before sifting into chunks.

    TODO:
    * Clarify whether the limit is 8MB per chunk or 8MB per file

    @param dir_path Path to the target directory
    @return List of lists; list of chunks of filenames for upload
    """
    global MAX_MEME_SIZE
    chunk_size = 0
    files_in_dir = []
    output = [[]]
    for filename in os.listdir(dir_path):
        full_path = os.path.join(dir_path, filename)
        # Skip directories
        if os.path.isfile(full_path):
            # Skip large files
            size = os.path.getsize(full_path)
            if size <= MAX_MEME_SIZE:
                files_in_dir.append((discord.File(full_path), size))
    # Iterate over the file data
    for (file, size) in files_in_dir:
        # If len(chunk) > 9 or new chunk size > max., open a new chunk
        if (len(output[-1]) > 9) or ((chunk_size + size) > MAX_MEME_SIZE):
            output.append([])
            chunk_size = 0
        # Push to the last chunk and increase chunk size
        output[-1].append(file)
        chunk_size += size
    # Trim last list if empty
    # NOTE: This probably will never occur, given the algorithm above
    if len(output[-1]) == 0:
        return output[:-1]
    return output


def read_token(file_path: str) -> str:
    with open(file_path, "r") as fh:
        data = fh.read()
    return data.strip()


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
