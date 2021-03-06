import traceback
import discord
from discord.ext import tasks, commands
from datetime import datetime
from datetime import date
from func.lyrics.tv_lyrics import random_lyric
import calendar

timetable = [
	["07:00", "Tutor Period"],

	["07:20", "Period 1"],
	["08:00", "Period 2"],

	["08:40", "Period 3"],
	["09:20", "Period 4"],

	["09:50", "Break 1"],

	["10:25", "Period 5"],
	["11:05", "Period 6"],
	
	["11:35", "Break 2"],

	["12:30", "Period 7"],
	["13:00", "Period 8"],

	["13:30", "Dismissal"]
]

class crons(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.before_cron()
		self.cron.start()
	
	@tasks.loop(minutes=1)
	async def cron(self):
		# status
		snippet = random_lyric()

		game = discord.Game(f'"{snippet}"')
		
		await self.bot.change_presence(
			status=discord.Status.idle, 
			activity=game,
			afk=False
			)
		# reminders
		now = datetime.now()
		current_time = now.strftime("%H:%M")
		channel = self.bot.get_channel(768095329244413995)

		my_date = date.today() # gets day
		day = calendar.day_name[my_date.weekday()]  #'Wednesday'

		def double_digits(num):
			num = str(num)
			if len(num) < 2:
				num = "0" + num
			return num

		def start(name : str):		
			time = current_time
			split = time.split(":")
			
			hour = int(split[0])
			minute = int(split[1])
			ampm = "am"
			
			# hour += 3 # add 3 to the hour

			if hour > 12:
				hour -= 12
				ampm = "pm"
			
			# convert to double digits
			hour = double_digits(hour)
			minute = double_digits(minute)

			new_time = f"{hour}:{minute} {ampm}"

			embed = discord.Embed(
				title = f'{day} | {new_time}', 
				description = f'{name}')
			return embed
		
		def mytime(time : str):		
			time = current_time
			split = time.split(":")
			
			hour = int(split[0])
			minute = int(split[1])
			
			hour += 3 # add 3 to the hour
			
			# convert to double digits
			hour = double_digits(hour)
			minute = double_digits(minute)

			new_time = f"{hour}:{minute}"

			return new_time
		
		current_time = mytime(current_time)
		print(f"Current Time: {current_time}")


		weekdays =  ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

		if True and day in weekdays: # if it's a weekday
			for lesson in timetable:
				if current_time == lesson[0]:
					# if it's the correct time
					await channel.purge(limit=100)
					embed = start(lesson[1])
					await channel.send(embed=embed) 

		# UTC = time - 3h

	@cron.before_loop
	async def before_cron(self):
		await self.bot.wait_until_ready() 
	
	@cron.error
	async def cron_error(self, error):
		formatted = "".join(
			traceback.format_exception(type(error), error, error.__traceback__)
		)
		# await self.bot.get_channel(channel_id).send(formatted)
		print(formatted)

def setup(bot):
	bot.add_cog(crons(bot))