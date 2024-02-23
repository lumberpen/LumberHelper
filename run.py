import csv
import math
import random

with open("MOCK_DATA.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")

    tanks = []
    healers = []
    dps = []
    names = []
    user_reactions = []
    pug_spots = 0

    for row in spamreader:
        user_reactions.append(row)

    random.shuffle(user_reactions)

    for row in user_reactions:
        if row[0] not in names:
            names.append(row[0])

    player_count = len(names)
    group_count = math.ceil(player_count / 5)
    remainder = player_count % 5
    if remainder > 0:
        pug_spots = 5 - remainder
    print(f"Players: {player_count} Groups: {group_count} Pugs: {pug_spots}")
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
