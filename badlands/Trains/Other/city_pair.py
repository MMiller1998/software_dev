from Trains.Other.city import City

class CityPair:
    """
    Represents a pair of two cities. city_1 is always lexicographically less than city_2

    Args:
        city_1 (City): one city in the city pair
        city_2 (City): the other city in the city pair

    Attributes:
        city_1 (City): the city in the city pair that is lexicographically less
        city_2 (City): the other city in the destination pair
    """
    city_1: City
    city_2: City

    def __init__(self, city_1: City, city_2: City):
        """
        Constructs an instances of CityPair's by making sure self.city_1 is the city with the name that is
        lexicographically less of the two cities
        :param city_1: one city in the city pair
        :param city_2: the other city in the city pair
        """
        if city_1 < city_2:
            self.city_1 = city_1
            self.city_2 = city_2
        else:
            self.city_1 = city_2
            self.city_2 = city_1

    # Override
    def __eq__(self, other):
        return self.city_1 == other.city_1 and self.city_2 == other.city_2

    # Override
    def __hash__(self):
        return hash((self.city_1.__hash__(), self.city_2.__hash__()))

    # Override
    def __lt__(self, other):
        if self.city_1.name == other.city_1.name:
            return self.city_2 < other.city_2
        else:
            return self.city_1 < other.city_1
