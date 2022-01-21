# Bryson Rivera
# Quoridor Game, where 2 players race to reach the opposite end of the board
# the first player to make it to the end wins. Game involves moving past fences that are
# placed horizontally and vertically to get to the other side.
class QuoridorGame:
    """This class represents the Quoridor Game. The __init__ method
        uses composition to turn each class in the .py file into a data member.
        The class also holds two additional data members, which will be used to
        determine which players turn it is (1 or 2) and a values that will be critical
        to initiating the starting values of the players on the board.
        This class is responsible for orchestrating the Quoridor game.
        Each players move will come from this class, as well as some other important methods
        that will be used to determine if a move is plausible given the restrictions of the game"""

    def __init__(self):
        """Creates a QuoridorGame object with the Board, player, player1, players, switch_player, initiate_board
            and is_winner data members. """
        self._board = Board()
        self._player = Player()
        self._player1 = Player1()
        self._player2 = Player2()
        self._switch_player = 1
        self._game_not_won = True
        self.starting_board()

    def get_player1_coordinates(self):
        """returns the coordinates for player 1"""
        return self._player1.get_player1_coordinates()

    def get_player2_coordinates(self):
        """returns the coordinates for player 2"""
        return self._player2.get_player2_coordinates()

    def get_player_coordinates(self, pawn):
        """given the number representing the player, method returns the current coordinates for that player."""
        if pawn == 1:
            return self._player1.get_player1_coordinates()
        else:
            return self._player2.get_player2_coordinates()

    def update_players_position(self, new_coordinates, player):
        """Given the new coordinates and the number representing the
        player this method makes sure that for each player there is only one pawn on the board.
        Method also updates players current position and updates the the pawn move in the board.
        This method should only be called, when we have verified that the move is valid."""
        matrix_position = self._player.position_adjustment(new_coordinates)
        if player == 1:
            self._player1.increment_num_of_p1_pawns(1)
            if self._player1.get_player1_coordinates() is not None:
                prev = self._player1.get_player1_coordinates()
                if self._player1.get_num_of_p1_pawns_on_board() > 1:
                    self._player1.increment_num_of_p1_pawns(-1)
                    self._board.remove_old_player_position(prev)
            self._board.set_player_in_board(matrix_position, player)
            self._player1.set_player1_coordinates(new_coordinates)
            self._switch_player += 1
        else:
            self._player2.increment_num_of_p2_pawns(1)
            if self._player2.get_player2_coordinates() is not None:
                prev = self._player2.get_player2_coordinates()
                if self._player2.get_num_of_p2_pawns_on_board() > 1:
                    self._player2.increment_num_of_p2_pawns(-1)
                    self._board.remove_old_player_position(prev)
            self._board.set_player_in_board(matrix_position, player)
            self._player2.set_player2_coordinates(new_coordinates)
            self._switch_player -= 1
        return

    def visualize_board(self):
        """method returns the board we are currently working with, showing the position of the values in the list."""
        best_visualization = ""
        for i in self._board.get_board():
            best_visualization += str(i) + "\n"
        print(best_visualization)
        return True

    def get_player_positions(self):
        """method that helps us see the current coordinates for each player."""
        print(f"Player 1 position: {self._player1.get_player1_coordinates()}")
        print(f"Player 2 position: {self._player2.get_player2_coordinates()}")

    def starting_board(self) -> object:
        """Method is only called once at the beginning of the game, to initiate the board."""
        # initialize which fence positions are forbidden (edges of the board)
        self._player.set_forbidden_fence_coordinates("v")
        self._player.set_forbidden_fence_coordinates("h")

        # initialize player 1

        self._board.player1_valid_moves(
            (4, 0), self._player.get_dictionary_fences())
        # self._player1.set_player1_coordinates((4, 0))
        self.update_players_position((4, 0), 1)
        self._player1.set_winning_coordinates_list()

        # initialize player 2
        self._board.player2_valid_moves(
            (4, 8), self._player.get_dictionary_fences())
        # self._player2.set_player2_coordinates((4, 8))
        self.update_players_position((4, 8), 2)
        self._player2.set_player2_winning_coordinates()

        return True

    def move_pawn(self, player, new_coord):
        """given the number representing the player and the new coordinate value,
        this method is the center method that will be used to move a player to a new position.
        This method calls the initial_checks method. If initial_checks return True, method will then call
        the Board classes update_valid_moves method and edge_case_player method. If new_coordinates
        is in the list generated from the board classes methods, then the method should call the
        update_players_position method. Finally, the method will return True. If any of the tests fail, method returns
        False """
        if self._game_not_won:

            # get dictionary of fences currently on board
            fences = self._player.get_dictionary_fences()

            # verify player turn and check that space we want to move into is empty
            if self._switch_player is player and self._board.check_space_and_coord_pawn(new_coord) == 0:
                if player == 1:
                    moves = self._board.player1_valid_moves(
                        self.get_player_coordinates(player), fences)
                else:
                    moves = self._board.player2_valid_moves(
                        self.get_player_coordinates(player), fences)

                new_list = self._board.edge_case(
                    moves, self.get_player_coordinates(player), new_coord, fences)

                if new_coord in new_list:
                    self.update_players_position(new_coord, player)
                    if self._player1.get_player1_coordinates() in self._player1.get_player1_winning_coordinates():
                        self._game_not_won = False
                    if self._player2.get_player2_coordinates() in self._player2.get_player2_winning_coordinates():
                        self._game_not_won = False
                    return True

        return False

    def place_fence(self, player, v_or_h_fence, new_fence_coordinate):
        """Given the numbers representing the player, letter representing whether, the fence is vertical or horizontal
        and the new coordinate, this method will add a coordinate into a dictionary that will be
        used by one of the Board methods to determine if a move is valid or not. In order to determine if the placement
        of the fence is valid or not, we call the Player classes check_space_and_coord_fence method.
        If the value returns True, meaning the new coordinate for the fence is in range of the board and no other
        fence with the same coordinate exists, the move is valid and should be recorded into the
        fence_dictionary data member."""
        if self._game_not_won:

            checks_systems = self._player.check_space_and_coord_fence(
                v_or_h_fence, new_fence_coordinate)
            if checks_systems and self._switch_player is player:

                if player == 1:
                    if self._player1.get_num_of_player1_fences() > 0:
                        self._player.set_dictionary_of_fences(
                            v_or_h_fence, new_fence_coordinate)
                        self._player1.reduce_num_of_player1_fences()
                        self._switch_player += 1
                        return True
                else:
                    if self._player2.get_num_of_player2_fences() > 0:
                        self._player.set_dictionary_of_fences(
                            v_or_h_fence, new_fence_coordinate)
                        self._player2.reduce_num_of_player2_fences()
                        self._switch_player -= 1
                        return True
        return False

    def is_winner(self, player):
        """Given the number representing the player, this method returns true if the player coordinate
        representing that number, is in the list of winning coordinates. Else the method should return false. """
        if player == 1:
            if self._player1.get_player1_coordinates() in self._player1.get_player1_winning_coordinates():
                return True
        else:
            if self._player2.get_player2_coordinates() in self._player2.get_player2_winning_coordinates():
                return True

        return False


class Board:
    """This class represents actionable parts of the game that center around the game board itself.
        We use this class to update moves on the board as well as to determine what moves are considered valid.
        This class actually contains the board we are working with to move around our pieces.
        This class also uses composition to get access to the Player, Player1 and Player2 classes.
        The reason we use these classes in the board class, is so that when our QuoridorGame class
        says to make a move, our game will be able to grab each players values from the game and place
        them in the proper locations onto the board."""

    def __init__(self):
        """ initializes board object with the following attributes: a board, player,
        player1 and player2. Each data member is set to private."""
        self._board = [[0 for i in range(9)] for x in range(9)]
        self._player = Player()
        self._player1 = Player1()
        self._player2 = Player2()

    def check_space_and_coord_pawn(self, player_coordinates):
        """Method checks for one things. 1) are the coordinates in the range of the board
        If this is true, method will return position of the board. Reason we return position of board, is so for
        our move_pawn method to verify that the new position we want to move to is empty. """
        if player_coordinates[0] in range(9) and player_coordinates[1] in range(9):
            return self._board[player_coordinates[1]][player_coordinates[0]]
        else:
            return

    def get_board(self):
        """returns the board we are working with."""
        return self._board

    def set_player_in_board(self, tuple_coordinates, player):
        """Given the new players coordinates and the player number, method updates
        the new players position in the board. This method indexes the board using the tuple
        coordinates as the numbers we should index to. Once we have indexed the board,
        the method sets the empty value into the value of the player given in the argument"""
        if player == 1:
            self._board[tuple_coordinates[0]][tuple_coordinates[1]] = 1
            return
        else:
            self._board[tuple_coordinates[0]][tuple_coordinates[1]] = 2
            return

    def remove_old_player_position(self, old_tuple_coordinates):
        """Given the old coordinates of any player, method set the that position
        on the board back to empty."""
        self._board[old_tuple_coordinates[1]][old_tuple_coordinates[0]] = 0
        return

    def player1_valid_moves(self, cur_coord, fences):
        """Given the current coordinate position and the number representing the player,
        this method adds new coordinates into a list of valid moves for that player.
        In our QuoridorGame class, we use this method to determine if the new coordinate is valid.
        If the new coordinate in the make_move class is not in the list set up by this method,
        the make_move method will return False and the player will not be able to move
        (they will need to re-pick a coordinate that is in the list of valid moves)"""
        p1_valid_list = self._player1.get_list_of_valid_moves_player1()
        if len(p1_valid_list) > 0:
            self._player1.reset_list_of_valid_moves_player1()

        if fences.get('v') is None:
            if cur_coord[0] in range(0, 8):
                p1_valid_list.append((cur_coord[0] + 1, cur_coord[1]))
            if cur_coord[0] in range(1, 9):
                p1_valid_list.append((cur_coord[0] - 1, cur_coord[1]))
        elif fences.get('v') is not None:
            if (cur_coord[0] + 1, cur_coord[1]) not in fences.get("v") and cur_coord[0] in range(0, 8):
                p1_valid_list.append((cur_coord[0] + 1, cur_coord[1]))
            if (cur_coord[0], cur_coord[1]) not in fences.get("v") and cur_coord[0] in range(1, 9):
                p1_valid_list.append((cur_coord[0] - 1, cur_coord[1]))

        if fences.get('h') is None:
            if cur_coord[1] in range(0, 8):
                p1_valid_list.append((cur_coord[0], cur_coord[1] + 1))
            if cur_coord[1] in range(1, 9):
                p1_valid_list.append((cur_coord[0], cur_coord[1] - 1))
        elif fences.get("h") is not None:
            if (cur_coord[0], cur_coord[1] + 1) not in fences.get("h") and cur_coord[1] in range(0, 8):
                p1_valid_list.append((cur_coord[0], cur_coord[1] + 1))
            if (cur_coord[0], cur_coord[1]) not in fences.get("h") and cur_coord[1] in range(1, 9):
                p1_valid_list.append((cur_coord[0], cur_coord[1] - 1))

        return p1_valid_list

    def player2_valid_moves(self, cur_coord, fences):
        """Given the current coordinate position and the number representing the player,
        this method adds new coordinates into a list of valid moves for that player.
        In our QuoridorGame class, we use this method to determine if the new coordinate is valid.
        If the new coordinate in the make_move class is not in the list set up by this method,
        the make_move method will return False and the player will not be able to move
        (they will need to re-pick a coordinate that is in the list of valid moves)"""
        p2_valid_list = self._player2.get_list_of_valid_moves_player2()
        if len(p2_valid_list) > 0:
            self._player2.reset_list_of_valid_moves_player2()

        if fences.get("v") is None:
            if cur_coord[0] in range(0, 8):
                p2_valid_list.append((cur_coord[0] + 1, cur_coord[1]))
            if cur_coord[0] in range(1, 9):
                p2_valid_list.append((cur_coord[0] - 1, cur_coord[1]))

        elif fences.get("v") is not None:
            if (cur_coord[0] + 1, cur_coord[1]) not in fences.get("v") and cur_coord[0] in range(0, 8):
                p2_valid_list.append((cur_coord[0] + 1, cur_coord[1]))
            if (cur_coord[0], cur_coord[1]) not in fences.get("v") and cur_coord[0] in range(1, 9):
                p2_valid_list.append((cur_coord[0] - 1, cur_coord[1]))

        if fences.get("h") is None:
            if cur_coord[1] in range(0, 8):
                p2_valid_list.append((cur_coord[0], cur_coord[1] + 1))
            if cur_coord[1] in range(1, 9):
                p2_valid_list.append((cur_coord[0], cur_coord[1] - 1))
        elif fences.get("h") is not None:
            if (cur_coord[0], cur_coord[1] + 1) not in fences.get("h") and cur_coord[1] in range(0, 8):
                p2_valid_list.append((cur_coord[0], cur_coord[1] + 1))
            if (cur_coord[0], cur_coord[1]) not in fences.get("h") and cur_coord[1] in range(1, 9):
                p2_valid_list.append((cur_coord[0], cur_coord[1] - 1))

        return p2_valid_list

    def edge_case(self, moves_list, current, new, fences):
        """given the list of coordinates from the update_valid_moves class,
        the current position and the new position, this method should append
        additional coordinates into the list from update_valid_moves method,
        if any edge cases are presented on the board. Regardless if any edge case exists,
        the method returns list of valid moves (updated or not)."""
        for i in moves_list:
            if self._board[i[1]][i[0]] != 0:
                if fences.get("h") is None:
                    if current[1] + 2 is new[1] and i[1] + 1 in range(9):
                        moves_list.append((i[0], i[1] + 1))
                    if current[1] - 2 is new[1] and i[1] - 1 in range(9):
                        moves_list.append((i[0], i[1] - 1))

                elif fences.get("h") is not None:
                    if (i[0], i[1]) in fences.get("h") or (i[0], i[1] + 1) in fences.get("h"):
                        if fences.get("v") is None:
                            moves_list.append((i[0] - 1, i[1]))
                            moves_list.append((i[0] + 1, i[1]))
                        elif fences.get("v") is not None:
                            if (i[0], i[1]) not in fences.get("v"):
                                moves_list.append((i[0] - 1, i[1]))
                            if (i[0] + 1, i[1]) not in fences.get("v"):
                                moves_list.append((i[0] + 1, i[1]))
                    elif (i[0], i[1]) not in fences.get("h"):
                        if current[1] - 2 is new[1] and i[1] - 1 in range(9):
                            moves_list.append((i[0], i[1] - 1))
                        if current[1] + 2 is new[1] and i[1] + 1 in range(9):
                            moves_list.append((i[0], i[1] + 1))
        return moves_list


class Player:
    """This class represents actions/ features that both the Player1 and Player2 class share.
        Most notably is the data member holding the fence positions in the game. Since it does not
        matter whose fence belongs to who when moving in the board, it makes the most sense to combine
        the positions for each player in this manner. This class will communicate with its child classes,
        Player1 and Player2, since the object of Player is mainly meant to be an extension of the two without
        the need of rewriting it for the other class. """

    def __init__(self):
        """initializes the object player. Player initializes the values player1, player2
        and a dictionary that holds the number of fence values in the board. """
        self._player1 = Player1()
        self._player2 = Player2()
        self._fence_dictionary = dict()
        self._f_coordinates_not_allowed = dict()

    def check_space_and_coord_fence(self, v_or_h_fences, new_fence):
        """Given the letter reprenting whether a fence is placed horizontally or vertically
        and the new fence coordinate, this method verifies that the letter in the argument
        is in fact the letter v or h, and checks if the new fence coordinate is already in the list
        of fence coordinates in our fence dictionary. Method also verifies that the new coordinate
        is within range of the board. If everything checks out fine, then the method will return True
        else it will return False."""
        if v_or_h_fences != "v" and v_or_h_fences != "h":
            return False
        if self._fence_dictionary.get(v_or_h_fences) is None:
            if new_fence not in self._f_coordinates_not_allowed.get(v_or_h_fences):
                if new_fence[0] in range(9) and new_fence[1] in range(9):
                    return True
        if self._fence_dictionary.get(v_or_h_fences) is not None:
            if new_fence not in self._fence_dictionary.get(v_or_h_fences):
                if new_fence not in self._f_coordinates_not_allowed.get(v_or_h_fences):
                    if new_fence[0] in range(9) and new_fence[1] in range(9):
                        return True

        return False

    def get_dictionary_fences(self):
        """This get method return the games fence dictionary. The fence dictionary stores all the fences that are
        currently on the board (both player 1 and player 2)"""
        return self._fence_dictionary

    def set_dictionary_of_fences(self, v_or_h, new_fence_position):
        """given a coordinate position, when this method is called,
        the coordinate is added onto the list of fences in the board.
        This method will be called by the place_fence method in the QuoridorGame class."""
        self._fence_dictionary.setdefault(v_or_h, [])
        self._fence_dictionary[v_or_h].append(new_fence_position)
        return

    def position_adjustment(self, current_tuple):
        """with this method we can work with the standard we are given.
        Since in the matrix x is normally row and y is normally column, we need to flip this around.
        """
        inverse_tuple = (current_tuple[1], current_tuple[0])
        return inverse_tuple

    def retrieve_player(self, player_argument):
        """Given the number representing the player (1 or 2) this method returns the
        class for the given player. This can be used to retrieve any methods from the specific player."""
        if player_argument == 1:
            return self._player1
        else:
            return self._player2

    def set_forbidden_fence_coordinates(self, v_or_h):
        """this method will only be called, when the starting board method is called in the beginning of the
        game. these coordinates are forbidden because they reside on the edges of the board. This has no effect on the
        game, since it would not block a player from moving their pawn, hence these fence spaces are disposable.
        """
        self._f_coordinates_not_allowed.setdefault(v_or_h, [])
        for column in range(9):
            if v_or_h == "v":
                self._f_coordinates_not_allowed[v_or_h].append((0, column))
                self._f_coordinates_not_allowed[v_or_h].append((9, column))
            if v_or_h == "h":
                self._f_coordinates_not_allowed[v_or_h].append((column, 0))
                self._f_coordinates_not_allowed[v_or_h].append((column, 9))

        return self._f_coordinates_not_allowed

    def get_forbidden_fence_coordinates(self, v_or_h):
        """when called and given the single string letter argument, h or v, this method returns the
        the fence dictionary of forbidden fence coordinates in the board."""
        return self._f_coordinates_not_allowed.get(v_or_h)


class Player1:
    """The Player1 class is primarily responsible for updating and recording
        data that belongs to this individual player. This class does not use composition whereas the Player,
        Board and QuoridorGame does. This class is primarily used when any of the other classes (not Player2 class)
        needs to make a reference or call for a value that is held within this class.
        The class primarily holds getter/setter methods that will return or alter the current state
        of each data member within the class.  This class is almost a mirror image of the Player2 class;
        however, as the game progresses the data in each class alters."""

    def __init__(self):
        """Creates a player 1 object. This initalizes the player with the following attributes:
        a list of moves the player can make, a number representing the player, the coordinates for the player,
        the number of pawns on the board, and the number of fences available to the player. """
        self._p1_list_of_valid_moves = []
        self._player1 = 1
        self._p1_coordinates = None
        self._p1_pawns_on_board = 0
        self._player1_fences = 10
        self._player1_winning_coordinates = []

    def get_num_of_p1_pawns_on_board(self):
        """returns the number of pawns in the board."""
        return self._p1_pawns_on_board

    def increment_num_of_p1_pawns(self, number):
        """alters the number of pawns on the board"""
        self._p1_pawns_on_board += number

    def get_player1_coordinates(self):
        """returns the coordinates for player 1"""
        return self._p1_coordinates

    def set_player1_coordinates(self, new_position):
        """when given a new position, method sets the players coordinates equal to the new position."""
        self._p1_coordinates = new_position
        return self._p1_coordinates

    def get_list_of_valid_moves_player1(self):
        """when called, method returns the list of valid moves a player can make."""
        return self._p1_list_of_valid_moves

    def reset_list_of_valid_moves_player1(self):
        """when called, this method empties the list of valid moves player 1 can make."""
        del self._p1_list_of_valid_moves[:]
        return self._p1_list_of_valid_moves

    def get_num_of_player1_fences(self):
        """when called, method returns the number of fences available for player 1 to use."""
        return self._player1_fences

    def reduce_num_of_player1_fences(self):
        """When called this method reduces the number of fences a player may use by 1."""
        self._player1_fences -= 1
        return self._player1_fences

    def set_winning_coordinates_list(self):
        """method is called at the starting board method in the QuoridorGame class,
        method sets the winning coordinates for player 1. If current coordinate for player 1 is in the list
        of winning coordinates, then player 1 wins."""
        for number in range(0, 9):
            self._player1_winning_coordinates.append((number, 8))
        return self._player1_winning_coordinates

    def get_player1_winning_coordinates(self):
        """when called, this method returns the winning coordinates for player 1. This method will be used to compare,
        player current coordinates. If current coordinates are in the winning coordinates, then the data member
        is_winner will be set to True. Once this data member is set to true, the game is over."""
        return self._player1_winning_coordinates


class Player2:
    """The Player2 class is primarily responsible for updating and recording data that
        belongs to this individual player. This class does not use composition whereas the Player,
        Board and QuoridorGame does. This class is primarily used when any of the other classes
        (not Player1 class) needs to make a reference or call for a value that is held within this class.
        The class primarily holds getter/setter methods that will return or alter the current state of each
        data member within the class. This class is almost a mirror image of the Player1 class; however,
        as the game progresses the data in each alters. """

    def __init__(self):
        """method creates a player 2 object. Method creates an object with a list of moves player 2 may take,
        the number representing player 2, the coordinates for player 2, the number of pawns on the board for player 2,
        the number of fences player 2 has."""
        self._p2_list_of_valid_moves = []
        self._player2_pawn = 2
        self._p2_coordinates = None
        self._p2_pawns_on_board = 0
        self._player2_fences = 10
        self._player2_winning_coordinates = []

    def get_num_of_p2_pawns_on_board(self):
        """returns the number of pawns in the board."""
        return self._p2_pawns_on_board

    def increment_num_of_p2_pawns(self, number):
        """alters the number of pawns on the board"""
        self._p2_pawns_on_board += number

    def get_player2_coordinates(self):
        """returns the coordinates for player 2"""
        return self._p2_coordinates

    def set_player2_coordinates(self, new_position):
        """when given a new position, method sets the players coordinates equal to the new position."""
        self._p2_coordinates = new_position
        return self._p2_coordinates

    def get_list_of_valid_moves_player2(self):
        """when called, method returns the list of valid moves a player can make."""
        return self._p2_list_of_valid_moves

    def reset_list_of_valid_moves_player2(self):
        """when called, this method empties the list of valid moves player 2 can make."""
        del self._p2_list_of_valid_moves[:]
        return self._p2_list_of_valid_moves

    def get_num_of_player2_fences(self):
        """when called, method returns the number of fences available for player 2 to use."""
        return self._player2_fences

    def reduce_num_of_player2_fences(self):
        """When called this method reduces the number of fences a player may use by 1."""
        self._player2_fences -= 1
        return self._player2_fences

    def set_player2_winning_coordinates(self):
        """method is called at the starting board method in the QuoridorGame class,
        method sets the winning coordinates for player 2. If current coordinate for player 2 is in the list
        of winning coordinates, then player 2 wins."""
        for number in range(0, 9):
            self._player2_winning_coordinates.append((number, 0))
        return self._player2_winning_coordinates

    def get_player2_winning_coordinates(self):
        """when called, this method returns the winning coordinates for player 2. This method will be used to compare,
        player current coordinates. If current coordinates are in the winning coordinates, then the data member
        is_winner will be set to True. Once this data member is set to true, the game is over."""
        return self._player2_winning_coordinates


def main():
    q = QuoridorGame()


if __name__ == "__main__":
    main()
