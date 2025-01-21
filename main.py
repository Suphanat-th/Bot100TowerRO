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
data_web_costume = data["Costume"]
dataCareerClass = data["Class"]
    
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
    chanel_id = interaction.channel.id
    if chanel_id == 1101698840475742228 or chanel_id == 1330807911995277404 : 
        str = '### __The Endless Tower. __ ### \n'
        await interaction.response.send_message(content = str)

        for entry in data_array:
            sortedCharactor = sorted(entry["Charactor"], key=lambda x: x['DateTime'])
            str = ''
            str += f"<@{entry['Id']}>\n"
            for chrt in sortedCharactor:
                # ใส่ข้อมูล
                # Create a datetime object

                next_dt = datetime(chrt["Year"], chrt["Month"], chrt["Day"],
                            chrt["Hour"], chrt["Min"], chrt["Sec"])
                # Prev 7 days
                prev_dt = next_dt + timedelta(days=-7)

                pre_date = prev_dt.strftime("%a %d %b %Y (%H:%M)")
                next_date = next_dt.strftime("%a %d %b %Y (%H:%M)")
                difDateToday = days_between_Today(next_dt.strftime("%Y-%m-%d"))


                str += "\n"
                str += f">{dataCareerClass[chrt['Occupation']]}"
                str += f"> ลงไปล่าสุด : {pre_date}\n"

                if difDateToday>=0 :
                    if difDateToday==0: # Today
                        str += f"> ลงได้อีกครั้ง : ```fix\n{next_date}```\n"
                    else : # Not Active
                        str += f"> ลงได้อีกครั้ง : ```diff\n+ {next_date}```\n"  
                else : # Can quest
                    str += f"> ลงได้อีกครั้ง : ```diff\n- {next_date}```\n"  

                str += '\n'

            await interaction.followup.send(content=str)
    else :
        return


@bot.tree.command(name='costume',description="Go to link costume ! ")
async def costumecommand(interaction):
        await interaction.response.send_message(data_web_costume)



# ///////////  Func ///////////////


def days_between_Today(d1):
    d2 = datetime.now("%Y-%m-%d")
    return (d2 - d1).days

# /////////// END Func ////////////// 

server_on()
bot.run(os.getenv('TOKEN'))
