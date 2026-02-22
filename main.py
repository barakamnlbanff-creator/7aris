import os
import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("1457454411046715487")  # optional

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def is_mod():
    async def predicate(interaction: discord.Interaction):
        perms = interaction.user.guild_permissions
        return perms.kick_members or perms.ban_members or perms.moderate_members or perms.administrator
    return app_commands.check(predicate)

@bot.event
async def on_ready():
    try:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
        else:
            await bot.tree.sync()
        print(f"Logged in as {bot.user}")
    except Exception as e:
        print("Sync error:", e)

@bot.tree.command(name="kick", description="طرد عضو من السيرفر")
@is_mod()
@app_commands.describe(member="العضو", reason="السبب (اختياري)")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب"):
    await interaction.response.defer(ephemeral=True)
    try:
        await member.kick(reason=reason)
        await interaction.followup.send(f"تم طرد {member.mention}. السبب: {reason}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"ماقدرت أطرده: {e}", ephemeral=True)

@bot.tree.command(name="ban", description="حظر عضو من السيرفر")
@is_mod()
@app_commands.describe(member="العضو", reason="السبب (اختياري)", delete_message_days="حذف رسائل آخر X أيام (0-7)")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب", delete_message_days: int = 0):
    await interaction.response.defer(ephemeral=True)
    try:
        delete_message_days = max(0, min(7, delete_message_days))
        await member.ban(reason=reason, delete_message_seconds=delete_message_days * 24 * 3600)
        await interaction.followup.send(f"تم حظر {member.mention}. السبب: {reason}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"ماقدرت أحظره: {e}", ephemeral=True)

@bot.tree.command(name="mute", description="كتم عضو مؤقت (تايم آوت)")
@is_mod()
@app_commands.describe(member="العضو", minutes="مدة الكتم بالدقائق", reason="السبب (اختياري)")
async def mute(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "بدون سبب"):
    await interaction.response.defer(ephemeral=True)
    try:
        minutes = max(1, min(40320, minutes))  # حتى 28 يوم
        until = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)
        await interaction.followup.send(f"تم كتم {member.mention} لمدة {minutes} دقيقة. السبب: {reason}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"ماقدرت أكتمه: {e}", ephemeral=True)

@bot.tree.command(name="unmute", description="فك الكتم (إلغاء التايم آوت)")
@is_mod()
@app_commands.describe(member="العضو", reason="السبب (اختياري)")
async def unmute(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب"):
    await interaction.response.defer(ephemeral=True)
    try:
        await member.timeout(None, reason=reason)
        await interaction.followup.send(f"تم فك الكتم عن {member.mention}.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"ماقدرت أفك الكتم: {e}", ephemeral=True)

bot.run(MTQ3NTAwNzY4NTAzOTQ4OTE2OA.GaWjDw.EXL9Ql43M7th918GqiW2BFW2ED4j3I2r_x7RCA)
