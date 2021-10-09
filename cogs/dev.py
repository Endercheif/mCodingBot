from typing import TYPE_CHECKING

import psutil
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Bot


class Dev(commands.Cog):
    """Admin & Test features"""

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(
        name="panel", aliases=("pan",), help="Some data about the panel"
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.is_owner()
    async def panel_stats(self, ctx):
        cols: tuple = ("blue", "green", "yellow", "orange", "red")
        mb: int = 1024 ** 2

        _embed = self.bot.embed(title="Bot Stats")

        vm = psutil.virtual_memory()
        percent: int = 100 * (vm.used / vm.total)
        _embed.add_field(
            name=f":{cols[int(percent // 20)]}_square: __RAM__",
            value="\n".join(
                (
                    f"> `{percent:.3f}` **%**",
                    f" - `{vm.total / mb:,.3f}` **Mb**",
                )
            ),
        )

        cpu_freq, cpu_percent = psutil.cpu_freq(), psutil.cpu_percent()
        _embed.add_field(
            name=f":{cols[int(cpu_percent // 20)]}_square: __CPU__",
            value=(
                f"> `{cpu_percent:.3f}`**%**\n"
                f"- `{cpu_freq.current / 1000:.1f}`/"
                f"`{cpu_freq.max / 1000:.1f}`"
                " **Ghz**"
            ),
        )

        disk = psutil.disk_usage(".")
        percent: int = 100 * (disk.used / disk.total)
        _embed.add_field(
            name=f":{cols[int(percent // 20)]}_square: __DISK__",
            value="\n".join(
                (
                    f"> `{percent:.3f}` **%**",
                    f"- `{disk.total / mb:,.3f}` **Mb**",
                )
            ),
        )

        await ctx.send(embed=_embed)

    @commands.command(name="reload_config", aliases=("reloadconf",))
    @commands.is_owner()
    async def reload_config(self, ctx: commands.Context):
        self.bot.config = self.bot.config.load()
        await ctx.send("Done.")

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cogs(self, ctx: commands.Context):
        c = 0

        for cog in self.bot.cogs:
            cog_namespaced = f'app.cogs.{cog.name}'

            try:
                self.bot.unload_extension(cog_namespaced)
                self.bot.load_extension(cog_namespaced)
            except Exception as e:
                await ctx.send(f"Error while reloading {cog.name}: {e}")
                c += 1

        await ctx.send(f"Reloaded whole bot, error: {c}")


def setup(bot: "Bot"):
    bot.add_cog(Dev(bot))
