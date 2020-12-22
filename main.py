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
DISCORD_SERVER_ID = int(os.getenv('DISCORD_SERVER_ID'))
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
CHESS_GAME_ID = os.getenv('CHESS_GAME_ID')

# Make game board
board = chess.Board()

# Setup lichess connection
session = berserk.TokenSession(LICHESS_TOKEN)
chess_client = berserk.Client(session)

# Get game info
game = chess_client.games.export(CHESS_GAME_ID)

# DISCORD STUFF HERE
discord_client = discord.Client()

@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')

    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    stream = chess_client.board.stream_game_state(CHESS_GAME_ID)

    for event in stream:
        moves = [move for move in event['state']['moves'].split()] # Get list of moves in game state
        for move in moves:
            board.push_san(move) # Add each move to the board
        board_svg = chess.svg.board(board) 
        with open('board.svg', 'w') as f:
            f.write(board_svg) # Make .svg of board
        with open('board.svg', 'rb') as f: 
            board_png = cairosvg.svg2png(file_obj=f, write_to='board.png') # Convert .svg to .png
        
        white = event['white'].get('name') # Get white player
        black = event['black'].get('name') # Get black player

        message = f'White pieces: {white}\nBlack pieces: {black}\nTurn #: {len(moves)}\n'
        
        await channel.send(content=message, file=discord.File('board.png')) # Post board image to Discord channel

discord_client.run(DISCORD_TOKEN)
