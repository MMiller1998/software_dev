from Trains.Common.map import Map

class IMapGenerator:
    """
    An interface for different strategies for creating a map.
    """
    
    def generate_map() -> Map:
        """
        :return: a generated map
        """
        raise NotImplementedError()