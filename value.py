import discord
from discord.ext import commands
import aiohttp
import asyncio

intents = discord.Intents.all()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_nfts(session, url, cursor=None):
    items = []
    url = url + f'&cursor={cursor}' if cursor else url
    data = await fetch(session, url)
    if data is not None: # Add this line
        items.extend(data.get('items', []))
        next_cursor = data.get('cursor')
        if next_cursor:
            items.extend(await fetch_all_nfts(session, url, next_cursor))
    return items

@bot.command()
async def value(ctx):
    discord_id = str(ctx.author.id)

    async with aiohttp.ClientSession() as session:
        mintgarden_data = await fetch(session, f'https://api.mintgarden.io/profile/by_discord/{discord_id}')

        mintgarden_ids = []
        total_value = 0
        nft_count = 0
        collection_counts = {}

        for mintgarden_id_data in mintgarden_data:
            mintgarden_id = mintgarden_id_data['id']
            mintgarden_ids.append(mintgarden_id)
            print(f"Mintgarden ID: {mintgarden_id}")

            nft_items = await fetch_all_nfts(session, f'https://api.mintgarden.io/profile/{mintgarden_id}/nfts?type=owned&size=100')
            nft_count += len(nft_items)

            for item in nft_items:
                collection_data = await fetch(session, f'https://api.mintgarden.io/collections/{item["collection_id"]}')
                item_value = collection_data.get("floor_price", 0)
                if item_value is None:
                    item_value = 0
                total_value += item_value

                collection_name = item['collection_name']
                if collection_name not in collection_counts:
                    collection_counts[collection_name] = {'count': 0, 'value': 0}
                collection_counts[collection_name]['count'] += 1
                collection_counts[collection_name]['value'] += item_value

        # Sorting collections by their total value
        sorted_collections = sorted(collection_counts.items(), key=lambda item: item[1]['value'], reverse=True)

        # First embed contains total value, number of Mintgarden IDs, and number of NFTs
        overview = "Total Value: {:.1f} XCH\nNumber of DIDs: {}\nNumber of NFTs: {}\nNumber of Collections: {}".format(total_value, len(mintgarden_ids), nft_count, len(sorted_collections))
        embed = discord.Embed(title="{}'s Portfolio Analysis".format(ctx.author.name), color=0x00ff00)
        embed.add_field(name="Overview", value=overview, inline=False)
        embed.set_footer(text="Disclaimer: The values provided are exclusively based on the floor prices from each collection.")
        await ctx.send(embed=embed)

        # Additional embeds for each collection
        for start in range(0, len(sorted_collections), 10):
            end = start + 10
            current_collections = sorted_collections[start:end]

            collection_info = ""  # Initialize the variable here

            for i, (collection, count_value) in enumerate(current_collections, start=start+1):
                collection_percentage = (count_value['value'] / total_value) * 100 if total_value != 0 else 0
                collection_info += "{}: {} NFTs, {:.1f} XCH, {:.1f}% of total\n".format(collection, count_value['count'], count_value['value'], collection_percentage)

            embed = discord.Embed(title="Collections {}-{}".format(start+1, min(end, len(sorted_collections))), color=0x00ff00)
            embed.add_field(name="NFTs by Collection", value=collection_info, inline=False)
            embed.set_footer(text="Disclaimer: The values provided are exclusively based on the floor prices from each collection.")
            await ctx.send(embed=embed)

bot.run('your-bot-token-here')
