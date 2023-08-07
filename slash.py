import discord, requests, json
from discord.ext import commands
from discord import app_commands
from requests.auth import HTTPBasicAuth

token = 'MTEyMjE5ODU2MTM0MjM1NzU5NA.GKiXbk.8NTosKVsThHoIMih4slq7pAkLtfVtVCWiNt1sE'
client_secrect = '31BT4qbU06AmBdnLNndny_zUAna3vXdM'
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

clientID = '3e6dcddbaf034d09bc29fd04b37fa40f'
clientSecrect = '866f55d35ff14c3797e1f52201f45c09'

url = 'https://accounts.spotify.com/api/token'
data = {'grant_type': 'client_credentials'}
auth = HTTPBasicAuth(clientID, clientSecrect)

response = requests.post(url, data=data, auth=auth)

accessToken = response.json()['access_token']
headers = {"Authorization": f"Bearer {accessToken}"}

@bot.event
async def on_ready():
    print("Bot is up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name='hello')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Yo {interaction.user.mention}! Nice to see ya!")

@bot.tree.command(name='say')
@app_commands.describe(arg = 'What should I say?')
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said `{arg}`")

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