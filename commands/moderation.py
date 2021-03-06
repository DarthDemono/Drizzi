import discord
from discord.ext import commands


def Checker(**permissions):
    original = commands.has_permissions(**permissions).predicate
    async def extended(ctx):
        if ctx.guild is None:
            return False
        return commands.is_owner() or await original(ctx)
    return commands.check(extended)

class moderation(commands.Cog):
    """
    Standard moderation commands
    """
    def __init__(self, client):
        self.client=client

    @commands.command(help='Mute any user')
    @commands.check(Checker(manage_roles=True))
    async def mute(self,msg,member,*reasons):

        reason = ' '.join(reasons)

        for user in msg.message.mentions:
            member = user

        if not msg.message.mentions:
            return await msg.channel.send('❓❓ Please Choose a User to mute')

        for role in msg.guild.roles:
            if role.name == 'muted':
                muteRole = role

            if role.name == 'Muted':
                muteRole = role

        try:
            await member.send(f"You've been Muted in {msg.guild} for: {reason}")
            await member.add_roles(muteRole)
            await msg.channel.send(f'**`✅ {member}` was successfully Muted >>** {reason}')
        except Exception as error:
            await msg.channel.send(f'❌ `{member}` Could not be muted: {error} ')

    @commands.command(help='unmute any user')
    @commands.check(Checker(manage_roles=True))
    async def unmute(self,msg):


        for user in msg.message.mentions:
            member = user

        if not msg.message.mentions:
            return await msg.channel.send('❓❓ Please Choose a User to unmute')

        for role in msg.guild.roles:
            if role.name == 'muted':
                muteRole = role

            if role.name == 'Muted':
                muteRole = role


        try:
            await member.remove_roles(muteRole)
            await msg.channel.send(f'✅ **`{member}` was successfully Unmuted**')
        except Exception as error:
            await msg.channel.send(f'❌ `{member}` Could not be unmuted: {error} ')

    @mute.error
    async def mute_handler(self,ctx,error):
       if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send('❌ **You dont have permissions to use this command!**')


    @unmute.error
    async def unmute_handler(self,ctx,error):

        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send('❌ **You dont have permissions to use this command!**')


    @commands.command(aliases=['clear'], help='deletes specified number of messages')
    @commands.check(Checker(manage_messages=True))
    async def purge(self,msg, ammount=5):

        if ammount == 0:
            return await msg.channel.send('❌ You cant clear 0 messages')
        try:
            await msg.channel.purge(limit=ammount)
            await msg.channel.send(f'✅ Succesfully purged `{ammount}` messages')
        except Exception as err:
            await msg.channel.send(err)

    @purge.error
    async def purge_handler(self,msg,error):

        if isinstance(error, commands.MissingPermissions):
             await msg.channel.send('❌ **You dont have permissions to use this command!**')

    @commands.command(aliases=['arole'], help='Adds any role to a user')
    @commands.check(Checker(manage_roles=True))
    async def addrole(self,msg,member,*,rolename):

        for user in msg.message.mentions:
            mem = user

        for role in msg.guild.roles:

            if role.name == rolename:
                try:
                    await mem.add_roles(role)
                    await msg.channel.send(f'`✅{role.name}` Was successfully given to `{user.name}`')
                except Exception as err:
                    await msg.channel.send(err)

    @commands.command(aliases=['remrole', 'rrole'],help='removes any role from a user')
    @commands.check(Checker(manage_roles=True))
    async def removerole(self,msg,member,*,rolename):

        for user in msg.message.mentions:
            mem = user

        for role in msg.guild.roles:

            if role.name == rolename:
                try:
                    await mem.remove_roles(role)
                    await msg.channel.send(f'`✅ {role.name}` Was successfully removed from `{user.name}`')
                except Exception as err:
                    await msg.channel.send(err)

    @addrole.error
    async def arole_handler(self,ctx,error):

        if isinstance(error, commands.MissingPermissions):
             await ctx.channel.send('❌ **You dont have permissions to use this command!**')

    @removerole.error
    async def rrole_handler(self,ctx,error):

        if isinstance(error, commands.MissingPermissions):
             await ctx.channel.send('❌ **You dont have permissions to use this command!**')

    @commands.command(help='kicks any user from the server')
    @commands.check(Checker(kick_members=True))
    async def kick(self, msg,member,*,reason):

        for user in msg.message.mentions:
            member = user

        try:
            await member.send(f"You've been kicked in {msg.guild} for: {reason}")
            await member.kick(reason=reason)
            await msg.channel.send(f'**`✅ {member}` was successfully kicked >>** {reason}')
        except Exception as err:
            await msg.channel.send(f'❌ {member} could not be kicked: {err}')

    @commands.command(help='Strike the BAN HAMMER')
    @commands.check(Checker(ban_members=True))
    async def ban(self,msg,member,*reasons):

        reason = ' '.join(reasons)

        for user in msg.message.mentions:
            member = user

        try:
            try:
                await member.send(f"You've been banned in {msg.guild} for: {reason}")
            except:
                pass

            await member.ban(reason=reason)
            await msg.channel.send(f'**`✅ {member}` was successfully banned >>** {reason}')
        except Exception as err:
            await msg.channel.send(f'❌ {member} could not be banned: {err}')

    @commands.command(help='Unbans any banned user ')
    @commands.check(Checker(ban_members=True))
    async def unban(self, msg,*,member):

        banned_users = await msg.guild.bans()

        member_name, member_disc = member.split('#')

        for bans in banned_users:
            user = bans.user

            if (user.name, user.discriminator) == (member_name , member_disc):
                await msg.guild.unban(user)
                await msg.channel.send(f'**`✅ {user.name}#{user.discriminator}` was successfully unbanned**')


    @ban.error
    async def ban_handler(self,ctx,error):

        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send('❌ **You dont have permissions to use this command!**')

    @unban.error
    async def unban_handler(self,ctx,error):

        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send('❌ **You dont have permissions to use this command!**')



def setup(client):
    client.add_cog(moderation(client))
