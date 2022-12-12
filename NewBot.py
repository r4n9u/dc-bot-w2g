import discord
import json
import requests
from discord import app_commands

TOKEN = ''
WKEY = ''
GID = 918867350785261618
W2GKeys = {}

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced= False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=GID)) 
            self.synced = True
        print(f"We have logged in as {self.user}.")

bot = client()
tree = app_commands.CommandTree(bot)

@tree.command(guild = discord.Object(id=GID), name = 'w2link', description='Create W2G Room with preloaded Video')
async def createRoom(interaction: discord.Interaction, link: str):
    yt_link = link
    url = 'https://api.w2g.tv/rooms/create.json'
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    data = {'w2g_api_key':WKEY,'share':yt_link,'bg_color':'#133857','bg_opacity':"100"}
    data = requests.post(url=url , headers=headers , params=data).json()
    streamkey = data['streamkey']
    embed=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
    embed.add_field(name="Roomkey: ", value=streamkey, inline=True)
    W2GKeys[interaction.channel.id] = streamkey
    await interaction.response.send_message(embed=embed)

@tree.command(guild = discord.Object(id=GID), name = 'w2room', description='Create W2G Room')
async def createRoom(interaction: discord.Interaction):
    yt_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url = 'https://api.w2g.tv/rooms/create.json'
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    data = {'w2g_api_key':WKEY,'share':yt_link,'bg_color':'#133857','bg_opacity':"100"}
    data = requests.post(url=url , headers=headers , params=data).json()
    streamkey = data['streamkey']
    embed=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
    embed.add_field(name="Roomkey: ", value=streamkey, inline=True)
    W2GKeys[interaction.channel.id] = streamkey
    await interaction.response.send_message(embed=embed)

@tree.command(guild = discord.Object(id=GID), name = 'w2add', description='Updates W2G Room')
async def createRoom(interaction: discord.Interaction, link: str):
    print(W2GKeys)
    newLink = link
    try:
        streamkey = W2GKeys[interaction.channel.id]
        print(streamkey)
    except KeyError:
        error=discord.Embed(title="No room found",  url='https://dino.reuther05.de', color=0x133857)
        error.add_field(name="No room found in this channel: ", value="please use !w2g <link>", inline=False)
        await interaction.response.send_message(embed=error)
        return 
    if len(newLink) == 0:
        error=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
        error.add_field(name="No link found in command: ", value="please use !w2add <link>", inline=False)
        await interaction.response.send_message(embed=error)
        return 
    yt_link = newLink
    url = 'https://api.w2g.tv/rooms/' + streamkey +'/sync_update'
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    data = {'w2g_api_key':WKEY,'item_url':yt_link}
    try:
        requests.post(url=url , headers=headers , params=data).json()
    except:
        print()
    update=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
    update.add_field(name="Room updated: ", value=streamkey, inline=False)
    await interaction.response.send_message(embed=update)


bot.run(TOKEN)