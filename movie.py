import discord
import time
import datetime
import asyncio
import random
import os


import requests

from discord.ext import commands
from asyncio import timeouts
#from threading import Timer

import logging



import firebase_admin
from firebase_admin import credentials, firestore

from dotenv import load_dotenv

load_dotenv()

###cred = os.getenv("CRED")

cred = credentials.Certificate("cert goes here")



firebase_admin.initialize_app(cred)

db = firestore.client()
print(db)

f = open("placeholder text name whatever you want", "r") #replaced this functionality

cache = f.read()
order = []

#print(cache)
movielist = {}


#next = 0

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
#intents.add_reactions = True

#bot = MyBot(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)


#@bot.tree.command()

#bot.tree.sync()
#bot.tree.add_command(lists)


if cache:
        spl = cache.split(", 'order': ")
        order = spl[-1].strip('["]}').replace("'","").split(', ')
        cache = spl[0]
        print(type(order))
        for x in "'}{":

            cache = cache.replace(x,'')
        #cache = cache.replace(', ', ": ")
        
        cache = cache.split(", ")
     
        
       
        #for x in range(0,len(cache)-1,2):
        for x in cache:
            keyval = x.split(": ", 1)
            movielist[keyval[0]] = keyval[1]  
            #print(movielist)   

#names = [x for x in movielist if x != 'order']
#movielist['order'] = names
movielist['order'] = order
print((movielist))





ctime = time.localtime(time.time() - 71700)
ntime = time.time() + 86400*( 7 - abs(4 + ctime.tm_wday) % 7) - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec - 71700
#print((time.localtime(time.time()+ 86400*(7 - (ctime.tm_wday - 3))+ 72000 - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec)))
#print(ntime - time.time()-71700)
    

print(ntime - (time.time() - 71700) )

print(time.asctime((time.localtime(ntime))),time.asctime(ctime))

x=datetime.datetime.today()



async def movie_ping(client,sec:int):###background task, update this on github
    
    timer = sec
    print( sec)
    print(ctime.tm_yday//7)
    
    while not client.is_closed():
        
        #timer = (ntime - (time.time() - 71700))
        #print(timer)
        timer = sec
        await asyncio.sleep(timer)
        await client.get_channel("placerholder id").send('Movie Night everyone,  ' + movielist['order'][(ctime.tm_yday //7 + 2) % len(movielist['order'])] + ' wants to watch ' + movielist[movielist['order'][(ctime.tm_yday //7 +2)%len(movielist['order'])]])
        sec = time.time() + 86400*( 7 - abs(4 + ctime.tm_wday) % 7) - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec - 71700 - (time.time() - 71700)
        print(sec)     # task runs every 60 seconds


async def search(query,channel,author):
    print(query,author,channel)
    if "movie" or "Movie" not in query:
        query = query+'+movie'
    try:
                response = requests.get(url="apikey"+query)

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

                elif zero["link"].startswith("https://www.imdb.com/title/"):
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

                
        else:
             await ctx.send("You didn't choose a movie to watch")
             
######database###################

@bot.hybrid_command(name="add",description="Suggest movies to randomly pick")
async def add(ctx):


    split = ctx.message.content.split(' ',1)
    print(split)
        
    if len(split) == 2 and split[1]:
        
        try:
            doc_ref = db.collection("Movies").document(str(ctx.author))
            doc_ref.set({"Person": str(ctx.author),"movie": await search(split[1].replace(" ","+"),ctx.channel, ctx.author.name)})
        except:
            return
        
    else:
        await ctx.send("You didn't choose a movie to watch")



@bot.hybrid_command(name="pick",description="Pick from the pool of suggested movies")
async def pick(ctx):
    people = []

    if str(ctx.author) not in ['list of mods']:
        await ctx.send("You don't have permission for this")
        

    stream = db.collection('Movies').stream()
    print(stream)
    output = [(doc.to_dict()) for doc in stream]
    stream = db.collection("Present").stream()
    print(stream)
    people = [list((doc.to_dict()).keys())[0] for doc in stream]
    print(people)


    total = db.collection("Movies").count(alias="all")


    sending = output[random.randint(0,((total.get()[0][0]).value)-1)]
    while(sending['Person'] not in people):
        sending = output[random.randint(0,((total.get()[0][0]).value)-1)]
        print(sending['Person'])
    
    print(sending)
    await ctx.send(str(sending['movie']) + ', ' + str(sending['Person']))
    docs = db.collection("Present").list_documents()
    for doc in docs:
        doc.delete()
    db.collection("Watched").document(sending["movie"]).set({"movie":sending["movie"]})
    db.collection("Movies").document(sending["Person"]).delete()
    
    

@bot.hybrid_command(name="present",description="Mark yourself present for the movie")
async def present(ctx):

    db.collection("Present").document(str(ctx.author)).set({str(ctx.author): True})
    await ctx.send("Marked")

@bot.hybrid_command(name="pool",description="Show all movies that can be randomly picked")
async def pool(ctx):

    stream = db.collection('Movies').stream()
    output = [(doc.to_dict()) for doc in stream]

    send = ""

    for x in output:

        send = send + str(x['movie']) + "\n"
    

    await ctx.send(send)


@bot.hybrid_command(name="past",description="List of movies that were watched")
async def past(ctx):

    stream = db.collection("Watched").stream()
    output = [(doc.to_dict()) for doc in stream]

    send = ""

    for x in output:

        send = send + str(x['movie'] + "\n")

    await ctx.send(send)


#####################database #########################################
        

        


@bot.hybrid_command(name="next",description="Shows who and what movie is next week")
async def next(ctx):

    person = movielist['order'][(ctime.tm_yday  - 11 //7 - 3 ) % len(movielist['order'])]
        
    pmovie =  movielist[person]
        
    await ctx.send('Next movie night is ' +time.asctime(time.localtime(ntime))[:11] + ', ' + person + ' picked the movie ' + pmovie  )



@bot.hybrid_command(name="list",description="Displays everyone's selected movie")
async def all_Movies(ctx):
    output = "All movies: \n"
    for x in movielist:
        if x != 'order':
            output += x + ": " + movielist[x] + "\n"
    
    await ctx.send(output)


    
@bot.hybrid_command(description= "Displays the or der of server members, adding 'random' changes the order")
async def order(ctx,arg=None):
    print(type(ctx.author))

    if arg == None:
        await ctx.send(str(movielist['order'])[1:-1].replace("'",""))
    elif arg == 'random':
        #print((movielist['order']))
        #if type(movielist['order']) == str:
        #    movielist['order'] = movielist['order'].strip("'")
        #    print(type(movielist['order']))

        if str(ctx.author) != 'trapbarackobama':
            print(ctx.author)
            await ctx.send("You're a bum")

        else:
            random.shuffle(movielist['order'])
            #print(type(movielist['order']))
            await ctx.send('New order generated: ' + str(movielist['order'])[1:-1].replace("'",""))
    else:
        await ctx.send("Wrong input, try again")

@bot.hybrid_command(name='offset',description="Inputs : 0\nmove order of members forward or back, add 'forward' or 'back' to command")
async def offset(ctx):

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

@bot.hybrid_command(name='swap',description="move order of members forward or back, add 'forward' or 'back' to command")
async def swap(ctx,arg1,arg2):

    split = ctx.message.content.split(" ", 2)

    if len(split) == 3 and str(ctx.author) == "trapbarackobama":

        neworder = movielist["order"]

        first = neworder.index(arg1)
        second = neworder.index(arg2)

        neworder[first] = str(arg2)
        neworder[second] = str(arg1)
        movielist["order"] = neworder

        await ctx.send("New Order: \n" + str(movielist["order"])[1:-1])

        return

    else:
        await ctx.send("Wrong input, choose two server members")




@bot.hybrid_command(name='sync')
async def sync(ctx):
    #print(ctx.guild)
    if ctx.author.name == 'trapbarackobama':
        try:
            
            await bot.tree.sync()
            print(bot.commands)
        except:
            print('No')
    else:
        #await interaction.response.send_message('You must be the owner to use this command!')
        return


###############end commands##################



@bot.event
async def on_connect():
    
    
    print()
    
    #await print(ctime,[x for x in names],movielist,bot.users) 

@bot.event
async def on_ready():
    
    commands = ""
    commands = commands.join([x + ', ' for x in [x.name for x in bot.tree._get_all_commands()]])
    print(commands[:-8])
  
    
    await bot.change_presence(status=discord.Status.online)
    await bot.get_channel("placeholder id").send("Hello, commands can be used with '!', the slash command menu currently doesn't work\n"
                                              "Available commands: " + commands[:-8])


    if movielist == {}: #For the sake of starting in a new server, initialize storage with each member
        order = [x.name for x in bot.get_guild('placeholder_server').members]
        for x in order:
            movielist[x] == None ## Initialize each member in the dict, without a movie suggestion

        movielist["order"] = order # default movie night order is whatever order the server grabs all users
    
    
    await movie_ping(bot, ntime - (time.time() - 71700))


@bot.event
async def on_message(message):
    print(message.content)
    if message.author == bot.user:
        return
    
   
         
    
    
    await bot.process_commands(message)


    if message.content.startswith('$movie'):
        
        split = message.content.split(' ',1)
        print(split)
        
        
        if len(split) ==2 :
        
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
        if str(message.author.name) == 'placeholdermod':

            #f.close()
            await shutdown()
            await bot.get_channel("placeholder id").send('Shutting down')
            #await bot.change_presence(discord.Status.offline)
            await bot.close()

            #asyncio.sleep(time.time() + 86400*( 7 - abs(4 + ctime.tm_wday) % 7) - ctime.tm_hour*3600 - ctime.tm_min*60 - ctime.tm_sec - 71700 - (time.time() - 72120))
            await bot.connect()

        else:  
            return
            #discord.utils.sleep_until((time.localtime(time.time()+ 86400*(7 - (ctime.tm_wday - 3)))))
            #asyncio.sleep(86400*(7 - (ctime.tm_wday - 3)))
            #idk how to disable this shit

    if message.content.startswith('$delete'):
        print(type(message.author))
        if str(message.author.name) == 'trapbarackobama':
            mess = message.content.split(' ', 1)
            
            del movielist[mess[1]] 

    if message.content.startswith('$next'):
        
        person = movielist['order'][((ctime.tm_yday - 11  //7  - 3)) % len(movielist['order'])]
        
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
            if message.author != 'trapbarackobama':
                print(message.author)
                await message.channel.send("You're a bum")

            else:
                random.shuffle(movielist['order'])
                #print(type(movielist['order']))
                await message.channel.send('New order generated: ' + str(movielist['order'])[1:-1].replace("'",""))
        else:
            await message.channel.send("Wrong input, try again")
            
    
    
    
    ''' 
    Database implemented, old code left in 
    '''
    
@bot.event
async def on_disconnect():
    f.write(str(movielist))
    #f.close()
    await bot.close()
    await bot.change_presence(discord.Status.offline)
    
    #await bot.connect()


async def shutdown():
    await bot.change_presence(status=discord.Status.offline) 




f = open("discord.log", "w")
bot.run('placeholder appid',log_handler=None)
#asyncio.run(shutdown())
f.write(str(movielist))

f.close()


