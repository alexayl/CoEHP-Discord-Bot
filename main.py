import discord
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime, timezone


TOKEN = "REPLACE_WITH_YOUR_DISCORD_BOT_TOKEN"
STUDENT_ROLE_NAME = 'Verified Student'
DOORBELL_CHANNEL_NAME = 'doorbell'  # or None to skip filtering by channel
DOORBELL_BOT_NAME = 'DoorbellBot'   # change if needed

notStudent = {"All Powerful Suzanne", "Server Developer:", "Intern", "Advisors", "Instructional team", "Peer TA", "Peer Mentor", "MEE6"}

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    for guild in client.guilds:
        student_role = discord.utils.get(guild.roles, name=STUDENT_ROLE_NAME)
        if not student_role:
            print(f'Role "{STUDENT_ROLE_NAME}" not found.')
            continue

        # Get students with ONLY the student role
        student_members = [
            m for m in guild.members 
            if set(m.roles).isdisjoint(notStudent)
        ]
        student_ids = {m.id for m in student_members}

        total_students = len(student_members)
        total_student_messages = 0
        engaged_student_ids = set()

        # Identify the doorbell channel (optional)
        doorbell_channel = discord.utils.get(guild.text_channels, name=DOORBELL_CHANNEL_NAME)

        weekly_engagement = defaultdict(set)  # { (year, week): set(user_ids) }

        for channel in guild.text_channels:
            if not channel.permissions_for(guild.me).read_message_history:
                continue

            try:
                async for message in channel.history(limit=None):
                    if message.author.id not in student_ids:
                        continue
                    if doorbell_channel and message.channel.id == doorbell_channel.id:
                        continue
                    if message.author.bot:
                        continue

                    total_student_messages += 1
                    engaged_student_ids.add(message.author.id)

                    # Get message week
                    msg_time = message.created_at.replace(tzinfo=timezone.utc)
                    year, week, _ = msg_time.isocalendar()
                    weekly_engagement[(year, week)].add(message.author.id)

            except discord.Forbidden:
                print(f"Skipping {channel.name} — missing permissions")


    print(f"total students: {total_students}")
    print(f"total student messages: {total_student_messages}")
    print(f"number of students who have engaged: {len(engaged_student_ids)}")
    print("\nWeekly Engagement:")

    # Prepare data for plotting
    weeks = []
    engagement_counts = []
    for (year, week), user_ids in sorted(weekly_engagement.items()):
        weeks.append(f"{week:02}-{str(year)[-2:]}")  # Week number and last two digits of year
        engagement_counts.append(len(user_ids))
        print(f"Week {year}-W{week:02}: {len(user_ids)} students engaged")

    # Plotting the engagement chart
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(weeks, engagement_counts, marker='o')
        plt.title('Weekly Student Engagement')
        plt.xlabel('Week Number')
        plt.ylabel('Number of Engaged Students')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('engagement_chart.png')
        print('Engagement chart saved as engagement_chart.png')
    except ImportError:
        print('matplotlib is not installed. Skipping chart generation.')

    await client.close()

client.run(TOKEN)