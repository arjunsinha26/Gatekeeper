import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import random
import string
import asyncio
from io import BytesIO
from datetime import timedelta

TOKEN = "Enter your token here"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

BACKGROUND = Image.open(
    "background.jpg"
).convert("RGBA").resize((900, 300))

duplicate_messages = {}
punishment_cooldown = {}
image_spam = {}

TIMEOUT_MINUTES = 30

SPAM_INTERVAL = 10
SPAM_THRESHOLD = 3
PUNISHMENT_COOLDOWN = 30

IMAGE_THRESHOLD = 3
IMAGE_INTERVAL = 10

def generate_captcha(length=6):

    chars = string.ascii_uppercase + string.digits

    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )

def create_captcha_image(text):

    width = 300
    height = 100

    image = Image.new(
        "RGB",
        (width, height),
        (255, 255, 255)
    )

    draw = ImageDraw.Draw(image)

    try:

        font = ImageFont.truetype(
            "arial.ttf",
            40
        )

    except:

        font = ImageFont.load_default()

    for _ in range(15):

        x1 = random.randint(0, width)
        y1 = random.randint(0, height)

        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line(
            (x1, y1, x2, y2),
            fill=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ),
            width=2
        )

    draw.text(
        (75, 30),
        text,
        font=font,
        fill=(0, 0, 0)
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer

async def create_welcome_image(member: discord.Member):

    background = BACKGROUND.copy()

    avatar_asset = member.display_avatar.with_size(128)

    avatar_bytes = await avatar_asset.read()

    avatar = Image.open(
        BytesIO(avatar_bytes)
    ).convert("RGBA")

    avatar = avatar.resize((120, 120))

    mask = Image.new(
        "L",
        avatar.size,
        0
    )

    draw_mask = ImageDraw.Draw(mask)

    draw_mask.ellipse(
        (0, 0, 120, 120),
        fill=255
    )

    avatar.putalpha(mask)

    avatar_x = (900 - 120) // 2
    avatar_y = 35

    background.paste(
        avatar,
        (avatar_x, avatar_y),
        avatar
    )

    draw = ImageDraw.Draw(background)

    try:

        welcome_font = ImageFont.truetype(
            "arial.ttf",
            38
        )

        username_font = ImageFont.truetype(
            "arial.ttf",
            26
        )

        member_font = ImageFont.truetype(
            "arial.ttf",
            22
        )

    except:

        welcome_font = ImageFont.load_default()
        username_font = ImageFont.load_default()
        member_font = ImageFont.load_default()

    welcome_text = "WELCOME"

    bbox = draw.textbbox(
        (0, 0),
        welcome_text,
        font=welcome_font
    )

    welcome_width = bbox[2] - bbox[0]

    draw.text(
        (
            (900 - welcome_width) // 2,
            170
        ),
        welcome_text,
        font=welcome_font,
        fill=(255, 255, 255)
    )

    username_text = member.name

    bbox = draw.textbbox(
        (0, 0),
        username_text,
        font=username_font
    )

    username_width = bbox[2] - bbox[0]

    draw.text(
        (
            (900 - username_width) // 2,
            215
        ),
        username_text,
        font=username_font,
        fill=(220, 220, 220)
    )

    member_text = f"Member #{member.guild.member_count}"

    bbox = draw.textbbox(
        (0, 0),
        member_text,
        font=member_font
    )

    member_width = bbox[2] - bbox[0]

    draw.text(
        (
            (900 - member_width) // 2,
            250
        ),
        member_text,
        font=member_font,
        fill=(200, 200, 200)
    )

    buffer = BytesIO()

    background.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer

@bot.event
async def on_ready():

    print(f"{bot.user} is online")

    try:

        synced = await bot.tree.sync()

        print(f"✅ Synced {len(synced)} slash command(s)")

    except Exception as e:

        print(f"[SYNC ERROR] {e}")

@bot.event
async def on_member_join(member: discord.Member):

    try:

        guild = member.guild
        bot_member = guild.get_member(bot.user.id)

        unverified_role = next(
            (
                r for r in guild.roles
                if r.name.lower() == "unverified"
            ),
            None
        )

        verified_role = next(
            (
                r for r in guild.roles
                if r.name.lower() == "verified"
            ),
            None
        )

        if unverified_role is None:

            unverified_role = await guild.create_role(
                name="UNVERIFIED"
            )

        if verified_role is None:

            verified_role = await guild.create_role(
                name="VERIFIED"
            )

        welcome_overwrites = {

            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            unverified_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            verified_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            bot_member: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True
            )
        }

        welcome_channel = discord.utils.get(
            guild.text_channels,
            name="welcome"
        )

        if welcome_channel is None:

            welcome_channel = await guild.create_text_channel(
                name="welcome",
                overwrites=welcome_overwrites
            )

        else:

            await welcome_channel.edit(
                overwrites=welcome_overwrites
            )

        verify_overwrites = {

            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            unverified_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            verified_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            bot_member: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True
            )
        }

        verify_channel = discord.utils.get(
            guild.text_channels,
            name="verify"
        )

        if verify_channel is None:

            verify_channel = await guild.create_text_channel(
                name="verify",
                overwrites=verify_overwrites
            )

        else:

            await verify_channel.edit(
                overwrites=verify_overwrites
            )

        for channel in guild.channels:

            if channel.name in ["welcome", "verify"]:
                continue

            try:

                await channel.set_permissions(
                    unverified_role,
                    view_channel=False
                )

            except:
                pass

        await member.add_roles(unverified_role)

        welcome_image = await create_welcome_image(member)

        await welcome_channel.send(
            file=discord.File(
                fp=welcome_image,
                filename="welcome.png"
            )
        )

        await verify_channel.send(
            f"🔐 {member.mention} please use `/verify` in this channel."
        )

    except Exception as e:

        print(f"[JOIN ERROR] {e}")

@bot.tree.command(
    name="verify",
    description="Verify yourself"
)
async def verify(interaction: discord.Interaction):

    try:

        guild = interaction.guild
        user = interaction.user

        if interaction.channel.name != "verify":

            return await interaction.response.send_message(
                "❌ You can only use this command in #verify",
                ephemeral=True
            )

        verified_role = next(
            (
                r for r in guild.roles
                if r.name.lower() == "verified"
            ),
            None
        )

        unverified_role = next(
            (
                r for r in guild.roles
                if r.name.lower() == "unverified"
            ),
            None
        )

        if verified_role in user.roles:

            return await interaction.response.send_message(
                "✅ You are already verified.",
                ephemeral=True
            )

        captcha = generate_captcha()

        captcha_buffer = create_captcha_image(captcha)

        await interaction.response.send_message(
            "📸 Type the captcha shown below.",
            file=discord.File(
                fp=captcha_buffer,
                filename="captcha.png"
            ),
            ephemeral=True
        )

        def check(message):

            return (
                message.author == user
                and message.channel == interaction.channel
            )

        try:

            msg = await bot.wait_for(
                "message",
                timeout=60,
                check=check
            )

            if msg.content.strip().upper() == captcha:

                await user.add_roles(verified_role)

                if unverified_role in user.roles:

                    await user.remove_roles(unverified_role)

                await interaction.followup.send(
                    "✅ Verification successful!",
                    ephemeral=True
                )

            else:

                await interaction.followup.send(
                    "❌ Incorrect captcha.",
                    ephemeral=True
                )

        except asyncio.TimeoutError:

            await interaction.followup.send(
                "⌛ Verification timed out.",
                ephemeral=True
            )

    except Exception as e:

        print(f"[VERIFY ERROR] {e}")

        if not interaction.response.is_done():

            await interaction.response.send_message(
                "❌ An unexpected error occurred.",
                ephemeral=True
            )

@bot.event
async def on_message(message: discord.Message):

    if message.author.bot:
        return

    if not message.guild:
        return

    guild_id = message.guild.id
    user_id = message.author.id

    current_time = asyncio.get_event_loop().time()

    # IMAGE SPAM

    if len(message.attachments) > 0:

        if guild_id not in image_spam:

            image_spam[guild_id] = {}

        if user_id not in image_spam[guild_id]:

            image_spam[guild_id][user_id] = []

        image_spam[guild_id][user_id].append({

            "time": current_time,
            "message": message
        })

        image_spam[guild_id][user_id] = [

            msg_data
            for msg_data in image_spam[guild_id][user_id]
            if current_time - msg_data["time"] <= IMAGE_INTERVAL
        ]

        if len(image_spam[guild_id][user_id]) >= IMAGE_THRESHOLD:

            try:

                messages_to_delete = [

                    msg_data["message"]
                    for msg_data in image_spam[guild_id][user_id]
                ]

                try:

                    await message.channel.delete_messages(
                        messages_to_delete
                    )

                except:

                    for msg in messages_to_delete:

                        try:
                            await msg.delete()
                        except:
                            pass

                duration = timedelta(
                    minutes=TIMEOUT_MINUTES
                )

                await message.author.timeout(
                    duration,
                    reason="Image spam detected"
                )

                await message.channel.send(
                    f"🖼️🚫 {message.author.mention} timed out for image spam.",
                    delete_after=5
                )

                image_spam[guild_id][user_id] = []

            except Exception as e:

                print(f"[IMAGE SPAM ERROR] {e}")

            return

    # TEXT SPAM

    if guild_id not in duplicate_messages:

        duplicate_messages[guild_id] = {}

    if user_id not in duplicate_messages[guild_id]:

        duplicate_messages[guild_id][user_id] = []

    if guild_id not in punishment_cooldown:

        punishment_cooldown[guild_id] = {}

    duplicate_messages[guild_id][user_id].append({

        "content": message.content.lower(),
        "time": current_time,
        "message": message
    })

    duplicate_messages[guild_id][user_id] = [

        msg_data
        for msg_data in duplicate_messages[guild_id][user_id]
        if current_time - msg_data["time"] <= SPAM_INTERVAL
    ]

    same_messages = [

        msg_data
        for msg_data in duplicate_messages[guild_id][user_id]
        if msg_data["content"] == message.content.lower()
    ]

    if len(same_messages) >= SPAM_THRESHOLD:

        last_punishment = punishment_cooldown[guild_id].get(
            user_id,
            0
        )

        if current_time - last_punishment < PUNISHMENT_COOLDOWN:

            return

        punishment_cooldown[guild_id][user_id] = current_time

        try:

            messages_to_delete = [

                msg_data["message"]
                for msg_data in same_messages
            ]

            try:

                await message.channel.delete_messages(
                    messages_to_delete
                )

            except:

                for msg in messages_to_delete:

                    try:
                        await msg.delete()
                    except:
                        pass

            duration = timedelta(
                minutes=TIMEOUT_MINUTES
            )

            await message.author.timeout(
                duration,
                reason="Repeated spam detected"
            )

            await message.channel.send(
                f"🚫 {message.author.mention} timed out for spam.",
                delete_after=5
            )

            duplicate_messages[guild_id][user_id] = []

        except Exception as e:

            print(f"[SPAM ERROR] {e}")

        return

    await bot.process_commands(message)
@bot.tree.command(
    name="flush",
    description="Delete messages in the channel"
)

@app_commands.describe(
    amount="Number of messages to delete"
)
async def flush(
    interaction: discord.Interaction,
    amount: int
):

    # Admin only
    if not interaction.user.guild_permissions.manage_messages:

        return await interaction.response.send_message(
            "❌ You do not have permission.",
            ephemeral=True
        )

    # Limit protection
    if amount < 1 or amount > 100:

        return await interaction.response.send_message(
            "❌ Amount must be between 1 and 100.",
            ephemeral=True
        )

    try:

        await interaction.response.defer(
            ephemeral=True
        )

        deleted = await interaction.channel.purge(
            limit=amount
        )

        await interaction.followup.send(
            f"🗑️ Deleted {len(deleted)} messages.",
            ephemeral=True
        )

    except Exception as e:

        print(f"[CLEAR ERROR] {e}")

        await interaction.followup.send(
            "❌ Failed to delete messages.",
            ephemeral=True
        )

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    print(f"[APP COMMAND ERROR] {error}")

bot.run(TOKEN)
