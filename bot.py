import discord, requests, json
from discord.ext import commands
from discord import app_commands
from requests.auth import HTTPBasicAuth

# Enter your bot token
token = TOKEN
# Enter you bot client secrect
client_secrect = CLIENT_SECRECT
# Initializing the bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Enter your Spotify client id
clientID = CLIENT_ID
# Enter your Spotify client secrect
clientSecrect = CLIENT_SECRECT

# Authorizing to use Spotify's API
url = 'https://accounts.spotify.com/api/token'
data = {'grant_type': 'client_credentials'}
auth = HTTPBasicAuth(clientID, clientSecrect)

response = requests.post(url, data=data, auth=auth)

accessToken = response.json()['access_token']
headers = {"Authorization": f"Bearer {accessToken}"}

# This fuction will be the first to run when you run the bot. That's why the function's name is "on_ready".
@bot.event
async def on_ready():
    print("Bot is up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# A simple slash command to say hello.
@bot.tree.command(name='hello')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Yo {interaction.user.mention}! Nice to see ya!")

# A simple slash that makes the bot say whatever you make it.
@bot.tree.command(name='say')
@app_commands.describe(arg = 'What should I say?')
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said `{arg}`")

# Slash command that will prompt you a user input. You can type in a year and it'll return Spotify's top ten songs from that year.
@bot.tree.command(name='search')
@app_commands.describe(arg = "Year")
async def search(interaction: discord.Interaction, arg: str):
    url = 'https://api.spotify.com/v1/search'
    search = f'?query=year%3A{arg}&type=track&locale=en-US%2Cen%3Bq%3D0.9&offset=0&limit=10'
    fullURL = f"{url}{search}"
    response = requests.get(fullURL, headers=headers)
    data = response.json()
    #print(json.dumps(data, indent=2))
    l = ''
    no = 1
    for i in data['tracks']['items']:
        title = i['name']
        artist = i['artists'][0]['name']
        link = i['external_urls']["spotify"]
        song = f"{no}. '{title}' by {artist}\n{link}\n"
        l += song
        no += 1
    await interaction.response.send_message(f"Here are the top ten songs of {arg}!\n\n{l}")

    

bot.run(token)
