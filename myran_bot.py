  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import multiprocessing
import threading
import concurrent

BOT_OWNER_ROLE = 'runner' # change to what you need
#BOT_OWNER_ROLE_ID = "503197827556704268" 
  
 

 
oot_channel_id_list = [
"698032380577054741","697321259502927923","698075836451913748","681891490208677958","626458458064945164","694528602586480722","569420128794443776","650009503453937693"
]

answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 626
nomarkscore = 515
markscore = 411

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Myran Bot is Ready")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        
        self.embed=discord.Embed(title="Hq Eraser",description = "",colour = discord.Colour.red())
        self.embed.add_field(name="**Correct Answer**", value="0", inline=False)
        self.embed.add_field(name="**Erase Answer**", value="0", inline=False)
        self.embed.set_footer(text='Hq Eraser || Myran')
        

        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        #one_check = ""
        #two_check = ""
        #three_check = ""
        right_answer = "?"
        not_answer = "?"
        

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        right_answer = '?'
        not_answer = ' ? '
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        #global wrong             

        if highest > 0:
            if answer == 1:
                #one_check = ""
                right_answer = "``:one:`` ``✅``"
            else:
                #one_check = ""
                not_answer = "``:one:`` ``❌`` "

            if answer == 2:
                #two_check = " "
                right_answer = "``two`` ``✅``"
            else:
                #one_check = ""
                not_answer = "``two`` ``❌``"

            if answer == 3:
                #three_check = "  "
                right_answer = "``:three:`` ``✅`` "
            else:
                #one_check = ""
                not_answer = "``:three:`` ``❌`` "
     

            

        #if lowest < 0:
            #if answer == 1:
                #one_cross = ""
                #not_answer = "Not :one: "

           # if answer == 2:
                #two_cross = ""
                #not_answer = "Not :two: "

            #if answer == 3:
                #three_cross = "" 
               # not_answer = "Not :three: "          
 
        #self.embed.set_field_at(0, name="**__OPTION 1__**", value="**{0}.00**{1}".format(lst_scores[0], one_check))
        #self.embed.set_field_at(1, name="**__OPTION 2__**", value="**{0}.00**{1}".format(lst_scores[1], two_check))
        #self.embed.set_field_at(2, name="**__OPTION 3__**", value="**{0}.00**{1}".format(lst_scores[2], three_check))
        #self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/621954596402888724/657871070841405440/GIF-191030_000606.gif")
        #self.embed.set_footer(text='©With❤by『Dèv |༒☬A̴t̴a̴n̴u̴A̴D☬༒』#2471',icon_url='https://cdn.discordapp.com/attachments/621954596402888724/648951259251867681/GIF-191125_094448.gif')
        self.embed.set_field_at(0, name="**Correct Answer**", value=right_answer) 
        self.embed.set_field_at(1, name="**Erase Answer**", value=not_answer) 


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Myran Bot is ready")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="With『Dèv |༒☬A̴t̴a̴n̴u̴A̴D☬༒』#2471|| -lo"))

    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "hq":
            await message.delete()
            if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
                self.embed_msg = None
                await self.clear_results()
                await self.update_embeds()
                self.embed_msg = \
                    await message.channel.send('',embed=self.embed)
                #await self.embed_msg.add_reaction("")
                #await self.embed_msg.add_reaction("")
                #await self.embed_msg.add_reaction("")
                self.embed_channel_id = message.channel.id
            else:
                await message.channel.send("**Fuck!** You Not Have permission To Use This **cmd!** :stuck_out_tongue_winking_eye:")
            return

         
        if message.content.lower() == "role":
          await message.delete()
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
              embed = discord.Embed(title="**__Rule Name__ = *runner*", color=0x0FF14)
              await message.channel.send(embed=embed)
          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('NzA1NDYwNzAyODk0MzU4NjA4.XqsCrg.OsCo1Q17KeBNRGOL4A-YFzwdrFw'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('NTQ0NTY3ODkyNjk2NjI5MjU4.XoVa6g.VbiS89IQEumU4NKSaApofNBj8-s',
                                   bot=False))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=2)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()
