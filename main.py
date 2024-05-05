import discord
from discord.ext import commands
from datetime import datetime
from sheet import GoogleSheetsAPI
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("UserToName.json", "r") as json_file:
    Dict = json.load(json_file)
json_file.close()

def UserToName(user):
    try:
        return Dict[user]
    except:
        return None

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

API = GoogleSheetsAPI()
spreadsheet_id = os.getenv("SPREADSHEET_ID")

bot = commands.Bot(command_prefix='/', intents=intents, tree_cls=discord.app_commands.CommandTree)

@bot.event
async def on_ready():
    print(f'Bot is ready')
    try:
        sync = await bot.tree.sync()
        print(f"Synced {sync} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")
        
@bot.tree.command(name="ping", description="Replies with pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")
    
@bot.tree.command(name="debt", description="Who did you lend money from?")
async def debt(interaction: discord.Interaction, lender: discord.Member, amount: float, description: str = "\"No description\""):
    borrower_name = UserToName(interaction.user.name)
    lender_name = UserToName(str(lender))
    if borrower_name == None or lender_name == None or borrower_name == lender_name:
        await interaction.response.send_message("Invalid user.")
        return
    API.use_spreadsheet(spreadsheet_id)
    API.create_debt(borrower_name, lender_name, amount, description)
    API.create_log(borrower_name, lender_name, amount, description, False)
    await interaction.response.send_message(f"{interaction.user.display_name} owes {lender.display_name} {amount} for {description}.")
    
@bot.tree.command(name="lend", description="Who did you lend money to?")
async def lend(interaction: discord.Interaction, borrower: discord.Member, amount: float, description: str = "\"No description\""):
    borrower_name = UserToName(str(borrower))
    lender_name = UserToName(interaction.user.name)
    if borrower_name == None or lender_name == None or borrower_name == lender_name:
        await interaction.response.send_message("Invalid user.")
        return
    API.use_spreadsheet(spreadsheet_id)
    API.create_debt(borrower_name,lender_name, amount, description)
    API.create_log(borrower_name, lender_name, amount, description, True)
    await interaction.response.send_message(f"{borrower.display_name} owes {interaction.user.display_name} {amount} for {description}.")
    
bot.run(DISCORD_TOKEN)