import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

import json
from datetime import datetime, timedelta,timezone
import pytz
import asyncio

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
async def on_member_remove(member):
    channel = bot.get_channel(1330807911995277404)  # IDห้อง
    text = f"เจ้านายยยยย ท่าน {member.name} ได้หนีจาก Discord เราไปแล้วเมี๊ยววว TT"
    await channel.send(text)  # ส่งข้อความไปที่ห้องนี้



# คำสั่ง chatbot
@bot.event
async def on_message(message):
    # mes = message.content # ดึงข้อความที่ถูกส่งมา
    # if mes == 'hello':
    #     await message.channel.send("Hello It's me") # ส่งกลับไปที่ห้องนั่น

    # elif mes == 'hi bot':
    #     await message.channel.send("Hello, " + str(message.author.name))

    await bot.process_commands(message)
    # ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ




# ///////////////////// Commands /////////////////////
# กำหนดคำสั่งให้บอท



# Slash Commands
@bot.tree.command(name='qtower', description='List of quest endless tower.')
async def qtowercommand(interaction):
    chanel_id = interaction.channel.id
    if chanel_id == 1101698840475742228 or chanel_id == 1330807911995277404 : 
        embedVar = discord.Embed(title="### __The Endless Tower. __ ###", description="รายชื่อร้อยชั้นของแต่ละคน", color=0x00ff00)
        embedVar.add_field(name=f":x:", value="ไม่สามารถลงได้", inline=False)
        embedVar.add_field(name=f":white_check_mark:", value="ลงได้", inline=False)
        embedVar.add_field(name=f":watch:", value="ใกล้จะถึงเวลาแล้ว อีกไม่กี่ชั่วโมง", inline=False)
        await interaction.response.send_message(embed = embedVar)

        for entry in data_array:
            sortedCharactor = sorted(entry["Charactor"], key=lambda x: x['DateTime'])
            str = ''
            str += f"<@{entry['Id']}>\n"
            for chrt in sortedCharactor:
                # ใส่ข้อมูล
                # Create a datetime object


                next_dt = datetime(chrt["Year"], chrt["Month"], chrt["Day"],
                            chrt["Hour"], chrt["Min"], chrt["Sec"])
                difHoursToday = hours_between_Today(pytz.timezone('Asia/Bangkok').localize(next_dt))
                # Prev 7 days
                prev_dt = next_dt + timedelta(days=-7,hours=-1)

                pre_date = prev_dt.strftime("%a %d %b %Y (%H:%M)")
                next_date = next_dt.strftime("%a %d %b %Y (%H:%M)")

                str += "\n"
                str += f"> **__{dataCareerClass[chrt['Occupation']]}__** \n"
                str += f"> hours_int {difHoursToday} \n"
                str += f"> ลงไปล่าสุด : {pre_date}\n"

                if difHoursToday <= 0 : # Activate Quest
                    str += f"> ลงได้อีกครั้ง : {next_date} :white_check_mark: \n"  
                elif difHoursToday > 0 and difHoursToday<= 12: # Wait Quest
                    str += f"> ลงได้อีกครั้ง : {next_date} :watch: \n"
                else :  # Not Pass Quest
                    str += f"> ลงได้อีกครั้ง : {next_date} :x: \n"

                str += '\n'

            await interaction.followup.send(content=str)
    else :
        return


@bot.tree.command(name='costume',description="Go to link costume ! ")
async def costumecommand(interaction):
        await interaction.response.send_message(data_web_costume)



# ///////////  Func ///////////////


def hours_between_Today(qdt):
    qdt = qdt.astimezone(pytz.timezone('Asia/Bangkok'))  # Next Quest 
    current_dt = datetime.now(pytz.timezone('Asia/Bangkok'))  # DateTime Now
    # Activate Quest = current_dt >= quest
    # Can't Activate Quest = current_dt < quest
    # -,0 = can activate
    return (qdt-current_dt).total_seconds()/3600  

# /////////// END Func ////////////// 

server_on()
bot.run(os.getenv('TOKEN'))
