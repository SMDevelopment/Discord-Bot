# Work with Python 3.6
import discord

TOKEN = ''

client = discord.Client()

global botPrefix
botPrefix='.'

global drunkLevel
drunkLevel=0


def drunkify(defMsg,drunkLevel):
    import random as r
    import string as s
    spacePos=[]
    wordStartEnd=''
    
    spaces=defMsg.count(' ') #counting the spaces. Every character left and right of a space is a safe letter
    for i in range(0,len(defMsg)): #Linear search for the spaces
        if defMsg[i]==' ':
            space=i
            wordStart=space-1
            wordEnd=space+1
    
    safeLetters=[0,wordStart,wordEnd] #storing the safe letters
    changingLetters=r.randint(1,(len(defMsg)-spaces)) #randomising the amount of changed letters
    changingLetters=changingLetters/2+drunkLevel #The formula is split accross 2 lines for readability

    counter=0
    changedCount=0
    while counter!=len(defMsg) and changedCount!=changingLetters: #The loop terminates when the max amount of letters has changed or if the program runs out of letters to change
        changing=r.randint(0,2) #There is a 2:1 chance that the letter will change
        if changing>0:
            if defMsg[counter] not in safeLetters:
                msg=defMsg.replace(defMsg[counter],r.choice(s.ascii_lowercase[:26]))
        counter+=1
    return msg

@client.event
async def on_message(message):
    global drunkLevel
    global botPrefix
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return 

    #who are you
    if message.content.startswith('%swhoareyou' %botPrefix):
        msg = drunkify('I am Comrade Dimitri! I am a merry slav that enjoys vodka and killing capitalists! I am a work in progress, currently being developed by @Legless#0972 {0.author.mention}'.format(message),drunkLevel)
        await client.send_message(message.channel, msg)

    if message.content.startswith('%shelp' %botPrefix):
        msg=('''{0}takeshot : you share some vodka with me. I will get more drunk and begin to make typos as I get more and more drunk. Can only happen once every 15 min.
{1}whoareyou : you ask me who I am
{2}help : lists commands'''.format(botPrefix,botPrefix,botPrefix))
        await client.send_message(message.channel,msg)

    #Scrapped due to difficulties locking to the admins
##    if message.content.startswith("%sbotprefix" %botPrefix):
##        if ctx.message.author.server_permissions.administrator==True:
##            botPrefix=message.content[11]
##            print(botPrefix)
##            msg=drunkify("The command prefix has been changed to %s, Comrade" %botPrefix,drunkLevel)
##            await client.send_message(message.channel,msg)
##
##        else:
##            msg=drunkify('You do not have permission to do that! Ask the admin to use this commadn in your stead, Comrade {0.author.mention}'.format(message),drunkLevel)
##            await client.send_message(message.channel,msg)

    #take shot
    if message.content.startswith('%stakeshot'%botPrefix):
        if drunkLevel==0: #starting the cooldown if it isn't already active
            drunkLevel+=1
            import time as t
            global cooldownStart
            cooldownStart=t.time()
            msg=drunkify('*takes a shot of vodka* Thank you Comrade {0.author.mention}! Dimitri is very happy!'.format(message),drunkLevel)
            await client.send_message(message.channel,msg)

        else:
            import time as t
            cooldownEnd=t.time()
            cooldownDuration=((cooldownEnd-cooldownStart)/60)
            if cooldownDuration>=15:
                msg=drunkify('*takes a shot of vodka* Thank you Comrade {0.author.mention}! Dimitri is very happy!').format(message)
                await client.send_message(message.channel,msg)
            else:
                msg=drunkify('Dimitri no want more vodka! {0.author.mention}'.format(message),drunkLevel)
                await client.send_message(message.channel,msg)
    #music
    if message.content.startswith("%smusic" %botPrefix):
        import ctx
        import random as r
        songChoice=r.randint(0,1)
        if songChoice==0:
            url='https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwjAu7nh_7_eAhVrAcAKHVfrDPgQwqsBMAB6BAgEEAQ&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DBnTW6fZz-1E&usg=AOvVaw2lyjzAilr1363eldkUN9-f'
        else:
            url='https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwj60tKegMDeAhXLJsAKHaHBBvEQ3ywwAHoECAAQBA&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DU06jlgpMtQs&usg=AOvVaw2BX0Z1iO9bEPuy0zNpRXnb'
        
        author = message.author
        voice_channel = author.voice_channel
        vc = await client.join_voice_channel(voice_channel)

        player = await vc.create_ytdl_player(url)
        player.start()

        msg=drunkify("I will play some music for you, Comrade {0.author.mention}".format(message),drunkLevel)



@client.event
async def on_ready():   
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
