import discord
from discord.ext import commands
from utils.tool import getAntiChannelLogs, getConfig, getanti, getantichannel
from datetime import datetime

class AntiChannelUpdate(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    async def handle_punishment(self, user_id: int, guild: discord.Guild, punishment: str, reason: str):
        try:
            if punishment == "Ban":
                await guild.ban(discord.Object(id=user_id), delete_message_days=1, reason=reason)
            elif punishment == "Kick":
                await guild.kick(discord.Object(id=user_id), reason=reason)
            elif punishment == "Strip":
                member = guild.get_member(user_id) or await guild.fetch_member(user_id)
                if member:
                    roles_to_remove = [role for role in member.roles if role != guild.default_role and role.position < guild.me.top_role.position]
                    if roles_to_remove:
                        await member.remove_roles(*roles_to_remove, reason="Unauthorized channel creation (AntiNuke)")
                    else:
                        pass
            else:
                pass
        except Exception as e:
            pass


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        try:
            guild = before.guild
            anti = getanti(guild.id)
            if anti != "on":
                return
            
            data = getConfig(before.guild.id)
            antichannel = getantichannel(before.guild.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            reason = "Cypher • Security | AntiChannelUpdate"

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update, after=datetime.utcnow() - datetime.timedelta(seconds=30)):
                user_id = entry.user.id
                
                if entry.user.id == self.client.user.id:
                    return
                
                if entry.user.id == guild.owner_id or str(entry.user.id) in wled or str(entry.user.id) in data.get("owners", []) or anti == "off" or antichannel == "off":
                    return

                await self.handle_punishment(user_id, guild, punishment, reason)
                await after.edit(name=before.name, topic=before.topic, nsfw=before.nsfw, category=before.category, slowmode_delay=before.slowmode_delay, type=before.type, overwrites=before.overwrites, reason=reason)
                break

        except discord.Forbidden:
            pass
        except Exception as e:
            print(e)


async def setup(client: commands.Bot):
    await client.add_cog(AntiChannelUpdate(client))
