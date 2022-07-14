import discord
from discord.ext import commands
import json
from time import sleep
import requests
from random import randint
import pyshorteners


with open("config.json") as f:
	data = json.load(f)

token = data.get("token")
prefix = data.get("prefix")


tizxr = commands.Bot(command_prefix=prefix, self_bot=True)

@tizxr.event
async def on_ready():
	print(f"Logged In As: {tizxr.user.name}")

@tizxr.command()
async def check(ctx, args):
	get_by_username = requests.get(f"https://api.roblox.com/users/get-by-username?username={args}").json()
	id = get_by_username['Id']
	get_by_id = requests.get(f"https://users.roblox.com/v1/users/{id}").json()
	description = get_by_id['description']
	itsbanned = get_by_id["isBanned"]
	display = get_by_id["displayName"]
	get_picture = f"https://www.roblox.com/avatar-thumbnail/image?userid={id}&width=420&height=420"
	embed = f"https://embed.rauf.workers.dev/?author=Username%253A%2520{args}&description=User%27s%2520Id%253A%2520{id}%250AUser%27s%2520Display%2520Name%253A%2520{display}%250AIf%2520User%2520Is%2520Banned%253A%2520{itsbanned}&image=https%253A%252F%252Fwww.roblox.com%252Favatar-thumbnail%252Fimage%253Fuserid%253D{id}%2526width%253D420%2526height%253D420"
	print(embed)
	await ctx.send(f"Profile Link: https://www.roblox.com/users/{id}/profile | Embed Url: {embed}")
	await ctx.send(f"```User Description: {description}```")


@tizxr.command()
async def login(ctx, cookie):
	cookies = {'.ROBLOSECURITY': str(cookie)}
	roblox = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies)
	if roblox.status_code==200:
		with open("robloxcookie.json") as database:
			textdata = json.load(database)
			data = textdata["data"]
			get_token = requests.post('https://auth.roblox.com/v2/logout', cookies=cookies)
			token = get_token.headers['x-csrf-token']
			update_data = {str(tizxr.user.name): token, str(tizxr.user.id): cookie}
			data.update(update_data)
			main_data = {"data": data}
			print(main_data)
			write = open("robloxcookie.json", "w")
			json.dump(main_data, write)
			write.close()
			await ctx.send("**Logged In!**")
	else:
		await ctx.send(":gem: | Sorry Cookie Was Wrong. Try again later.")



@tizxr.command()
async def spam(range, text):
	for msg in range(int(range)):
		await ctx.send(text)
		sleep(1)

@tizxr.command()
async def profile(ctx):
	with open("robloxcookie.json") as checkcookie:
		data = json.load(checkcookie)
		dataa = data["data"]
		if str(tizxr.user.id) in dataa:
			cook = dataa[str(tizxr.user.id)]
			cookie = {'.ROBLOSECURITY': str(cook)}
			roblox = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie)
			if roblox.status_code==200:
				userdata = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie).json() #get user data
				userid = userdata['id']
				credit = requests.get("https://billing.roblox.com/v1/credit", cookies=cookie).json()['balance']
				birthday = requests.get("https://accountinformation.roblox.com/v1/birthdate", cookies=cookie).json()
				transactions = requests.get(f"https://economy.roblox.com/v2/users/{userid}/transaction-totals?timeFrame=Month&transactionType=summary", cookies=cookie, data={'timeFrame':'Month', 'transactionType': 'summary'}).json()
				pending = transactions['pendingRobuxTotal']
				username = userdata['name']
				display = userdata['displayName']
				robuxdata = requests.get(f'https://economy.roblox.com/v1/users/{userid}/currency', cookies=cookie).json() 
				robux = robuxdata['robux'] #get robux balance #display name
				premiumbool = requests.get(f'https://premiumfeatures.roblox.com/v1/users/{userid}/validate-membership', cookies=cookie).json()
				rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100', cookies=cookie).json()
				while rap_dict['nextPageCursor'] != None:
					rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100',cookies=cookie).json()
				rap = sum(i['recentAveragePrice'] for i in rap_dict['data'])
				avatar = f"https://www.roblox.com/avatar-thumbnail/image?userid={userid}&width=420&height=420"
				birthday = requests.get("https://accountinformation.roblox.com/v1/birthdate", cookies=cookie).json()
				await ctx.send(f"""> **{username}'s Profile --> https://www.roblox.com/users/{userid}/profile** \n*Pending Robux:* {pending} \n*UserId:* {userid}\n*Display Name:* {display}\n*Premium:* {premiumbool}\n*Rap*: {rap} \n*Robux:* {robux} \n*Credit*: {credit} \n**Avatar Link:** {str(avatar)}""")
			else:
				await ctx.send("**Invalid Cookie or You Have Not Logged In. Please Use `!login` to log back in!")


@tizxr.command()
async def unlock_pin(ctx, args):
		with open("robloxcookie.json") as checkcookie:
			data = json.load(checkcookie)
			dataa = data["data"]
			if str(tizxr.user.id) in dataa:
				cook = dataa[str(tizxr.user.id)]
				cookie = {'.ROBLOSECURITY': str(cook)}
				roblox = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie)
				if roblox.status_code==200:
					get_token = requests.post('https://auth.roblox.com/v2/logout', cookies=cookie)
					token = None
					token = get_token.headers['x-csrf-token']
					await ctx.send("**:gem: | Unlocking Pin... Please Give It Some Time!**")
					if len(args)==4:
						header = {
						'x-csrf-token': token,
						'content-type': 'application/json'
						}
						unlock = requests.post("https://auth.roblox.com/v1/account/pin/unlock", headers=header, cookies=cookie, json={"pin": str(args)})
						if unlock.status_code==200:
							await ctx.send("**Pin Unlocked!**")
						elif unlock.status_code==429:
							await ctx.send("too many requests made.. slow down and try again LATER!!!")
						else:
							await ctx.send("WRONG PIN!")
					else:
						await ctx.send("**Pin Must Be 4 Letters..**")
				else:
					await ctx.send("**Invalid Cookie or You Have Not Logged In. Please Use `!login` to log back in!**")

@tizxr.command()
async def massunfrined(ctx):
		with open("robloxcookie.json") as checkcookie:
			data = json.load(checkcookie)
			dataa = data["data"]
			if str(tizxr.user.id) in dataa:
				cook = dataa[str(tizxr.user.id)]
				cookie = {'.ROBLOSECURITY': str(cook)}
				roblox = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie)
				if roblox.status_code==200:
					get_token = requests.post('https://auth.roblox.com/v2/logout', cookies=cookie)
					token = None
					token = get_token.headers['x-csrf-token']
					sleep(1)
					userdata = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie).json() #get user data
					userid = userdata['id']
					get_frined = requests.get(f'https://friends.roblox.com/v1/users/{userid}/friends').json()
					friends = get_frined["data"]
					list = {}
					header = {'x-csrf-token': token, 'content-type': 'application/json'}
					for ii in friends:
						list[ii["id"]] = ii
						try:
							unfrined = requests.post(f'https://friends.roblox.com/v1/users/{ii["id"]}/unfriend', cookies=cookie, headers=header)
							print(f"Unfrineded: {ii['name']}")
						except:
							await ctx.send("**Invalid Cookie or You Have Not Logged In. Please Use `!login` to log back in!")
				else:
					await ctx.send("**Invalid Cookie or You Have Not Logged In. Please Use `!login` to log back in!**")


@tizxr.command()
async def avatar(ctx, username):
	get_by_username = requests.get(f"https://api.roblox.com/users/get-by-username?username={username}").json()
	if "Id" in get_by_username:
		id = get_by_username['Id']
		try:
			i = requests.get(f"https://www.roblox.com/avatar-thumbnail/image?userid={id}&width=420&height=420")
			await ctx.send(f"**Avatar For: {username}. \n **{i.url}")
		except:
			await ctx.send("Invalid User!")
	else:
		await ctx.send("Invalid User")

@tizxr.command()
async def add_frined(ctx, args):
	with open("robloxcookie.json") as checkcookie:
			data = json.load(checkcookie)
			dataa = data["data"]
			if str(tizxr.user.id) in dataa:
				cook = dataa[str(tizxr.user.id)]
				cookie = {'.ROBLOSECURITY': str(cook)}
				roblox = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie)
				if roblox.status_code==200:
					get_token = requests.post('https://auth.roblox.com/v2/logout', cookies=cookie)
					token = None
					token = get_token.headers['x-csrf-token']
					get_by_username = requests.get(f"https://api.roblox.com/users/get-by-username?username={args}").json()
					name = get_by_username["Username"]
					if "Id" in get_by_username:
						id = get_by_username['Id']
						header = {'x-csrf-token': token, 'content-type': 'application/json'}
						i = requests.post(f"https://friends.roblox.com/v1/users/{id}/request-friendship", cookies=cookie, headers=header, json={"friendshipOriginSourceType": "Unknown"})
						if i.status_code==200:
							await ctx.send(f"**Sent Request To**`:` {name}")
						elif i.status_code==400:
							await ctx.send(f"Already Sent a Request to {name}")
						else:
							await ctx.send("Something Went Wrong")
					else:
						await ctx.send("Not a valid user!")
				else:
					await ctx.send("**Invalid Cookie or You Have Not Logged In. Please Use `!login` to log back in!**")


@tizxr.command()
async def unfrined(ctx, args):
	with open("robloxcookie.json") as checkcookie:
			data = json.load(checkcookie)
			dataa = data["data"]
			if str(tizxr.user.id) in dataa:
				cook = dataa[str(tizxr.user.id)]
				cookie = {'.ROBLOSECURITY': str(cook)}
				roblox = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie)
				if roblox.status_code==200:
					get_token = requests.post('https://auth.roblox.com/v2/logout', cookies=cookie)
					token = None
					token = get_token.headers['x-csrf-token']
					get_by_username = requests.get(f"https://api.roblox.com/users/get-by-username?username={args}").json()
					mydata = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookie).json() #get user data
					myid = mydata['id']
					id = get_by_username["Id"]
					header = {'x-csrf-token': token, 'content-type': 'application/json'}
					i = requests.get(f"https://friends.roblox.com/v1/users/{myid}/friends/statuses?userIds={id}", cookies=cookie, headers=header).json()
					date = i["data"]
					status = (date[0]["status"])
					if status=="Friends":
						e = requests.post(f"https://friends.roblox.com/v1/users/{id}/unfriend", headers=header, cookies=cookie)
						if e.status_code==200:
							await ctx.send(f":gem: | Unfrineded {args}!")
						elif e.status_code==403:
							await ctx.send("Token Validation Failed. Please Use `!login (cookie)` To log back in and fix this!")
						else:
							await ctx.send("Your Not Frineds With The Mentioned User!")
					else:
						await ctx.send("Your Not Frineds With The Mentioned User!")
				else:
					await ctx.send("**Invalid Cookie or You Have Not Logged In. Please Use `!login` to log back in!**")


@tizxr.command()
async def find(ctx, ix):
	check = requests.get(f"https://verify.eryn.io/api/user/{ix}")
	if check.status_code==200:
		username = requests.get(f"https://verify.eryn.io/api/user/{ix}").json()["robloxUsername"]
		idx = requests.get(f"https://verify.eryn.io/api/user/{ix}").json()["robloxId"]
		await ctx.send(f"**Username: {username}, Id: {idx}**")
	else:
		print("User Not Linked To ROVER Bot")


tizxr.run(token, bot=False)