import discord
from discord.ext import commands
import os
import logging
import game_engine               
import preanswer_check                                                                                                                                                                           

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print("Shrimp.ly is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):

    print(f'Message from {message.author}: {message.content}')

    await bot.process_commands(message)

@bot.tree.command(name="begin",description="Begins a Game of Shrimply.py!")
async def begin(interaction: discord.Interaction):
    print("Command Recieved")
    await interaction.response.send_message(f"Game of Shrimp.ly is Starting in 5 Seconds")
    channel_id = interaction.channel_id
    channel = bot.get_channel(channel_id)
    question, answer = game_engine.serve_question()
    await channel.send(f"{question}")
    message = await bot.wait_for('message',check=None,timeout=15)
    print(message.content)
    print(answer)
    result, matched_answer, points = preanswer_check.check_answer(answer,message.content)
    if result == True:
        await channel.send(f"You answered: {matched_answer}... AND IT WAS CORRECT.\n You have been awarded {points} points")
    else:
        await channel.send(f"You answered: {message.content}... and it was wrong :(")

    
    

    



    
bot.run(token, log_handler=handler, log_level=logging.DEBUG)