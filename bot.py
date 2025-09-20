import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is now online!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, 
        name="!play"
    ))

@bot.command()
async def play(ctx, *, query):
    if not query:
        await ctx.send("❌ Please provide a song name! Example: `!play shape of you`")
        return
        
    if not ctx.author.voice:
        await ctx.send("❌ You must be in a voice channel first!")
        return
    
    try:
        voice_channel = ctx.author.voice.channel
        
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)
        
        await ctx.send(f"🎵 Playing: {query}")
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('⏹️ Stopped')
    else:
        await ctx.send('❎ Bot is not in a voice channel')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="🎵 Music Bot Help", color=0x00ff00)
    embed.add_field(
        name="Commands", 
        value="""
        `!play [song]` - Play a song
        `!stop` - Stop playback
        `!help` - Show help
        """, 
        inline=False
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)