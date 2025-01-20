import discord
import logging
import re
import sys
from discord.ext import commands
from sqlalchemy.orm import Session
from database.session import session
from models.server_config import Base, ServerConfig
from commands.commands import ping, setprefix, PrefixRequest
from utils.logging_setup import setup_logging
from schemas.waypoint import CoordinateCreate, WaypointCreate
from models.coordinate import Coordinate as CoordinateModel
from models.waypoint import Waypoint as WaypointModel

# Setup logging
setup_logging()

# Create tables
Base.metadata.create_all(bind=session.bind)

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)


def signal_handler(signum, frame):
    logging.info("Application received a signal to close.")
    sys.exit(0)


@bot.event
async def on_ready() -> None:
    """Perform startup tasks when the bot is ready."""
    logging.info(f"Logged in as {bot.user.name} - {bot.user.id}")
    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logging.error(f"Failed to perform startup tasks: {e}")


@bot.event
async def on_message(message) -> None:
    if message.author.bot and not message.webhook_id:
        return

    pattern = r"xaero-waypoint:([^:]+):([^:]+):([^:]+):([^:]+):([^:]+):([^:]+):([^:]+):([^:]+):([^:]+)"
    match = re.match(pattern, message.content)

    if match:
        waypoint = {
            "name": match.group(1),
            "type": match.group(2),
            "x": int(match.group(3)),
            "y": int(match.group(4)),
            "z": int(match.group(5)),
            "color": int(match.group(6)),
            "visibility": match.group(7) == "true",
            "yaw": int(match.group(8)),
            "dimension": match.group(9),
            "file": "default_file",  # Assuming file field
        }

        # Validate the coordinate data
        try:
            coordinate_data = CoordinateCreate(
                x=waypoint["x"], y=waypoint["y"], z=waypoint["z"]
            )
            waypoint_data = WaypointCreate(
                name=waypoint["name"],
                type=waypoint["type"],
                color=waypoint["color"],
                visibility=waypoint["visibility"],
                dimension=waypoint["dimension"],
                file=waypoint["file"],
                coordinate_id=None,  # This will be set after creating the coordinate
            )

            # Create a new database session
            db_session = session()

            try:
                # Create a new coordinate
                new_coordinate = CoordinateModel(
                    x=coordinate_data.x, y=coordinate_data.y, z=coordinate_data.z
                )
                db_session.add(new_coordinate)
                db_session.commit()
                db_session.refresh(new_coordinate)

                # Create a new waypoint
                new_waypoint = WaypointModel(
                    name=waypoint_data.name,
                    type=waypoint_data.type,
                    color=waypoint_data.color,
                    visibility=waypoint_data.visibility,
                    dimension=waypoint_data.dimension,
                    file=waypoint_data.file,
                    coordinate_id=new_coordinate.id,
                )
                db_session.add(new_waypoint)
                db_session.commit()

                # Send a confirmation message
                await message.channel.send(f"Waypoint '{waypoint['name']}' processed.")
            except Exception as e:
                db_session.rollback()
                await message.channel.send(f"Error processing waypoint: {str(e)}")
            finally:
                db_session.close()
        except Exception as e:
            await message.channel.send(f"Invalid waypoint data: {str(e)}")

    # Ensure other commands and events are still processed
    await bot.process_commands(message)


@bot.tree.command(
    name="setprefix", description="Set the command prefix for this server"
)
async def setprefix_command(interaction: discord.Interaction, prefix: str):
    request = PrefixRequest(prefix=prefix)
    await setprefix(interaction, request, session)


# Event when bot joins a new guild
@bot.event
async def on_guild_join(guild):
    db_session = session()
    try:
        config = ServerConfig(server_id=str(guild.id))
        db_session.add(config)
        db_session.commit()
        logging.info(f"Joined new guild: {guild.name}")
    except Exception as e:
        db_session.rollback()
        logging.error(f"Error adding guild to database: {str(e)}")
    finally:
        db_session.close()


# Run the bot
bot.run("YOUR_BOT_TOKEN")
