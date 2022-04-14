Pair: badlands

Commit: 6ff5c4cc2ae33187baf3f41a819661a698f8260f

Score: 120/145

Grader: Eshwari 🗺
  
30/30: accurate self eval

`strategy`

80/100

- 6/20 pts for proper organization (an interface for strategies, abstraction over strategy functionality, concrete implementations of hold-10 and buy-now)
  - 6/10 for the specific classes
  - 0/10 for the common buy algorithm factored out 
    - See notes below, also look how you basically repeat the BuyNow.get_turn in Hold10.get_turn...
  - I believe Matthias wanted to specifically have an explicit separation of an interface for strategies (having the choose-destinations and choose-actions methods) and an abstract class for abstraction over strategy functionality (e.g. common buy algorithm) because these technically serve different purposes. Whenever you have a data definition that something is 'one-of' something (e.g. you have different types of strategies) you need an interface and when you need to abstract commonalities you use an abstract class. These entities are easily present in Java and I know you're working in Python, but this is still just a general concept of OOD.
  - Giving some points because you do at least have 2 separate classes for BuyNow and Hold10. This is the design Matthias was looking for:
```
+-----------+                   +-----------+
| istrategy | <---------------- | astrategy |
+-----------+                   +-----------+
                                     ^
                                     |
                            +------------------+
                            |                  |
                +------------------+      +------------------+
                | hold-10-strategy |      | buy-now-strategy |
                +------------------+      +------------------+

- istrategy is the interface
- astrategy contains the common buy algorithm,
   plus small commonalities concerning the setup routine

- hold-10, one concrete implementation 
- buy-now, one concrete implementation 
```
- 0/10 BONUS points if the README or interface module/file contains a diagram for the organization
- 20/20 pts for signatures and purpose statements of
  - 10/10 pts: a choose-destinations method
  - 10/10 pts: a choose-action method                   
- 20/20 pts for >=1 unit tests of the choose-destination for hold-10
- 20/20 pts for unit tests of the choose-action for buy-now (>= 1 for checking "acquire a connection", >= 1 for checking "give me more cards")
- 14/20 pts for factoring out
  - 7/10 pts: lexical order of destinations: sig/purp/unit
  - 7/10 pts: lexical order of connections: sig/purp/unit
    - I don't think it is good practice for you to be overriding `__lt__`; you should have made separate specific methods for the comparisons with appropriate purpose statements.
      - You appear to have somewhat of a purpose statement for connection comparisons but it really should have incorporated Matthias's specifications for lexicographic orderings. And then you should have made a purpose statement like that for your destination comparisons.
      - Also, the connections one could have been written better. Something like (and it's fine because `or` is lazy):
        - `return (self.__city_pair < other.__city_pair) or (self.length < other.length) or (self.color.value < other.color.value)`
   

`player-protocol`
  
10/15
  
- 0/5 pts `setup` first
  - There is no `setup` method to pass in the map, cards, and rails, which is needed for the player API. Has been discussed in class and is part of [Logical Interactions](https://felleisen.org/matthias/4500-f21/local_protocol.html)
- 5/5 pts `pick` separate second, or explicitly included in `setup`
- 5/5 pts `take-turn` follows
