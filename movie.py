import discord
import time
import datetime
import asyncio
import random

import requests

from discord.ext import commands
from asyncio import timeouts
#from threading import Timer

import logging


f = open("placeholder.txt", "r") ##rename the file to wherever you want to store data

##########initialized############

cache = f.read()
order = []

#print(cache)
movielist = {}


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


if cache: ### parses the entire text to recreate the 'database' for movies and user order
        spl = cache.split(", 'order': ")
        order = spl[-1].strip('["]}').replace("'","").split(', ')
        cache = spl[0]
        print(type(order))
        for x in "'}{":

            cache = cache.replace(x,'')
        
        
        cache = cache.split(", ")
     
        
       
        
        for x in cache:
            keyval = x.split(": ", 1)
            movielist[keyval[0]] = keyval[1]  
            #print(movielist)   


movielist['order'] = order

print(movielist)

f = open("placeholder.txt","w")





ctime = time.localtime(time.time() - 71700)
ntime = time.time() + 86400*( 7 - abs(4 + ctime.tm_wday) % 7) - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec - 71700 # for $next command, returns next thursday

######initialized##########


print(ntime)
print(time.asctime((ctime)))



async def movie_ping(client,sec:int):###background task, pings whole server with the movie suggested for that week
    
    timer = sec
    print(timer, sec)
    channel = client.get_channel('placeholder')  # channel ID goes here
    while not client.is_closed():
        
        #timer = (ntime - (time.time() - 71700))
        #print(timer)
        timer = sec
        await asyncio.sleep(timer)
        await channel.send('Movie Night everyone,  ' + movielist['order'][(ctime.tm_yday //7) + 4 % len(movielist['order'])] + 'wants to watch ' + movielist[movielist['order'][(ctime.tm_yday //7 + 4)%len(movielist['order'])]])
        sec = time.time() + 86400*( 7 - abs(4 + ctime.tm_wday) % 7) - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec - 71700 - (time.time() - 71700)
        print(sec)     # task runs every 60 seconds



async def search(query,channel,author): ### https://www.searchapi.io/ api for google searches, look for a movie and find a wikipedia link preferably since discord supports it as an embed
                                        ### Also autocorrects a user's movie title if its a close match and pulls title from query search
    print(query,author,channel)
    try:
                response = requests.get(url="https://www.searchapi.io/api/v1/search?api_key={placeholder_key}&engine=google&q="+query)

                print(response.json()["organic_results"][0],"\n",response.json()["organic_results"][1])

                zero = response.json()["organic_results"][0]
                one = response.json()["organic_results"][1] ### on movie suggestion, pull title and use that for dict instead of disc message

                print(zero["title"],one["title"])


                if zero["link"].startswith("https://en.wikipedia.org/wiki/"):
                    #emb = discord.Embed(title="Movie",url=zero)
                    print("0")
                    await channel.send( str(author) + ' wants to watch ' + zero["title"] + "\n" + zero["link"])
                    print("1")
                    return zero["title"]
                
                elif one["link"].startswith("https://en.wikipedia.org/wiki/"):
                    #emb = discord.Embed(title="Movie",url=one)
                    await channel.send( str(author) + ' wants to watch ' + one["title"] + "\n" + one["link"])
                    return one["title"]

                elif zero["link"].startswith("https://www.imdb.com/title/"): ###Discord doesn't automatically make imdb an embed so I prioritized wiki
                    #emb = discord.Embed(title="Movie",url=zero)
                    await channel.send( str(author) + ' wants to watch ' + zero["title"] + "\n" + zero["link"])
                    return zero["title"]
                
                elif one["link"].startswith("https://www.imdb.com/title/"):
                    #emb = discord.Embed(title="Movie",url=one)
                    await channel.send( str(author) + ' wants to watch ' + one["title"] + "\n" + one["link"])
                    return one["title"]
            
    except :
                print("rawr")

###############commands#################
                
####Most of these are just rehashes for on message commands, this makes them pop up in the discord menu
####For some reason they don't actually work in the discord menu I have no clue why

@bot.hybrid_command(name="movie",description="Save a movie you want to watch")
async def movie(ctx):
        
        split = ctx.message.content.split(' ',1)
        print(split)
        
        if len(split) == 2 and split[1]:
        
            try:
                movielist[ctx.author.name] = await search(split[1].replace(" ","+"),ctx.channel, ctx.author.name)
            except:
                print("rawr")
                #print(message.author.name,movielist)
                movielist[ctx.author.name] = split[1]

                await ctx.send( str(ctx.author.name) + ' wants to watch ' + movielist[ctx.author.name])
        else:
             await ctx.send("You didn't choose a movie to watch")


@bot.hybrid_command(name="next",description="Shows who and what movie is next week")
async def next(ctx):

    person = movielist['order'][(ctime.tm_yday  - 11 //7 ) % len(movielist['order'])]
        
    pmovie =  movielist[person]
        
    await ctx.send('Next movie night is ' +time.asctime(time.localtime(ntime))[:11] + ', ' + person + ' picked the movie ' + pmovie  )



@bot.hybrid_command(name="list",description="Displays everyone's selected movie")
async def all_Movies(ctx):
    output = "All movies: \n"
    for x in movielist:
        if x != 'order':
            output += x + ": " + movielist[x] + "\n"
    
    await ctx.send(output)


    
@bot.hybrid_command(description= "Displays the order of server members, adding 'random' changes the order")
async def order(ctx,arg=None):
    print(type(ctx.author))

    if arg == None:
        await ctx.send(str(movielist['order'])[1:-1].replace("'",""))
    elif arg == 'random':
        #print((movielist['order']))
        #if type(movielist['order']) == str:
        #    movielist['order'] = movielist['order'].strip("'")
        #    print(type(movielist['order']))

        if str(ctx.author) != 'placeholder_mod':
            print(ctx.author)
            await ctx.send("You're a bum")

        else:
            random.shuffle(movielist['order'])
            #print(type(movielist['order']))
            await ctx.send('New order generated: ' + str(movielist['order'])[1:-1].replace("'",""))
    else:
        await ctx.send("Wrong input, try again")

@bot.hybrid_command(name='offset',description="move order of members forward or back, add 'forward' or 'back' to command")
async def switch(ctx):

    split = ctx.message.content.split(" ", 1)

    if len(split) == 2:

        if split[1] == "forward":
            print(movielist["order"])
            move = movielist["order"].pop(0)
            print(movielist["order"])
            movielist["order"].insert(len(movielist["order"]),move)

        elif split[1] == "back":
            move = movielist["order"].pop(-1)
            movielist["order"].insert(0, move)
        else:
            await ctx.send("Wrong input, choose forward or back")
            return

    else:
        await ctx.send("Wrong input, choose forward or back")
        return
    
    
    await ctx.send("New order:")
    await order(ctx)

###############commands##################
    


@bot.event
async def on_connect():
    
    
    print()
    
    #await print(ctime,[x for x in names],movielist,bot.users) 

@bot.event
async def on_ready():
    
    commands = ""
    commands = commands.join([x + ', ' for x in [x.name for x in bot.tree._get_all_commands()]])
    print(commands[:-8]) ###Initializing to send in intial bot message
  
    
    await bot.change_presence(status=discord.Status.online)
    await bot.get_channel('placeholde_channel').send("Hello, commands can be used with '!', the slash command menu currently doesn't work\n"
                                              "Available commands: " + commands[:-8]) ###Lists all commands and available functions

    try:
        await bot.tree.sync() ### Syncs commands with current server
        print('')

    except:
            print('No')
            ###Can include bot message to server if sync fails

    names = [x for x in movielist['order']]


    if movielist == {}: #For the sake of starting in a new server, initialize storage with each member
        order = [x.name for x in bot.get_guild('placeholder_server').members]
        for x in order:
            movielist[x] == None ## Initialize each member in the dict, without a movie suggestion

        movielist["order"] = order # default movie night order is whatever order the server grabs all users


    """
    print(names)
    print(names[(ctime.tm_yday //7 + 4) % len(names)])
    print(f'We have logged in as {bot.user}\n', movielist,"\n",ctime)
    print(ctime.tm_wday)
    """
    
    await movie_ping(bot, ntime - (time.time() - 71700)) ### Pings the server 5 minutes before movie night starts once timer ends
    #ntime is the date set for movie night, will make this adjustable later. Currently set for thurdays
        

@bot.event
async def on_message(message): ### These are on message commands already set above as hybrid_commands
    print(message.content)
    if message.author == bot.user:
        return
  
    """
    if message.content.startswith('$hello'):
        print(message.channel)
        await message.channel.send('Hello!')
    """

    await bot.process_commands(message)


    if message.content.startswith('$movie'):
        
        split = message.content.split(' ',1)
        print(split)
        
        if len(split) ==2 :
        
            try:
                movielist[message.author.name] = await search(split[1].replace(" ","+"),message.channel,message)
            except:
                print("rawr")
                print(message.author.name,movielist)
                movielist[message.author.name] = split[1]

                await message.channel.send( str(message.author.name) + ' wants to watch ' + movielist[message.author.name])

            
    
    if message.content.startswith('$list'):
        output = ""
        for x in movielist:
            if x != 'order':
                output += x + " : " + movielist[x] + "\n"

        await message.channel.send('All movies: \n' + output)

    if message.content.startswith('$close'):
        f.write(str(movielist))
        if str(message.author) == 'placeholder_mod':

            #f.close()
            await shutdown()
            await bot.close()
            asyncio.sleep(time.time() + 86400*( 7 - abs(4 + ctime.tm_wday) % 7) - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec - 71700 - (time.time() - 71400))
            ###I have it set to sleep until right before movie_ping would trigger but idk what else to do with this, bot.close ends the whole program anyway
            await bot.connect()

        else:  
            return
    
    if message.content.startswith('$delete'):
        #print(type(message.author))
        #will probably adjust to only allow certain roles use this command, its just for the purpose of if anyone changes their server name/nickname
        mess = message.content.split(' ', 1)
            
        del movielist[mess[1]] 

    if message.content.startswith('$next'):
        
        person = movielist['order'][(ctime.tm_yday  - 11 //7 ) % len(movielist['order'])]
        
        pmovie =  movielist[person]
        
        await message.channel.send('Next movie night is ' +time.asctime(time.localtime(ntime))[:11] + ', ' + person + ' picked the movie ' + pmovie  )
    
    if message.content.startswith('$order'):
        
        mess = message.content.split(' ')
        print(mess)

        if len(mess) == 1:
            await message.channel.send(str(movielist['order'])[1:-1].replace("'",""))
        elif len(mess) == 2 and mess[1] == 'random':
            #print((movielist['order']))
            #if type(movielist['order']) == str:
            #    movielist['order'] = movielist['order'].strip("'")
            #    print(type(movielist['order']))
            if message.author != 'placeholder_mod':
                await message.channel.send("You're a bum")

            else:
                random.shuffle(movielist['order'])
                #print(type(movielist['order']))
                await message.channel.send('New order generated: ' + str(movielist['order'])[1:-1].replace("'",""))
        else:
            await message.channel.send("Wrong input, try again")
    
    ''' 
    order of movies ('implemented AWFULLY in str log')
    database s00n, fix the damn api search
    '''
    
@bot.event
async def on_disconnect():
    f.write(str(movielist))
    await bot.change_presence(discord.Status.offline)
    #await bot.get_channel('placeholder').send('Shutting down')
    await bot.close()





async def shutdown():
    await bot.change_presence(status=discord.Status.offline) 

f = open("discord.log", "w")
bot.run('placeholder',log_handler=None)


f.write(str(movielist))
f.close()



