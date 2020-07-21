# yourAI
GPT-2 Discord Bot and Steps to Train Something Like You

## My Environment (Important to Read)

I finetuned my gpt2 models locally on a RTX 2080 Super. Overclocked to around 1550MHz of memory allocated. With this using the `355M` (Medium sz) Model, I was able to reach 10k iterations within 4 hours. This will vary but you can even finetune enough for a workable bot within 5k iterations using a CPU.

For a chatbot like this I recommend you try to reach at least 8500-10000 iterations. If you reach an unchanging or NaN difference in learning rate stop the model, it may have trained to much and you will encounter really weird bugs. For this you should save every 500-1000 iterations so you have snapshots to revert to.

My discord bot runs with `8560` iterations using the `355M` on a dataset with `1375352` tokens (about 500k individual chat messages from discord). The messages are trained from a single discord channel which included myself and 4 friends. This resulted in a very specific personality set the bot picked up where it would make jokes that only we would pick up and call out each other even when others spoke to it. This isn't desireable unless you want to just have it in one server.

To combat this you should grab a lot of conversations that you take part in with many different people. Then in your final dataset make sure you have a lot of back and forth conversation. General and off-topic chats are good for this.

#### Things to watch out for!

- Links. You probably want to parse these from your dataset or your bot will start to send randomly generated links that look real. Sometimes it can send a real link and this can be funny but it's a rare occasion.
- Bot messages and server messages. Messages from bots can sounds like messages from bots and you don't want your life like AI to sound like a bot do you? Parse these out along with discord's `Joined the Server.` messages.
- Language. If you want your bot to be nice, don't put toxic stuff in the dataset. AI doesn't have feelings and GPT-2 especially doesn't care about your views or how moral you are. If you are toxic in discord your bot is going to be toxic.

## Getting Started

**USE A VIRTUALENV!!!**

First clone `gpt-2-simple`'s source code locally.

```
git clone https://github.com/minimaxir/gpt-2-simple
cd gpt-2-simple
```

Setup a virtualenv inside of the repo

```
virtualenv .env
# Wait for it to setup
.env\Scripts\activate # On Windows
source .env\bin\activate # On Unix
pip install -r requirements.txt 
# IF USING A GPU TO FINETUNE/GENERATE
pip install -r requirements-gpu.txt
```


Download the models you need:

```
gpt-2-simple download MODELNAME
```

Models are: `124M`, `355M`, `774M`, `1.5B`

**You will not be able to run anything more than the `355M` model on a gaming graphics card. Don't bother wasting the time to download the higher memory models unless you have a Titan or Quadro or something. If you are using Colab the `774M` can work sometimes. **


### Creating a Dataset

You should use a discord chat exporter like [this](https://github.com/Tyrrrz/DiscordChatExporter/releases/tag/2.20) and export it to txt. The format for my dataset was as follows:

```
name1:
conversational message here
maybe another one here

name2:
conversational reply here

name1:
reply

name2:
reply reply

name3:
blah blah blah
```

Obviously it had real contextual conversation going on but this is the format it was in.

## Finetuning the model

If you are running the finetuning on a CPU I recommend using the smaller `124M` model. If you have a beefy GPU like an RTX card or a high level GTX/RX card you can probably try the `355M` model.

Below is code to finetune a model basically:

```python
import gpt_2_simple as gpt2
from datetime import datetime


file_name = "dataset.txt" # File name of dataset

sess = gpt2.start_tf_sess()

gpt2.finetune(
            sess,
            dataset=file_name,
            model_name='355M', # Model you have already downloaded
            steps=-1, # -1 will do unlimited. Enter number of iterations otherwise
            restore_from='latest', # Also allows 'fresh' which will overwrite old training
            run_name='discord', # The name to pull or create a checkpoint under
            print_every=50, # Print iterations every X numebr
            sample_every=150, # Generate a text sample ever X number of iter.
            save_every=500, # Save a snapshot every X number of iter.
            learning_rate=0.0001, # Lower to 0.00001 if you are not getting massive changes in results
            batch_size=1 # Keep at 1 or 2, will use up more memory if you raise this
)
```

You can run this everytime and it will train your model and pick up from where it left off, or start a new one if you have a new `run_name`. 

Finetune your model until it reaches around 8k-10k iterations.

## The Discord Bot Part

Create a discord bot on the discord site.

First you need to go to the [Applications Section](https://discord.com/developers/applications) of the developer panel. Inside you need to create a new app.

<p align="center">
  <img src="https://i.imgur.com/oiUA5hT.png">
</p>

Add a name and go to the new application's settings. You need to create a Bot User:

<p align="center">
  <img src="https://i.imgur.com/qx3BviW.png">
</p>

Now copy the token for the bot.

Below you will find the code to run a basic answer bot using the GPT-2 model you trained with the steps above:

```python
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
```

When you run this it will respond to you or anybody who pings it using the last 9 messages as context for the bot to continue the conversation!

