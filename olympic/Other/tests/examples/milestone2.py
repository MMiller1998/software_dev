from trains.map import RailColor, TrainMap

r"""
Diagram for example #1

     BWI O
         |
 green,4 |
         |  red,3
     BWI O ------- O LAX
         |\
 green,5 | | blue,4
         |/
     BOS O

   blue,5
O -------- O
MRTL       IAD

O RSW
"""

train_map = TrainMap(500, 600)
bos = train_map.add_place('BOS', 322, 540)
lax = train_map.add_place('LAX', 16, 209)
bwi1 = train_map.add_place('BWI', 54, 45)
bwi2 = train_map.add_place('BWI', 69, 145)
mrtl = train_map.add_place('MRTL', 1, 1)
iad = train_map.add_place('IAD', 2, 2)
rsw = train_map.add_place('RSW', 3, 3)

c_bwi_bwi = train_map.add_connection(
    bwi1, bwi2, color=RailColor.GREEN, length=4)
c_bwi_lax = train_map.add_connection(
    bwi2, lax, color=RailColor.RED, length=3)
c_bwi_bos1 = train_map.add_connection(
    bwi2, bos, color=RailColor.GREEN, length=5)
c_bwi_bos2 = train_map.add_connection(
    bwi2, bos, color=RailColor.BLUE, length=4)
c_mrtl_iad = train_map.add_connection(
    mrtl, iad, color=RailColor.BLUE, length=5)

all_connections = [
    c_bwi_bwi,
    c_bwi_lax,
    c_bwi_bos1,
    c_bwi_bos2,
    c_mrtl_iad
]

dest_bwi1_lax = frozenset((bwi1, lax))
dest_mrtl_iad = frozenset((mrtl, iad))
dest_bwi1_bos = frozenset((bwi1, bos))
dest_bwi2_bos = frozenset((bwi2, bos))
dest_bwi1_bwi2 = frozenset((bwi1, bwi2))
dest_lax_bos = frozenset((lax, bos))
