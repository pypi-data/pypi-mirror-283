from enum import Enum


class RoomArchetype(Enum):
    """An enumeration representing different categories.

    :cvar LIVING_ROOM: "living_room"
    :vartype LIVING_ROOM: str
    :cvar KITCHEN: "kitchen"
    :vartype KITCHEN: str
    :cvar DINING: "dining"
    :vartype DINING: str
    :cvar BEDROOM: "bedroom"
    :vartype BEDROOM: str
    :cvar KIDS_BEDROOM: "kids_bedroom"
    :vartype KIDS_BEDROOM: str
    :cvar BATHROOM: "bathroom"
    :vartype BATHROOM: str
    :cvar NURSERY: "nursery"
    :vartype NURSERY: str
    :cvar RECREATION: "recreation"
    :vartype RECREATION: str
    :cvar OFFICE: "office"
    :vartype OFFICE: str
    :cvar GYM: "gym"
    :vartype GYM: str
    :cvar HALLWAY: "hallway"
    :vartype HALLWAY: str
    :cvar TOILET: "toilet"
    :vartype TOILET: str
    :cvar FRONT_DOOR: "front_door"
    :vartype FRONT_DOOR: str
    :cvar GARAGE: "garage"
    :vartype GARAGE: str
    :cvar TERRACE: "terrace"
    :vartype TERRACE: str
    :cvar GARDEN: "garden"
    :vartype GARDEN: str
    :cvar DRIVEWAY: "driveway"
    :vartype DRIVEWAY: str
    :cvar CARPORT: "carport"
    :vartype CARPORT: str
    :cvar HOME: "home"
    :vartype HOME: str
    :cvar DOWNSTAIRS: "downstairs"
    :vartype DOWNSTAIRS: str
    :cvar UPSTAIRS: "upstairs"
    :vartype UPSTAIRS: str
    :cvar TOP_FLOOR: "top_floor"
    :vartype TOP_FLOOR: str
    :cvar ATTIC: "attic"
    :vartype ATTIC: str
    :cvar GUEST_ROOM: "guest_room"
    :vartype GUEST_ROOM: str
    :cvar STAIRCASE: "staircase"
    :vartype STAIRCASE: str
    :cvar LOUNGE: "lounge"
    :vartype LOUNGE: str
    :cvar MAN_CAVE: "man_cave"
    :vartype MAN_CAVE: str
    :cvar COMPUTER: "computer"
    :vartype COMPUTER: str
    :cvar STUDIO: "studio"
    :vartype STUDIO: str
    :cvar MUSIC: "music"
    :vartype MUSIC: str
    :cvar TV: "tv"
    :vartype TV: str
    :cvar READING: "reading"
    :vartype READING: str
    :cvar CLOSET: "closet"
    :vartype CLOSET: str
    :cvar STORAGE: "storage"
    :vartype STORAGE: str
    :cvar LAUNDRY_ROOM: "laundry_room"
    :vartype LAUNDRY_ROOM: str
    :cvar BALCONY: "balcony"
    :vartype BALCONY: str
    :cvar PORCH: "porch"
    :vartype PORCH: str
    :cvar BARBECUE: "barbecue"
    :vartype BARBECUE: str
    :cvar POOL: "pool"
    :vartype POOL: str
    :cvar OTHER: "other"
    :vartype OTHER: str
    """

    LIVING_ROOM = "living_room"
    KITCHEN = "kitchen"
    DINING = "dining"
    BEDROOM = "bedroom"
    KIDS_BEDROOM = "kids_bedroom"
    BATHROOM = "bathroom"
    NURSERY = "nursery"
    RECREATION = "recreation"
    OFFICE = "office"
    GYM = "gym"
    HALLWAY = "hallway"
    TOILET = "toilet"
    FRONT_DOOR = "front_door"
    GARAGE = "garage"
    TERRACE = "terrace"
    GARDEN = "garden"
    DRIVEWAY = "driveway"
    CARPORT = "carport"
    HOME = "home"
    DOWNSTAIRS = "downstairs"
    UPSTAIRS = "upstairs"
    TOP_FLOOR = "top_floor"
    ATTIC = "attic"
    GUEST_ROOM = "guest_room"
    STAIRCASE = "staircase"
    LOUNGE = "lounge"
    MAN_CAVE = "man_cave"
    COMPUTER = "computer"
    STUDIO = "studio"
    MUSIC = "music"
    TV = "tv"
    READING = "reading"
    CLOSET = "closet"
    STORAGE = "storage"
    LAUNDRY_ROOM = "laundry_room"
    BALCONY = "balcony"
    PORCH = "porch"
    BARBECUE = "barbecue"
    POOL = "pool"
    OTHER = "other"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, RoomArchetype._member_map_.values()))
