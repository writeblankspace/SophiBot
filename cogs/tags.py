from discord.ext.commands.cooldowns import BucketType
import os
import random
import discord
import typing
from replit import db
from discord.ext import commands
from func.cooldown import cooldown_cmd
from func.tagfinder import find_tag

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ @commands.command(
        name="tag",
        help="Checks a member's current rank.",
        brief="Checks a member's current rank.")
    async def rank(self, ctx, member: typing.Optional[discord.Member]):
        pass """
    
    @commands.group(
        name="tag",
        help="Retrieves the value of a tag.",
        invoke_without_command=True,
        aliases=["tags"]
    )
    async def tag(self, ctx, tag = None):
        if ctx.invoked_subcommand is None:
            #if tag != "set" and tag != "list":
            # tags = db["tags"] # the tag database
            found = find_tag(tag) # searches for the tag
            if found["value"] != None:
                await ctx.send(found["value"])
            else: # send a list of tags
                find_tag("tags")
                tags = db["tags"]
                keys = tags.keys()
                f_keys = []
                for key in keys:
                    f_keys.append(f"`{key}`")
                s_keys = ", ".join(f_keys)
                embed = discord.Embed(
                    title = 'List of tags', 
                    description = s_keys
                )
                await ctx.send(embed=embed)
            
    # to del a key 
    # del my_dict['key']

    @tag.command(
        name="delete",
        help="Deletes a tag",
        hidden=True,
        aliases=["del", "rem", "remove"]
    )
    async def delete(self, ctx, tag):
        found = find_tag(tag) 
        if found["status"] == 200:
            del db["tags"][tag] # delete the tag
            embed = discord.Embed(
                title = f'Tag `{tag}` deleted!', 
                description = (
                    f"```\n"
                    f"{found['value']}\n"
                    f"```\n"
                )
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Tag `{tag}` doesn't exist.")


    @tag.command(
        name="set",
        help="Sets the value of a tag."
    )
    async def set(self, ctx, name : str, *, value : str):
        tags = db["tags"] # the tag database
        found = find_tag(name) # searches for the tag
        
        """ Looks for a tag in the database and
        returns `key`, `value`, and `status`. \n 
        Also initiates the tag database if not available. \n
        200 success | 404 not found | 500 error """
        
        if found["status"] == 404:
            e_title = f"Tag `{name}` created!"
            e_desc = f"```\n{value}\n```"
            tags[name] = value
        
        elif found["status"] == 200:
            e_title = f"Tag `{name}` overwritten!"
            e_desc = (
                f"**Old value:**\n"
                f"```\n"
                f"{found['value']}\n"
                f"```\n"
                f"**New value:**\n"
                f"```\n"
                f"{value}\n"
                f"```"
            )
            tags[name] = value
            
        else:
            e_title = "error"
            e_desc = "error"
        
        embed = discord.Embed(
            title = e_title, 
            description = e_desc)
            
        await ctx.send(embed=embed)
        

    @tag.command(
        name="list",
        help="Retrieves a list of tags."
    )
    async def list(self, ctx):
        find_tag("tags")

        tags = db["tags"]
        keys = tags.keys()

        f_keys = []
        
        for key in keys:
            f_keys.append(f"`{key}`")

        s_keys = ", ".join(f_keys)
        
        embed = discord.Embed(
            title = 'List of tags', 
            description = s_keys
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Tags(bot))