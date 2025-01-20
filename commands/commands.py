# commands/commands.py
import discord
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.server_config import ServerConfig
from schemas.waypoint import WaypointBase, WaypointCreate
import logging


class PrefixRequest(BaseModel):
    prefix: str


async def setprefix(
    interaction: discord.Interaction, request: PrefixRequest, session: Session
):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )
        return

    guild_id = str(interaction.guild.id)
    config = session.query(ServerConfig).filter_by(server_id=guild_id).first()
    if config:
        config.prefix = request.prefix
    else:
        config = ServerConfig(server_id=guild_id, prefix=request.prefix)
        session.add(config)
    session.commit()
    await interaction.response.send_message(
        f"Prefix set to {request.prefix}", ephemeral=True
    )


async def ping(interaction: discord.Interaction):
    logging.info(
        f"Ping command called by {interaction.user.name}#{interaction.user.discriminator}"
    )
    try:
        await interaction.response.send_message(
            f"Pong! {round(interaction.client.latency * 1000)}ms", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"Failed to get latency:\n```{e}```", ephemeral=True
        )
        logging.error(f"Failed to get latency: {e}")
