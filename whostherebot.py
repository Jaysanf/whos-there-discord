from typing import Union
import discord
from discord import channel

class WhosThereBot :
    def __init__(self, token) -> None:
        self.guildLog = {}
        self.userLog = {}
        self.token = token
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.presences = True
        self.client = discord.Client(intents=self.intents)

       
        # Check le login
        
    
    def runMainLoop(self):

        @self.client.event
        async def on_ready():
            print("We have logged in as {0.user}".format(self.client))

             # init guildLog
            for guild in (list(self.client.guilds)):
                self.guildLog[guild.id] = guild
            
        # Add the discord server
        @self.client.event
        async def on_guild_join(guild):
            self.guildLog[guild.id] = guild
            print(f"The guild [{guild.id}] has been added to the log.")


        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            # Check only for DMs
            if isinstance((message.channel), discord.channel.DMChannel):
                my_user =  self.client.get_user(message.author.id)
                if message.content == "who":
                    await self.whosOnline(my_user,message.channel)
                if message.content == "help":
                    await self.help(my_user,message.channel )
                if message.content == "subscribe":
                    await self.subscribe(my_user,message.channel)
                if message.content == "unsubscribe":
                    await self.unsubscribe(my_user,message.channel)
            return
        
        @self.client.event
        async def on_voice_state_update(member, before, after):
          
            for key in self.userLog:
                user = self.client.get_user(int(key))
                
                # If its yourself, no notification
                if int(key) == member.id :
                    continue
                    

                # If the user cant view the channel, no notification will be sent
                if (before.channel is None)and after.channel.guild in self.userLog[key]:
                    member1 = after.channel.guild.get_member(int(key))
                    if after.channel.permissions_for(member1).view_channel == False:
                        continue
                    await user.dm_channel.send(f"User **{member.name}** as join **{after.channel.name}** in **{after.channel.guild.name}**") 

                elif after.channel is None and before.channel.guild in self.userLog[key]:
                    member1 = before.channel.guild.get_member(int(key))
                    if before.channel.permissions_for(member1).view_channel == False:
                        continue
                    await user.dm_channel.send(f"User **{member.name}** as left **{before.channel.name}** in **{before.channel.guild.name}**")


                
                

            
            #if before.afk or after.afk:

                    

        self.client.run(self.token)

    async def whosOnline(self, user, channel):
        mutualGuilds = user.mutual_guilds
        msg = ""
        async with channel.typing():
            for guild in mutualGuilds:
                msg += f"Discord server: {guild.name} \n"
                vcs = (guild.voice_channels)
                for vc in vcs:
                    if vc.members != []:
                        msg += "\t\t" + self.channelFormat(vc) + "\n"
            await channel.send(msg)
        return

    async def help(self, channel):
        pass

    async def subscribe(self,user, channel):
        if f'{user.id}' not in self.userLog:
            self.userLog[f'{user.id}'] = []
        guildSubscribed = self.userLog[f'{user.id}']

        msg = f"Which Discord server you wanna subscribe (Click the corresponding reaction):\n\n"
        async with channel.typing():
            counter = 0 
            for guild in list(set(user.mutual_guilds) - set(guildSubscribed)):

                msg += f"\t\t**{counter}** --> **{guild.name}** \n "

                counter += 1

            
            myMSG = await channel.send(msg)
        # Add a reaction to the the MSG
        counter = 0 
        emojis = ["0️⃣", "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        for guild in list(set(user.mutual_guilds) - set(guildSubscribed)):

            await myMSG.add_reaction(emojis[counter])

            counter += 1

        @self.client.event
        async def on_reaction_add(reaction, user):
            if reaction.message == myMSG and user != self.client.user:
                guildPos = emojis.index(reaction.emoji)
                self.userLog[f'{user.id}'].append(list(set(user.mutual_guilds) - set(guildSubscribed))[guildPos])
                await myMSG.delete()

    async def unsubscribe(self,user,channel):
        self.userLog[f'{user.id}'] = []
        await channel.send("Unsubcribed successfully,")

    def channelFormat(self, channel):
        myStr = f"There is **{len(channel.members)}** member in **{channel.name}** : \n"
        
        for member in channel.members:
            myStr +=  "\t\t\t\t"+ member.name + "\n"
        return myStr

        

    
    
  
