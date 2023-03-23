import discord
import requests
import json
import asyncio
import wikipedia
import random
import os
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return(quote)
def get_wiki(search):
	response = wikipedia.page(search, auto_suggest=False)
	return(response)
def	vowel_check(check):
	vowel = {'a','e','i','o','u','A','E','I','O','U'}
	if check in vowel:
		return(True)
	else:
		return(False)
@client.event
async def on_ready():
	print('Bot is logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	await message.add_reaction(u"\U0001F44D")
	if message.content.startswith('!inspire'):
		print("Providing inspiration")
		quote = get_quote()
		await message.channel.send(quote)
	if message.content.startswith('!enough'):
		print("Shutting down")
		await client.close()
		await asyncio.sleep(1)
		exit()
	if message.content.startswith('!search'):
		search = message.content[8:]
		print("Searching wikipedia for:", search)
		quote = get_wiki(search)
		if len(quote.content.split('\n')[0]) < 1800:
			fstr = quote.title + '\n' + quote.url + '\n' + quote.content.split('\n')[0]
		else:
			fstr = quote.title + '\n' + quote.url + '\n' + quote.content[:500] + '...'
		print(len(fstr))
		await message.channel.send(fstr)
	if message.content.startswith('!haddock'):
		global content
		temp = content[random.randint(0,345)]
		if vowel_check(temp[0]):
			haddock = message.author.display_name + ' is an ' + temp
		else:
			haddock = message.author.display_name + ' is a ' + temp
		await message.channel.send(haddock)
		print("Haddock insult sent")


file = open('haddock.txt')
content = file.readlines()
client.run(os.getenv('DISCORD_TOKEN'))