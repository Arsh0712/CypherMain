import discord
from discord.ext import commands
import aiohttp

from utils.tool import getConfig, getanti, getantiemoji


class AntiEmojiUpdate(commands.Cog):
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
            
            updated_emojis = [emoji for emoji in after if emoji in before]
            if not updated_emojis:
                return

            data = getConfig(guild.id)
            antiemoji = getantiemoji(guild.id)
            punishment = data.get("punishment", "Strip")
            wled = data.get("whitelisted", [])
            reason = "Cypher • Security | AntiEmojiUpdate"

            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_update):
                user_id = entry.user.id
                if user_id == self.client.user.id or user_id == guild.owner_id or str(user_id) in wled or str(user_id) in data.get("owners", []) or anti == "off" or antiemoji == "off":
                    return

                for emoji in updated_emojis:
                    previous_emoji = next((e for e in before if e.id == emoji.id), None)
                    if previous_emoji:
                        async with self.session as session:
                            if punishment == "Ban":
                                async with session.put(f"https://discord.com/api/v10/guilds/{guild.id}/bans/{user_id}", json={"reason": reason}) as r:
                                    if r.status not in (200, 201, 204):
                                        pass
                                        pass

                            elif punishment == "Kick":
                                async with session.delete(f"https://discord.com/api/v10/guilds/{guild.id}/members/{user_id}", json={"reason": reason}) as r:
                                    if r.status not in (200, 201, 204):
                                        pass
                                        pass

                            elif punishment == "Strip":
                                member = guild.get_member(user_id)
                                if member:
                                    await member.edit(roles=[r for r in member.roles if not r.permissions.administrator], reason=reason)
                                else:
                                    pass
                            else:
                                pass

                        try:
                            await emoji.edit(name=previous_emoji.name, image=previous_emoji.image, reason="Cypher • Security | Reverting emoji update")
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
    await bot.add_cog(AntiEmojiUpdate(bot))
