# Quoridor Game
`QuoridorGame` is a backend program which provides users with the ability to play a 2-player Quoridor Game from start to finish. The game can be played with just two methods: `move_pawn` and `place_fence`.

 ***It is that simple!***

## Playing the Game

* Each player is given a single pawn and 10 fences.
* Opponents face each other off on opposite ends of the board. 
* In any given turn, a player can either choose to move their pawn or place a fence into the game. 
    * A turn lasts until the player has made a _valid move_.
* Fences are intended to block players from quickly reaching the other side of the game. Once a player runs out of fences, a players only option is to move their pawn. 
* Players can move their pawns one space (Vertically or Horizontally)
    * edge cases exist that can allow a player to jump over another player.
    * for more details on edge cases review [Detailed Game Instructions](https://en.gigamic.com/files/media/fiche_pedagogique/educative-sheet_quoridor-english.pdf)

**The first player whose pawn reaches any of the cells of the opposite player's base line wins the game.**

## The Board and Game Items



The following image represents our board and the possible coordinates where each players pawn may move to:

![image](https://user-images.githubusercontent.com/21003726/127106790-aaf4e265-a122-4fc3-bc70-77a261c78ea2.png)
 
***Pawns***

The pawn position `(x,y)` is defined by the coordinate of the top left corner of the cell that the pawn is on. `x` is the number from the vertical line and `y` is the number from the horizontal line, making the top left corner of the cell. The board positions start with `(0,0)` and end at `(8,8)`. At the beginning of the game, player 1 places pawn 1 (P1) on the top center of the board and player 2 places pawn 2 (P2) on the bottom center of the board.  The position of P1 and P2 is `(4,0)` and `(4,8)` when the game begins.   

***Fences***

When each player tries to place a fence on the board, the position of the fence is defined by a letter and coordinates.  For vertical fences, we use `v` and for horizontal fences, we use `h`.  As an example, for the blue fence (vertical) in the picture, we use the coordinate of the top corner to define it and for the red fence (horizontal), we use coordinate of the left corner to define it. 

## Implementation
To play we use the following methods:

Method Name   | Parameters     |   Return Values  |
------------- | -------------  | ---------------- |
`move_pawn`   | method takes following two parameters in order: an integer that represents which player (1 or 2) is making the move and a tuple with the coordinates of where the pawn is going to be moved to. | If the move is forbidden by the rule or blocked by the fence, return `False`. If the move was successful or if the move makes the player win, return `True`. If the game has been already won, return `False`.
`place_fence` |  method takes following 3 parameters in order: an integer that represents which player (1 or 2) is making the move, a string 'v' (vertical) or 'h' (horizontal), and a tuple with the coordinates of where the pawn is going to be moved to. | If player has no fence left, or if the fence is out of the boundaries of the board, or if there is already a fence there and the new fence will overlap or intersect with the existing fence, return `False`. If the fence can be placed, return `True`. If the game has been already won, return `False`
`is_winner`   | method that takes a single integer representing the player number (1 or 2) as a parameter and returns `True` if that player has won and `False` if that player has not won. | returns `True` if that player has won and `False` if that player has not won.
`visualize_board` | method takes no parameters. Method prints a physical representation of the board with the current location of each pawn on the board. | returns `None`

## How the Game is played

Here's a very simple example of how the QuoridorGame class will be used for gameplay.

```python
q = QuoridorGame()

q.move_pawn(2, (4,7)) #moves the Player2 pawn -- invalid move because only Player1 can start, returns False
q.move_pawn(1, (4,1)) #moves the Player1 pawn -- valid move, returns True
q.place_fence(1, 'h',(6,5)) #places Player1's fence -- out of turn move, returns False 
q.move_pawn(2, (4,7)) #moves the Player2 pawn -- valid move, returns True
q.visualize_board() # shows a game board with the pawns current position on the board.
q.place_fence(1, 'h',(6,5)) #places Player1's fence -- returns True
q.place_fence(2, 'v',(3,3)) #places Player2's fence -- returns True
q.is_winner(1) #returns False because Player 1 has not won
q.is_winner(2) #returns False because Player 2 has not won
```
## Program Features
* Detects edge cases, where players may be face-to-face. This would allow a player to jump over their opponent. When a player is face-to-face but a fence is placed in back of an opponent (blocking a player to jump over), this allows a player to move diagonally. 
* Detects when any given player is out of turn
* Detects if a position is unreachable for any given player, based on their current position in the board.
* Detects if a fence has already been placed on the board in any given position and direction. 
## Future Implementations
* *Fairplay Rule*. Fairplay rule is where Fences cannot be placed in a way that they would completely cut off access to an opponents back line (fences cannot completely cutoff opponents from reaching the other side.)
* GUI