from waypoint_mapper import (
    MapGenerator,
    Dimension,
    Colors,
    Flags,
    MinecraftVersion,
)

if __name__ == "__main__":
    generator = MapGenerator()
    seed = 132389425772377
    image = generator.generate_map_image(
        name="Example Waypoint",
        color=Colors.AQUA,
        x=-(39272),
        z=-(21656),
        dimension=Dimension.OVERWORLD,
        seed=seed,
        version=MinecraftVersion.MC_NEWEST,
        flags=Flags.DEFAULT,
        zoom=1,
    )
    image.save("output_image.png")
    print("Map image saved as output_image.png")
