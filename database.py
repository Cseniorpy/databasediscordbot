#PYTHON --VERSION --> 3.7.4

import discord
import datetime 
import time
import random
from discord.ext import commands
from discord.utils import get
import emoji 
import sqlite3
import asyncio

#ASSIGNING THE PREFIX FOR THE BOT
bot = commands.Bot(command_prefix='!')
token1 = "NjI3ODY4MDIxNTIzNzQyNzcx.X"
token2 = "ZOSew.3XlIDyGYe_tInnIt-ePUDSyW_Ic"
TOKEN = token1+token2

#EVERY BOT HAS OWN 'HELP' COMMAND DEFAULT
#REMOVE THIS COMMAND FOR CREATE A BRAND NEW ONE 
bot.remove_command('help')



#------------------------------------------------------------------------------------------------#
#                                           EVENT SECTION                                        #
#------------------------------------------------------------------------------------------------#

#WHEN THE BOT IS READY, THE EVENT WILL RISE
@bot.event 
async def on_ready():
    game = discord.Game("Coding Python")
    await bot.change_presence(status=discord.Status.idle, activity=game)


    global public_channel_list
    global channel_bot_test, channel_private_experiments
    channel_bot_test = bot.get_channel(627807374736097310)
    channel_private_experiments = bot.get_channel(627815214422687754)
    public_channel_list = [channel_bot_test,channel_private_experiments]



@bot.event 
async def on_member_join(member):
    welcome_message = """**Otonom Araç Projesi'ne Hoşgeldin {0.name}**\n```Ön Koşul```\n```Bu sunucuda geçirdiğin vakit boyunca kendini farklı alanlarda geliştirmek için birbirinden farklı fırsatlar yakalayabilirsin. Birçok kişiyle tanışabilir ve bilgi alışverişinde bulunabilirsin. Bu ekipte bulunduğun süreçte gösterdiğin çaba ve becerilerin, seni çok iyi yerlere getirecek. Eğer sen de kendini geliştirmek, ve bu Projenin gerçek bir üyesi olmak istiyorsan Ön Koşul'u okuduğunu onaylamalısın.. Unutma! her bir sohbet kayıt altına alınmaktadır..```""".format(member)
    channel = bot.get_channel(627921483934466072)
    msg_send = await channel.send(welcome_message)
    r1 = '\U00002714'
    #r2 = '\U00002716'
    reactions = [r1]
    await asyncio.sleep(3)
    for i in reactions:
        await msg_send.add_reaction(i)


#THIS EVENT NOTIFIED THE SPECIFIED CHANNELS WHEN A CHANNEL DELETED
@bot.event 
async def on_guild_channel_delete(channel):
    channel_chat = bot.get_channel(627812771450454046)
    await channel_chat.send("The channel named **{}** has been removed.. ".format(channel))

#THIS EVENT FOR DATABASE
#THE PURPOSE IS SAVING THE WHOLE DATA IN THE SERVER
#THE DATA INCLUDES [MESSAGE CONTENT]//[MESSAGE TIME]//[NAME OF THE AUTHOR]//[ID OF THE AUTHOR]
@bot.event 
async def on_message(message):
    
    #DECLAIRING THE VARIABLES FOR TABLE IN DATABASE
    current_time = datetime.datetime.now()
    self_user = message.author 
    #THIS FORMULA IS FOR SPECIFIED USER WHO SENT A MESSAGE
    user_name_in_database = f"{self_user}_name"

    #WITH THIS METHOD, THE BOT ITSELF CAN BE BLOCK 
    if self_user.id != 627810845971316737 and self_user.id != 627868021523742771:
        connect_database = sqlite3.connect('/root/autonomous/discord/{}.sqlite'.format(user_name_in_database))
        cursor_database = connect_database.cursor()

        table = """CREATE TABLE IF NOT EXISTS users
        (Name, ID, Message, Time)"""

        cursor_database.execute(table)
        cursor_database.execute("INSERT INTO users VALUES(?,?,?,?)",(self_user.name, self_user.id, message.content, current_time))
        connect_database.commit()

        cursor_database.execute("""SELECT * FROM users WHERE Name= '{}'""".format(user_name_in_database))
        #CHOOSE THE FETCH FOR THE DIFFERENT PURPOSES
        #THIS SECTION IS NOT REQUIRED FOR THE CODE'S CURRENT SITUATION 
        #fetched_one = cursor_database.fetchone()
        

        try:
            cursor_database.execute("UPDATE users SET Time = ?", (current_time))
        except ValueError:
            pass
        
        try:
            cursor_database.execute("UPDATE users SET Message = ?", (message.content))
        except sqlite3.ProgrammingError:
            pass


        
    #IT MUST BE IN THE on_message() EVENT
    #IF NOT, THE COMMANDS WON'T WORK PROPERLY
    await bot.process_commands(message)

"""
#SAVES THE INSULTING USERS IN HERE
insulting_users = []
#DELETE THE BAD WORDS FROM THE SERVER
#THIS IS REQUIRED IF MULTIPLE on_message() IN A SINGLE CODE
@bot.listen()
async def on_message(message):
    warn_message = "That was the last warn!"
    embed = discord.Embed(title='',description=warn_message, color = 0xcc1b18)
    insulting_words = []
    for i in insulting_words:
        if i in message.content.lower():
            await message.channel.purge(limit=1)
            await message.channel.send(embed=embed)
            await asyncio.sleep(2)
            await message.channel.purge(limit=10)
            insulting_users.append(message.author.id)
            if message.author.id in insulting_users:
                pass 
"""

#THIS IS FOR THE CLASSIC RULE CHANNEL WHEN AN USER ENTERS TO THE SERVER
#WITH THIS EVENT, THE USER MUST ACCEPT THE RULES BEFORE ENTERING THE SERVER'S CHANNELS
@bot.event 
async def on_reaction_add(reaction, user):
    guild = reaction.message.guild
    channel = bot.get_channel(627921483934466072)
    role = discord.utils.get(guild.roles, name='newbie')
    emj_approve = '\U00002714'
    if reaction.message.channel == channel: 
        if user.id != 627868021523742771:          
            if reaction.emoji == emj_approve:               
                await user.add_roles(role)
                channel_welcome = bot.get_channel(627812771450454046)
                await channel_welcome.send("Hoşgeldin {} :smile:".format(user.mention))


#------------------------------------------------------------------------------------------------#
#                                                                                                #
#------------------------------------------------------------------------------------------------#









#------------------------------------------------------------------------------------------------#
#                                         COMMAND SECTION                                        #
#------------------------------------------------------------------------------------------------#

"""
#THIS SHOWS THE SERVER'S INFO
@bot.command()
async def server(ctx):

    #ID BELONGS TO DEVELOPER
    server_admin = bot.get_user(ID)
    server = ctx.author.guild
    server_member_count = server.member_count

    embed = discord.Embed(title=f'**{str(server).upper()}**', description='', color = 0x32a8a4)
  
    embed.add_field(name='**Admin**', value=f'```{server_admin.name}```')
    embed.add_field(name='**Count of member**', value=f'```{server_member_count}```')
    embed.add_field(name='**Birthday of the Server**', value='```29/08/19```')

    await ctx.send(embed=embed)
"""
"""
#WITH THIS COMMAND, THE USER WHO HAS PERMISSION CAN REMOVE MESSAGES IN A CHANNEL
@bot.command()
async def clear(ctx, amount: int):

    user_list = [ID,ID2]
  
    if ctx.author.id in user_list:
        await ctx.channel.purge(limit = amount)
    else:
        await ctx.send("You can't use this command .. ")
"""

#THIS IS FOR RESIZED AVATAR IMAGE OF THE USER 
@bot.command()
async def profil(ctx):

    if not ctx.channel in public_channel_list:
        await ctx.channel.send("**Bu kanalı kullanmalısın :point_right: {0.mention}**".format(channel_bot_test))

    else:

        try:
        
            user = ctx.author # Fake snowflake, will not work
            if not user:
                return # Can't find the user, then quit
            profile_picture = user.avatar_url
            embed=discord.Embed(title=ctx.author.name, description='' , color=0xecce8b)
            embed.set_image(url=(profile_picture))
            await ctx.send(embed=embed)
        
        except sqlite3.OperationalError:
            await ctx.send("**Operational Error..**")


"""
@bot.command()
async def help(ctx):
    user = ctx.author 
    embed = discord.Embed(title='**Python Help Server**', description='', color=0x2dbbeb)
    embed.add_field(name='**hey**', value='```Greets the user```')
    embed.add_field(name='**profile**', value="```Shows the User's profile```")
    embed.add_field(name='**clear**', value="```Removes messages```")
    embed.add_field(name='**server**', value="```Shows the Server's info```")
    
    await user.send(embed=embed)

"""

#------------------------------------------------------------------------------------------------#
#                                                                                                #
#------------------------------------------------------------------------------------------------#



bot.run(TOKEN)
