import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

import json
from datetime import datetime, timedelta

# Load JSON file
with open('./100tower.json', 'r') as file:
    data = json.load(file)
# Access the "Data" array
data_array = data["Data"]
    
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())


# //////////////////// Bot Event /////////////////////////
# คำสั่ง bot พร้อมใช้งานแล้ว
@bot.event
async def on_ready():
    print("Bot Online!")
    print("555")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")




# แจ้งคนเข้า -ออกเซิฟเวอร์

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1140633489520205934) # IDห้อง
    text = f"Welcome to the server, {member.mention}!"

    emmbed = discord.Embed(title = 'Welcome to the server!',
                           description = text,
                           color = 0x66FFFF)

    await channel.send(text) # ส่งข้อความไปที่ห้องนี้
    await channel.send(embed = emmbed)  # ส่ง Embed ไปที่ห้องนี้
    await member.send(text) # ส่งข้อความไปที่แชทส่วนตัวของ member


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1140633489520205934)  # IDห้อง
    text = f"{member.name} has left the server!"
    await channel.send(text)  # ส่งข้อความไปที่ห้องนี้



# คำสั่ง chatbot
@bot.event
async def on_message(message):
    mes = message.content # ดึงข้อความที่ถูกส่งมา
    if mes == 'hello':
        await message.channel.send("Hello It's me") # ส่งกลับไปที่ห้องนั่น

    elif mes == 'hi bot':
        await message.channel.send("Hello, " + str(message.author.name))

    await bot.process_commands(message)
    # ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ




# ///////////////////// Commands /////////////////////
# กำหนดคำสั่งให้บอท



# Slash Commands
@bot.tree.command(name='qtower', description='List of quest endless tower.')
async def qtowercommand(interaction):
    emmbeds = []
    title ='The Endless Tower.'
    description = 'รายละเอียดวันและเวลาเควสของแต่ละคน'
    color = 0x66FFFF
    
    

    for entry in data_array:
        # ใส่ข้อมูล
        # Create a datetime object

        emmbed = discord.Embed(title=title,
                       description=description,
                       color=color,
                       timestamp= discord.utils.utcnow())

        dt = datetime(entry["Year"], entry["Month"], entry["Day"])
        # Add 7 days
        next_dt = dt + timedelta(days=7)

        pre_date = dt.strftime("%a %d %b %Y")
        next_date = next_dt.strftime("%a %d %b %Y")
        emmbed.add_field(name='*'+entry["Name"]+'*', value='', inline=False)
        emmbed.add_field(name='', value='__Lasted Date__ : `'+pre_date+'`', inline=True)
        emmbed.add_field(name='', value='__Next Date__ : `'+next_date+'`', inline=True)
        emmbed.add_field(name='',value='_____', inline=False)

        emmbeds.append(emmbed)

    await interaction.response.send_message(embeds = emmbeds)


@bot.tree.command(name='name')
@app_commands.describe(name = "What's your name?")
async def namecommand(interaction, name : str):
    filtered = [entry for entry in data_array if entry["Name"].lower() == name.lower()]
    if filtered:
         # Extract the first matching entry
        entry = filtered[0]
        # Create a datetime object
        dt = datetime(entry["Year"], entry["Month"], entry["Day"])
        formatted_date = dt.strftime("%d-%m-%Y")
        await interaction.response.send_message(f"Hello {name} {formatted_date}")




server_on()
bot.run(os.getenv('TOKEN'))
