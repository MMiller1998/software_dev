Pair: badlands

Commit: [`3eeb35`](https://github.ccs.neu.edu/CS4500-F21/badlands/tree/3eeb352f12d7860ac5f204adb178a044843feb85) *(Referenced URLs are not permalinks. Using `3eeb35` instead.)*

Score: 220/215

Grader: Alanna

Feedback: badlands
-------------------------------------------------
### Self Evaluation (30/30)
-------------------------------------------------
- (30/30) Accuracy
-------------------------------------------------
### Code Inspection (170/170)
-------------------------------------------------
#### In Player.pp : Total(50/50)
- five "public" methods and signtaures for:
    - (8/10) Setup - no purpose statement
    - (8/10) Pick - no purpose statement
    - (8/10) Play - no purpose statement
    - (10/10) More Cards
    - (10/10) Win
#### In referee.pp : Total(120/120)
- (10/10) a start-up phase (calling player's setup and pick)
- (10/10) a play-turns phase (involves calling play and more_cards)
- (10/10) a shut-down phase (call win and score function).
- Scoring segregated into separate methods, signature/purpose and unit tests for:
    - (20/20) segments of connections.
    - (20/20) longest path.
    - (20/20) destinations connected.
- (10/10) ranking function
- dealing with cheating/failing players:
    - (10/10) a single-point of control functionality for calling a player's functions/methods.
    - (10/10) a check that the desired action is legal.
-------------------------------------------------
### Design Inspection (20/15)
-------------------------------------------------
 - (5/5) purpose statement for the task.
 - (10/10) Manager informs player about the result of tournament at the very end of tournament.
 - BONUS(5/5) inform players the tournament has started.

