import csv
import discord
import math
import os
import random
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MESSAGE_ID = os.getenv("MESSAGE_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

description = """An bot to do things"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Message ID {MESSAGE_ID} (Channel ID: {CHANNEL_ID})")
    print("------")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    channel = bot.get_channel(int(CHANNEL_ID))
    print("Channel Info:")
    print(channel)
    print("------")
    # Fetch the message object using its ID
    message = await channel.fetch_message(int(MESSAGE_ID))
    print("Message Info:")
    print(message)
    print("------")
    # Fetch the reactions to the message
    reactions = message.reactions
    # Initialize a dictionary to store users and their reactions
    user_reactions = []

    # Loop through each reaction
    for reaction in reactions:
        async for user in reaction.users():
            if reaction.emoji in ["🛡️", "⚔️", "🩹"]:
                emoji_text = (
                    reaction.emoji.replace("🛡️", "tank")
                    .replace("⚔️", "dps")
                    .replace("🩹", "healer")
                )
                user_reactions.append([user.display_name, emoji_text])

    tanks = []
    healers = []
    dps = []
    names = []
    pug_spots = 0

    # shuffle users to ensure that the first is not picked everytime
    random.shuffle(user_reactions)

    # removing duplicates
    for row in user_reactions:
        if row[0] not in names:
            names.append(row[0])

    # Find how many players and groups and pugs we need
    player_count = len(names)
    group_count = math.ceil(player_count / 5)
    remainder = player_count % 5
    if remainder > 0:
        pug_spots = 5 - remainder

    print(f"Players: {player_count} Groups: {group_count} Pugs: {pug_spots}")

    # Add pugs to the list
    for i in range(1, pug_spots + 1):
        user_reactions.append([f"Pug {i}", "tank"])
        user_reactions.append([f"Pug {i}", "healer"])
        user_reactions.append([f"Pug {i}", "dps"])

    for row in user_reactions:
        if row[1] == "tank" and row[0] not in tanks:
            tanks.append(row[0])
        if row[1] == "healer" and row[0] not in healers:
            healers.append(row[0])
        if row[1] == "dps" and row[0] not in dps:
            dps.append(row[0])

    choosen_tanks = tanks[0:group_count]

    file = open("tanks.txt", "w")
    for i in choosen_tanks:
        file.write(i + "\n")
    file.close()

    trimmed_healers = [i for i in healers if i not in choosen_tanks]
    choosen_healers = trimmed_healers[0:group_count]
    file = open("healers.txt", "w")
    for i in choosen_healers:
        file.write(i + "\n")
    file.close()

    trimmed_dps = [
        i for i in dps if i not in choosen_tanks and i not in choosen_healers
    ]
    choosen_dps = trimmed_dps[0 : group_count * 3]

    file = open("dps.txt", "w")
    for dps in choosen_dps:
        file.write(dps + "\n")
    file.close()

    # field names
    fields = ["tank", "healer", "dps"]
    rows = []
    row_count = len(choosen_dps)
    choosen_tanks_csv = choosen_tanks[:]
    tank_rows_needed = row_count - len(choosen_tanks)
    for i in range(1, tank_rows_needed + 1):
        choosen_healers.append("")
        choosen_tanks_csv.append("")

    for x in range(1, group_count + 1):
        fields.append(f"group{x}")

    for i in range(0, row_count):
        row = [choosen_tanks_csv[i], choosen_healers[i], choosen_dps[i]]
        if i == 0:
            for tank in choosen_tanks:
                row.append(tank)
        else:
            for x in range(1, group_count + 1):
                row.append("")
        rows.append(row)

    with open(file="output.csv", newline="", mode="w") as f:

        write = csv.writer(f)

        write.writerow(fields)
        write.writerows(rows)

    await bot.close()


bot.run(TOKEN)
