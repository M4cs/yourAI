import discord, datetime
import gpt_2_simple as gpt2
import asyncio, random, string


sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='discord') # The name of your checkpoint

YOURNAME = "yourdiscordname"

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Activity(name="How to Become Human", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
    if client.user.mention in message.content.replace('<@!', '<@'):
        if message.author == client.user:
            return
        else:
            if client.is_ready:
                uses_con = False
                async with message.channel.typing():
                    if "makeconvo" in message.content:
                        print("Gen Convo")
                        uses_con = True
                        results = gpt2.generate(sess, run_name='discordlarge', temperature=0.9, nsamples=1, batch_size=1, prefix=message.author.name + ":\n" + message.content + "\n\n", length=350, include_prefix=True, return_as_list=True)
                        await message.channel.send("```\n" + str('=' * 20).join(results) + "\n```")
                    else:
                        print("Generating")
                        final = ''
                        prefix = ""
                        last_author = ""
                        old = await message.channel.history(limit=9).flatten()
                        old.reverse()
                        for msg in old:
                            if last_author == msg.author.name:
                                if len(msg.mentions) > 0:
                                    for mention in msg.mentions:
                                        msg.content.replace("<@!" + str(mention.id) + ">", "@" + mention.name)
                                prefix = prefix + msg.content + "\n"
                            else:
                                if len(msg.mentions) > 0:
                                    for mention in msg.mentions:
                                        msg.content.replace("<@!" + str(mention.id) + ">", "@" + mention.name)
                                last_author = msg.author.name
                                prefix = prefix + "\n\n" + msg.author.name + ":\n" + msg.content + "\n"
                        while True:
                            results = gpt2.generate(sess, run_name='discordlarge', temperature=0.9, nsamples=3, batch_size=3, prefix=prefix + "\n\n" + YOURNAME + ":\n", length=250, return_as_list=True, include_prefix=False, truncate="\n\n")
                            res_split = random.choice(results).split('\n')
                            ok = []
                            for r in res_split:
                                if not r.endswith(":") and len(r) > 2 and "http" not in r:
                                    ok.append(r)
                            if len(ok) > 0:
                                break
                        for i, msg in enumerate(ok):
                            if i == (len(ok) -1):
                                await asyncio.sleep(random.randint(0,1))
                                await message.channel.send(msg)
                            else:
                                async with message.channel.typing():
                                    await message.channel.send(msg)
                                    await asyncio.sleep(random.randint(1, 3))                   
            else:
                return



client.run('YOUR DISCORD TOKEN')
