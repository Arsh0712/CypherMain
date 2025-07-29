import discord
from discord.ext import commands, tasks
import aiohttp
import random
import requests

from core.Cypher import Cypher
from utils.tool import getAntiGuildLogs, getConfig, getanti, getantiguild
from datetime import datetime

class antiguild(commands.Cog):
    def __init__(self, client: Cypher):
        self.client = client      
        self.headers = {"Authorization": f"Bot MTE5MTM5OTk0MDAxNDk5NzU4NA.GKzqUA.IaRMKW0Esvg7kOsrrcx9i-vnm_9xYSKxVeGh8w"}
        self.processing = [
            
        ]

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

        
    @commands.Cog.listener()
    async def on_guild_update(self, before, after) -> None:
        try:
            anti = getanti(before.id)
            if anti != "on":
                return
            data = getConfig(before.id)
            anti = getanti(before.id)
            antiguild = getantiguild(before.id)
            punishment = data["punishment"]
            wled = data["whitelisted"]
            guild = after
            reason = "Cypher • Security | AntiGuildUpdate"


            async for entry in after.audit_logs(limit=1):
               user = entry.user.id
               user_id = entry.user.id
               api = random.randint(8,9)
            
            if entry.user.id == self.client.user.id:
               return
            
            if entry.user == after.owner or str(entry.user.id) in data.get("owners", []) or str(entry.user.id) in wled:
              return
           
            if anti == "off" or antiguild == "off":
               return
            
            else:
             if entry.action == discord.AuditLogAction.guild_update:
              async with aiohttp.ClientSession(headers=self.headers) as session:
               if punishment == "Ban":
                  async with session.put(f"https://discord.com/api/v{api}/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                      if before.icon and not before.icon == after.icon:
                        banneidn = requests.get(before.icon.url)
                        huehuehue = banneidn.content
                        await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, icon=huehuehue, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                      if after.icon and not before.icon:
                        await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, icon=None, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                      if not before.icon and not after.icon:
                        await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                      if before.icon == after.icon:
                        await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                        await self.getantichlogs(guild, user_id, punishment)
               elif punishment == "Kick":
                         async with session.delete(f"https://discord.com/api/v{api}/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r2:
                               if before.icon and not before.icon == after.icon:
                                bannei = requests.get(before.icon.url)
                                huehueh = bannei.content
                                await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, icon=huehueh, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                         if after.icon and not before.icon:
                           await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, icon=None, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                         if not before.icon and not after.icon:
                           await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                         if before.icon and before.icon == after.icon:
                           await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                           await self.getantichlogs(guild, user_id, punishment)
               elif punishment == "Strip":
                           mem = guild.get_member(entry.user.id)
                           await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
                           if before.icon and not before.icon == after.icon:
                              bann = requests.get(before.icon.url)
                              huehu = bann.content
                              await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, icon=huehu, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                           if after.icon and not before.icon:
                            await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, icon=None, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                           if not before.icon and not after.icon:
                             await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
                           if before.icon and before.icon == after.icon:
                            await after.edit(name=f"{before.name}", description=f"{before.description}", verification_level=before.verification_level, rules_channel=before.rules_channel, afk_channel=before.afk_channel, afk_timeout=before.afk_timeout, default_notifications=before.default_notifications, explicit_content_filter=before.explicit_content_filter, system_channel=before.system_channel, system_channel_flags=before.system_channel_flags, public_updates_channel=before.public_updates_channel, reason=reason, premium_progress_bar_enabled=before.premium_progress_bar_enabled)
               else:
                       return
        except Exception as e:
              pass
            

async def setup(bot):
    await bot.add_cog(antiguild(bot))