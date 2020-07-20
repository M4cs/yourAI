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
```


## Finetuning the model

If you are running the finetuning on a CPU I recommend using the smaller `124M` model. If you have a beefy GPU like an RTX card or a high level GTX/RX card you can probably try the `355M` model.
