import discord
from discord.ext import commands
import aiohttp

from utils.tool import getConfig, getanti, getantiemoji


class AntiEmojiCreate(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.headers = {"Authorization": f"Bot MTE5MTM5OTk0MDAxNDk5NzU4NA.GKzqUA.IaRMKW0Esvg7kOsrrcx9i-vnm_9xYSKxVeGh8w"}
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def cog_unload(self):
        await self.session.close()

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji]) -> None:
        try:
            anti = getanti(guild.id)
            if anti != "on":
                return 
            
            if len(after) > len(before):
                created_emojis = [emoji for emoji in after if emoji not in before]
                data = getConfig(guild.id)
                anti = getanti(guild.id)
                antiemoji = getantiemoji(guild.id)
                punishment = data.get("punishment", "Strip")
                wled = data.get("whitelisted", [])
                reason = "Cypher • Security | AntiEmojiCreate"

                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_create):
                    user_id = entry.user.id
                    if user_id == self.client.user.id or user_id == guild.owner_id or str(user_id) in wled or str(user_id) in data.get("owners", []) or anti == "off" or antiemoji == "off":
                        return

                    async with self.session as session:
                        if punishment == "Ban":
                            async with session.put(f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user_id}", json={"reason": reason}) as r:
                                if r.status in (200, 201, 204):
                                    pass
                                else:
                                    pass
                                    pass

                        elif punishment == "Kick":
                            async with session.delete(f"https://discord.com/api/v10/guilds/{guild.id}/members/{user_id}", json={"reason": reason}) as r:
                                if r.status in (200, 201, 204):
                                    pass
                                else:
                                    pass
                                    pass

                        elif punishment == "Strip":
                            member = guild.get_member(user_id)
                            if member:
                                await member.edit(roles=[r for r in member.roles if not r.permissions.administrator], reason=reason)
                                pass
                            else:
                                pass

                        else:
                            pass

                    for emoji in created_emojis:
                        try:
                            await emoji.delete(reason=reason)
                            pass
                        except discord.Forbidden:
                            pass
                        except discord.HTTPException as e:
                            pass
                        except Exception as e:
                            pass

        except discord.DiscordException as e:
            pass
        except Exception as e:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(AntiEmojiCreate(bot))
