import discord  #### py -3 -m pip install -U discord.py for windows and instructions https://github.com/Rapptz/discord.py
import json
import time

from discord.ext import commands
import logging

f = open("placeholder.txt", "r") ##rename the file to wherever you want to store data

##########initialized

cache = f.read()
movielist = {}

next = 0

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

if cache: ### this is literally just a txt file as a database I'm too lazy and poor to make a database that other people can use
        for x in "'}{":

            cache = cache.replace(x,'')
            #formats text file and removes ' because str.split adds double quotes


        cache = cache.replace(', ', ": ")
        cache = cache.split(": ")
        #separates keys and values to initialize the dict
     
        
       
        for x in range(0,len(cache)-1,2):
         
            movielist[cache[x]] = cache[x+1]     
            print(movielist)   

names = [x for x in movielist]

print(movielist)

f = open("placeholder.txt","w")



ctime = time.localtime(time.time())
ntime = time.asctime(time.localtime(time.time()+ 86400*(7 - (ctime.tm_wday - 3))))[:11] # for $next command

######initialized

print(ntime)

print(time.asctime((ctime)))

    
@bot.event
async def on_connect():
    '''
    empty for now, thinking of a future use
    '''
    
    print()
    
    #await print(ctime,[x for x in names],movielist,bot.users)
    



@bot.event
async def on_ready():
    
    names = [x.name for x in bot.get_guild('placeholder').members]
   
    #print(names,names[(ctime.tm_yday //7 + 1) % len(names)])
    
    #print(names[(ctime.tm_yday //7 + 1) % len(names)])
    #print(f'We have logged in as {bot.user}\n', movielist,"\n",ctime)
    #print(ctime.tm_wday)
    
    
    '''
    this is specifically for the day thursday, comparison can be adjusted to any set day, will probably implemenet a way to choose a day and load it here
    if ctime.tm_wday == 3:
        person = names[(ctime.tm_yday //7 + 2) % len(names)]
        pmovie = movielist[names[(ctime.tm_yday //7 + 2) % len(names)]]
        print(person,pmovie,ctime)
        await bot.get_channel('placeholder').send('@everyone, Movie Night ' + person  + pmovie + 'wants to watch')
        await print(names[(ctime.tm_yday//7 + 2 ) % len(names)]) 
    '''
    #print('Movie Night @everyone,  ' + names[(ctime.tm_yday //7) % len(names)] + 'wants to watch ' + movielist[names[(ctime.tm_yday //7)%len(names)]])
  
    
        

@bot.event
async def on_message(message):
    print(message.content)
    if message.author == bot.user:
        return
  
    if message.content.startswith('$hello'):
        print(message.channel)
        await message.channel.send('Hello!')

    if message.content.startswith('$movie'):
        
        split = message.content.split(' ',1)
        print(split)
        
        if len(split) == 2 :
            
            movielist[message.author.name] = split[1]
            
            print(message.author.name,movielist)
            
            await message.channel.send( str(message.author.name) + ' wants to watch ' + movielist[message.author.name])
    
    if message.content.startswith('$list'):
        output = ""
        for x in movielist:
            output += x + " : " + movielist[x] + "\n"

        await message.channel.send('All movies: \n' + output)

    if message.content.startswith('$close'):
        #just kills the app running in the terminal
        f.write(str(movielist))

        f.close()
        await bot.close()
    
    if message.content.startswith('$delete'):
        #print(type(message.author))
        #will probably adjust to only allow certain roles use this command, its just for the purpose of if anyone changes their server name/nickname
        mess = message.content.split(' ', 1)
            
        del movielist[mess[1]] 

    if message.content.startswith('$next'):
        
        person = names[(ctime.tm_yday + 3 //7) % len(names)]
        
        pmovie =  movielist[person]
        
        await message.channel.send('Next movie night is ' + ntime + ', ' + person + ' picked the movie ' + pmovie  )
    
    
    
    '''
    order of movies(thinking about grabbing order of users based on server roles)
    '''

@bot.event
async def on_disconnect():
    f.write(str(movielist))
    f.close()
    #await bot.get_channel('placeholder').send('Shutting down')
    await bot.close()

bot.run('placeholder',log_handler=None) #bot token question mark
f.write(str(movielist))
f.close()

####lots of f write and closes just to make sure everything saves
