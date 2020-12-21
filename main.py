import os
import dotenv
import discord
import berserk
import cairosvg
import chess
import chess.svg

# Make console logging pretty
from rich import print
from rich.traceback import install
install()

# SETUP STUFF HERE

dotenv.load_dotenv()
LICHESS_TOKEN = os.getenv('LICHESS_TOKEN')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
CHESS_GAME_ID = os.getenv('CHESS_GAME_ID')

# DISCORD STUFF HERE

discord_client = discord.Client()

@discord_client.event
async def on_ready():
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    print(f'{discord_client.user} has connected to Discord!')

@discord_client.event
async def on_message(message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if message.author.id == discord_client.user.id:
        return
    
    if message.content.startswith('!board'):
        session = berserk.TokenSession(LICHESS_TOKEN)
        chess_client = berserk.Client(session)
        board = chess.Board()
        game = chess_client.games.export(CHESS_GAME_ID)
        moves = [move for move in game['moves'].split()]

        for move in moves:
            board.push_san(move)

        board_svg = chess.svg.board(board)
        with open('board.svg', 'w') as f:
            f.write(board_svg)
        with open('board.svg', 'rb') as f:
            board_png = cairosvg.svg2png(file_obj=f, write_to='board.png')
        await channel.send(file=discord.File('board.png'))

discord_client.run(DISCORD_TOKEN)


# TODO: Include which player is which color in Discord post
# TODO: Post image every time a move is made