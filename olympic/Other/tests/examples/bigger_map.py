from trains.map import RailColor, TrainMap

train_map = TrainMap(500, 600)
city1 = train_map.add_place('1', 322, 540)
city2 = train_map.add_place('2', 16, 209)
city3 = train_map.add_place('3', 54, 45)
city4 = train_map.add_place('4', 69, 145)
city9 = train_map.add_place('9', 53, 22)
city10 = train_map.add_place('10', 147, 417)

city5 = train_map.add_place('5', 499, 599)
city6 = train_map.add_place('6', 1, 1)
city7 = train_map.add_place('7', 12, 13)
city11 = train_map.add_place('11', 432, 234)

city8 = train_map.add_place('8', 11, 11)

conn_3_4 = train_map.add_connection(
    city3, city4, color=RailColor.GREEN, length=4)
conn_4_2 = train_map.add_connection(
    city4, city2, color=RailColor.RED, length=3)
conn_4_1_green = train_map.add_connection(
    city4, city1, color=RailColor.GREEN, length=5)
conn_4_1_blue = train_map.add_connection(
    city4, city1, color=RailColor.BLUE, length=4)
conn_2_3 = train_map.add_connection(
    city2, city3, color=RailColor.WHITE, length=3)
conn_1_2 = train_map.add_connection(
    city1, city2, color=RailColor.WHITE, length=4)
conn_1_9 = train_map.add_connection(city1, city9, color=RailColor.RED, length=5)
conn_1_10 = train_map.add_connection(city1, city10, color=RailColor.BLUE, length=3)

conn_5_6 = train_map.add_connection(city5, city6, color=RailColor.BLUE, length=5)
conn_6_7 = train_map.add_connection(city6, city7, color=RailColor.RED, length=3)
conn_5_7 = train_map.add_connection(city5, city7, color=RailColor.GREEN, length=4)
conn_5_11 = train_map.add_connection(city5, city11, color=RailColor.WHITE, length=4)

all_connections = [
    conn_3_4,
    conn_4_2,
    conn_4_1_green,
    conn_4_1_blue,
    conn_2_3,
    conn_1_2,
    conn_1_9,
    conn_1_10,
    conn_5_6,
    conn_6_7,
    conn_5_7,
    conn_5_11
]

dest_1_2 = frozenset((city1, city2))
dest_1_3 = frozenset((city1, city3))
dest_1_4 = frozenset((city1, city4))
dest_1_9 = frozenset((city1, city9))
dest_1_10 = frozenset((city1, city10))
dest_2_3 = frozenset((city2, city3))
dest_2_4 = frozenset((city2, city4))
dest_2_9 = frozenset((city2, city9))
dest_2_10 = frozenset((city2, city10))
dest_3_4 = frozenset((city3, city4))
dest_3_9 = frozenset((city3, city9))
dest_3_10 = frozenset((city3, city10))
dest_4_9 = frozenset((city4, city9))
dest_4_10 = frozenset((city4, city10))
dest_9_10 = frozenset((city9, city10))

dest_5_6 = frozenset((city5, city6))
dest_6_7 = frozenset((city6, city7))
dest_5_7 = frozenset((city5, city7))
dest_5_11 = frozenset((city5, city11))
dest_6_11 = frozenset((city6, city11))
dest_7_11 = frozenset((city7, city11))
