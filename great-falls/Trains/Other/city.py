import re


class City:
    """
    Represents an immutable city in the Trains game map

    Args:
        name (str): the name of the city
        position (int, int): the position of the city on the map with positive coordinates

    Attributes:
        name (str): the name of the city
        position (int, int): the position of the city on the map with positive coordinates
    """
    name: str
    position: (int, int)

    def __init__(self, name: str, position: (int, int)):
        """
        Construct a City
        :param name: the name of the city
        :param position: the position of the city on the map
        :raises ValueError: if position coordinates are not positive
        """
        if position[0] < 0 or position[1] < 0:
            raise ValueError("A city's position must be positive coordinates")

        if not City.__valid_name(name):
            raise ValueError("A city's name must be less than 26 characters and can only contain letters, digits, "
                             "spaces, commas, and periods")

        self.name = name
        self.position = position

    @staticmethod
    def __valid_name(name: str) -> bool:
        return len(name) <= 25 and re.fullmatch("[A-Za-z0-9., ]+", name)

    # Override
    def __eq__(self, other):
        if isinstance(other, City):
            return self.name == other.name and self.position == other.position
        return False

    # Override
    def __hash__(self):
        return hash((self.name, self.position))

    # Override - required for comparisons when used in a heap
    def __lt__(self, other):
        return self.name < other.name