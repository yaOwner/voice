class Voice(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		try:
			if after.channel.id == 759846996721795112:
				if voice.count_documents({"owner": member.id}):
					
					name = voice.find_one({"owner": member.id})['name']
					limit = voice.find_one({"owner": member.id})['limit']

					category = discord.utils.get(member.guild.categories, id = 759847972979867659)
					channel = await member.guild.create_voice_channel(name, category = category)
					await channel.edit(user_limit = limit)
					await member.move_to(channel)

					voice.update_one({"owner": member.id}, {"$set": {"vID": channel.id}})
						
					def check(a,b,c):
						return len(channel.members) == 0
						
					await self.Bot.wait_for('voice_state_update', check=check)
					await channel.delete()
				
				else:
					
					category = discord.utils.get(member.guild.categories, id = 759847972979867659)
					channel = await member.guild.create_voice_channel(member.name, category = category)
					await member.move_to(channel)

					voice.insert_one(
						{
							"owner": member.id, 
							"name": member.name,
							"limit": 10,
							"vID": channel.id
						}
					)

						
					def check(a,b,c):
						return len(channel.members) == 0
						
					await self.Bot.wait_for('voice_state_update', check=check)
					await channel.delete()
		except:
			pass

	@commands.group(aliases = ['v'])
	async def voice(self, ctx):
		pass

	@voice.command()
	async def name(self, ctx, *, name = None):
		if not name:
			emb = discord.Embed(description = 'Напишите новое название голосового канала!', timestamp = datetime.datetime.utcnow())
			emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
			await ctx.send(embed = emb)

		else:
			if voice.count_documents({"owner": ctx.author.id}):
				vID = voice.find_one({"owner": ctx.author.id})['vID']
				channel = ctx.guild.get_channel(vID)
				if not channel:
					emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

				else:

					emb = discord.Embed(description = 'Вы успешно поменяли название канала!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

					await channel.edit(name = name)

					voice.update_one({"owner": ctx.author.id}, {"$set": {"name": name}})

			else:
				emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
				await ctx.send(embed = emb)


	@voice.command()
	async def lock(self, ctx, member: discord.Member = None):
		if not member:
			if voice.count_documents({"owner": ctx.author.id}):
				vID = voice.find_one({"owner": ctx.author.id})['vID']
				channel = ctx.guild.get_channel(vID)
				if not channel:
					emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

				else:

					role = discord.utils.get(ctx.guild.roles, name = '@everyone')
					await channel.set_permissions(role, connect = False)
					await channel.set_permissions(ctx.author, connect = True)

					emb = discord.Embed(description = 'Доступ к вашему каналу был закрыт!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

			else:
				emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
				await ctx.send(embed = emb)

		else:
			if voice.count_documents({"owner": ctx.author.id}):
				vID = voice.find_one({"owner": ctx.author.id})['vID']
				channel = ctx.guild.get_channel(vID)
				if not channel:
					emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

				else:

					await channel.set_permissions(member, connect = False)

					emb = discord.Embed(description = f'Доступ к вашему каналу был закрыт для {member.mention}!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

			else:
				emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
				await ctx.send(embed = emb)


	@voice.command()
	async def unlock(self, ctx, member: discord.Member = None):
		if not member:
			if voice.count_documents({"owner": ctx.author.id}):
				vID = voice.find_one({"owner": ctx.author.id})['vID']

				channel = ctx.guild.get_channel(vID)
				if not channel:
					emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

				else:
					role = discord.utils.get(ctx.guild.roles, name = '@everyone')
					await channel.set_permissions(role, connect = True)
					await channel.set_permissions(ctx.author, connect = True)

					emb = discord.Embed(description = 'Доступ к вашему каналу был открыт!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

			else:
				emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
				await ctx.send(embed = emb)

		else:
			if voice.count_documents({"owner": ctx.author.id}):
				vID = voice.find_one({"owner": ctx.author.id})['vID']

				channel = ctx.guild.get_channel(vID)
				if not channel:
					emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

				else:
					await channel.set_permissions(member, connect = True)

					emb = discord.Embed(description = f'Доступ к вашему каналу был открыт для {member.mention}!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

			else:
				emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
				await ctx.send(embed = emb)

	@voice.command()
	async def limit(self, ctx, limit: int = None):
		if not limit:
			emb = discord.Embed(description = 'Укажите лимит голового канала!', timestamp = datetime.datetime.utcnow())
			emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
			await ctx.send(embed = emb)

		elif limit > 99:
			emb = discord.Embed(description = 'Лимит слишком большой!', timestamp = datetime.datetime.utcnow())
			emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
			await ctx.send(embed = emb)

		else:
			
			if voice.count_documents({"owner": ctx.author.id}):

				vID = voice.find_one({"owner": ctx.author.id})['vID']
				channel = ctx.guild.get_channel(vID)

				if not channel:
					emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

				else:

					emb = discord.Embed(description = f'Вы успешно изменили лимит!', timestamp = datetime.datetime.utcnow())
					emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
					await ctx.send(embed = emb)

					await channel.edit(user_limit = limit)

					voice.update_one({"owner": member.id}, {"$set": {"limit": limit}})

			else:
				emb = discord.Embed(description = 'Зайдите в ваш голосовой канал!', timestamp = datetime.datetime.utcnow())
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))
				await ctx.send(embed = emb)


def setup(Bot):
	Bot.add_cog(Voice(Bot))
	print('[INFO] Voice загружен!')
