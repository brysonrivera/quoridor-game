# Bryson Rivera
# Quoridor Game, where 2 players race to reach the opposite end of the board
# the first player to make it to the end wins. Game involves moving past fences that are
# placed horizontally and vertically to get to the other side.

class QuoridorGame:
    """This class represents the Quoridor Game. 

        The __init__ method uses composition to turn each class in the .py file into a data member.
        The class also holds two additional data members, which will be used to
        determine which players turn it is (1 or 2) and a values that will be critical
        to initiating the starting values of the players on the board.
        This class is responsible for orchestrating the Quoridor game.
        Each players move will come from this class, as well as some other important methods
        that will be used to determine if a move is plausible given the restrictions of the game"""

    def __init__(self):
        """Creates a QuoridorGame object with the Board, player, player1, players, switch_player, initiate_board
            and is_winner data members. """
        self.board = Board()
        self.fences = Fences()
        self.player1 = Player1(1)
        self.player2 = Player2(2)
        self.switch_player = 1
        self.game_not_won = True
        self.starting_board()

    def get_player_coordinates(self, player_num):
        """given the number representing the player, method returns the current coordinates for that player."""
        if player_num == 1:
            return self.player1.get_player_coordinates()

        return self.player2.get_player_coordinates()

    def update_players_position(self, new_coordinates, player_num):
        """Given the new coordinates and the number representing the
        player this method makes sure that for each player there is only one pawn on the board.
        Method also updates players current position and updates the the pawn move in the board.
        This method should only be called, when we have verified that the move is valid."""
        player = self.player1 if player_num == 1 else self.player2
        matrix_position = self.position_adjustment(new_coordinates)
        player.increment_num_of_pawns(1)
        if player.get_player_coordinates() is not None:
            prev = player.get_player_coordinates()
            if player.get_num_of_pawns_on_board() > 1:
                player.increment_num_of_pawns(-1)
                self.board.remove_old_player_position(prev)
        self.board.set_player_in_board(matrix_position, player)
        player.set_player_coordinates(new_coordinates)
        self.switch_player = 2 if player_num == 1 else 1
        return

    def visualize_board(self):
        """method returns the board we are currently working with, showing the position of the values in the list."""
        best_visualization = ""
        for i in self.board.get_board():
            best_visualization += str(i) + "\n"
        print(best_visualization)
        return True

    def get_player_positions(self):
        """method that helps us see the current coordinates for each player."""
        print(f"Player 1 position: {self.player1.get_player_coordinates()}")
        print(f"Player 2 position: {self.player2.get_player_coordinates()}")

    def starting_board(self) -> object:
        """Method is only called once at the beginning of the game, to initiate the board."""
        # initialize which fence positions are forbidden (edges of the board)
        self.fences.set_forbidden_fence_coordinates("v")
        self.fences.set_forbidden_fence_coordinates("h")

        fences = self.fences.get_dictionary_fences()

        # initialize player 1
        self.board.valid_moves((4, 0), fences, self.player1)
        self.update_players_position((4, 0), 1)
        self.player1.set_winning_coordinates()

        # initialize player 2
        self.board.valid_moves((4, 8), fences, self.player2)
        self.update_players_position((4, 8), 2)
        self.player2.set_winning_coordinates()

        return True

    def move_pawn(self, player_num, new_coord):
        """given the number representing the player and the new coordinate value,
        this method is the center method that will be used to move a player to a new position.
        This method calls the initial_checks method. If initial_checks return True, method will then call
        the Board classes update_valid_moves method and edge_case_player method. If new_coordinates
        is in the list generated from the board classes methods, then the method should call the
        update_players_position method. Finally, the method will return True. If any of the tests fail, method returns
        False """
        player = self.player1 if player_num == 1 else self.player2

        if self.game_not_won:

            # get dictionary of fences currently on board
            fences = self.fences.get_dictionary_fences()

            # verify player turn and check that space we want to move into is empty
            if self.switch_player is player_num and self.board.check_space_and_coord_pawn(new_coord) == 0:

                # create a list of valid spaces the current player can move to
                moves = self.board.valid_moves(
                    self.get_player_coordinates(player_num), fences, player)

                # if edge case spaces exist where player can move to, add them to the list of valid moves.
                new_list = self.board.edge_case(
                    moves, self.get_player_coordinates(player_num), new_coord, fences)

                if new_coord in new_list:
                    self.update_players_position(new_coord, player_num)
                    if player.get_player_coordinates() in player.get_winning_coordinates():
                        self.game_not_won = False
                    return True

        return False

    def place_fence(self, player_num, v_or_h_fence, new_fence_coordinate):
        """Given the numbers representing the player, letter representing whether, the fence is vertical or horizontal
        and the new coordinate, this method will add a coordinate into a dictionary that will be
        used by one of the Board methods to determine if a move is valid or not. In order to determine if the placement
        of the fence is valid or not, we call the Player classes check_space_and_coord_fence method.
        If the value returns True, meaning the new coordinate for the fence is in range of the board and no other
        fence with the same coordinate exists, the move is valid and should be recorded into the
        fence_dictionary data member."""
        player = self.player1 if player_num == 1 else self.player2

        if self.game_not_won:

            checks_systems = self.fences.check_space_and_coord_fence(
                v_or_h_fence, new_fence_coordinate)
            if checks_systems and self.switch_player is player_num:
                if player.get_num_of_fences() > 0:
                    self.fences.set_dictionary_of_fences(
                        v_or_h_fence, new_fence_coordinate)
                    player.reduce_num_of_fences()
                    self.switch_player = 2 if player_num == 1 else 1
                    return True

        return False

    def is_winner(self, player_num):
        """Given the number representing the player, this method returns true if the player coordinate
        representing that number, is in the list of winning coordinates. Else the method should return false. """
        player = self.player1 if player_num == 1 else self.player2

        if player.get_player_coordinates() in player.get_winning_coordinates():
            return True

        return False

    def position_adjustment(self, current_tuple):
        """with this method we can work with the standard we are given.
        Since in the matrix x is normally row and y is normally column, we need to flip this around.
        """
        x, y = current_tuple[0], current_tuple[1]
        inverse_tuple = (y, x)
        return inverse_tuple


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
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def check_space_and_coord_pawn(self, player_coordinates):
        """Method checks for one things. 1) are the coordinates in the range of the board
        If this is true, method will return position of the board. Reason we return position of board, is so for
        our move_pawn method to verify that the new position we want to move to is empty. """
        x, y = player_coordinates[0], player_coordinates[1]
        if player_coordinates[0] in range(9) and player_coordinates[1] in range(9):
            return self.board[y][x]
        else:
            return

    def get_board(self):
        """returns the board we are working with."""
        return self.board

    def set_player_in_board(self, tuple_coordinates, player):
        """Given the new players coordinates and the player number, method updates
        the new players position in the board. This method indexes the board using the tuple
        coordinates as the numbers we should index to. Once we have indexed the board,
        the method sets the empty value into the value of the player given in the argument"""
        x, y = tuple_coordinates[0], tuple_coordinates[1]
        if player == 1:
            self.board[x][y] = 1
            return
        else:
            self.board[x][y] = 2
            return

    def remove_old_player_position(self, old_tuple_coordinates):
        """Given the old coordinates of any player, method set the that position
        on the board back to empty."""
        x, y = old_tuple_coordinates[0], old_tuple_coordinates[1]
        self.board[y][x] = 0
        return

    def valid_moves(self, cur_coord, fences, player):
        """Given the current coordinate position and the number representing the player,
        this method adds new coordinates into a list of valid moves for that player.
        In our QuoridorGame class, we use this method to determine if the new coordinate is valid.
        If the new coordinate in the make_move class is not in the list set up by this method,
        the make_move method will return False and the player will not be able to move
        (they will need to re-pick a coordinate that is in the list of valid moves)"""

        valid_list = player.get_list_of_valid_moves()
        if len(valid_list) > 0:
            player.reset_list_of_valid_moves()

        if fences.get('v') is None:
            if cur_coord[0] in range(0, 8):
                valid_list.append((cur_coord[0] + 1, cur_coord[1]))
            if cur_coord[0] in range(1, 9):
                valid_list.append((cur_coord[0] - 1, cur_coord[1]))
        elif fences.get('v') is not None:
            if (cur_coord[0] + 1, cur_coord[1]) not in fences.get("v") and cur_coord[0] in range(0, 8):
                valid_list.append((cur_coord[0] + 1, cur_coord[1]))
            if (cur_coord[0], cur_coord[1]) not in fences.get("v") and cur_coord[0] in range(1, 9):
                valid_list.append((cur_coord[0] - 1, cur_coord[1]))

        if fences.get('h') is None:
            if cur_coord[1] in range(0, 8):
                valid_list.append((cur_coord[0], cur_coord[1] + 1))
            if cur_coord[1] in range(1, 9):
                valid_list.append((cur_coord[0], cur_coord[1] - 1))
        elif fences.get("h") is not None:
            if (cur_coord[0], cur_coord[1] + 1) not in fences.get("h") and cur_coord[1] in range(0, 8):
                valid_list.append((cur_coord[0], cur_coord[1] + 1))
            if (cur_coord[0], cur_coord[1]) not in fences.get("h") and cur_coord[1] in range(1, 9):
                valid_list.append((cur_coord[0], cur_coord[1] - 1))

        return valid_list

    def edge_case(self, moves_list, current, new, fences):
        """given the list of coordinates from the update_valid_moves class,
        the current position and the new position, this method should append
        additional coordinates into the list from update_valid_moves method,
        if any edge cases are presented on the board. Regardless if any edge case exists,
        the method returns list of valid moves (updated or not)."""
        for i in moves_list:
            if self.board[i[1]][i[0]] != 0:
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


class Fences:
    """
    This a data class used to represent Fences in the QuoridorGame. An instance of this object will be created 
    when an instance of the QuoridorGame is created. This class becomes a data member of the QuoridorGame
    via Composition. Class is mainly used to get and set fences in the QuoridorGame. Fence class also has a method
    that is used to check if the position and coordinate of a fence is available for a player to place. 
    """

    def __init__(self):
        """initializes the object player. Player initializes the values player1, player2
        and a dictionary that holds the number of fence values in the board. """
        self.fence_dictionary = dict()
        self.f_coordinates_not_allowed = dict()

    def check_space_and_coord_fence(self, v_or_h_fences, new_fence):
        """Given the letter reprenting whether a fence is placed horizontally or vertically
        and the new fence coordinate, this method verifies that the letter in the argument
        is in fact the letter v or h, and checks if the new fence coordinate is already in the list
        of fence coordinates in our fence dictionary. Method also verifies that the new coordinate
        is within range of the board. If everything checks out fine, then the method will return True
        else it will return False."""
        if v_or_h_fences != "v" and v_or_h_fences != "h":
            return False
        if self.fence_dictionary.get(v_or_h_fences) is None:
            if new_fence not in self.f_coordinates_not_allowed.get(v_or_h_fences):
                if new_fence[0] in range(9) and new_fence[1] in range(9):
                    return True
        if self.fence_dictionary.get(v_or_h_fences) is not None:
            if new_fence not in self.fence_dictionary.get(v_or_h_fences):
                if new_fence not in self.f_coordinates_not_allowed.get(v_or_h_fences):
                    if new_fence[0] in range(9) and new_fence[1] in range(9):
                        return True
        return False

    def get_dictionary_fences(self):
        """This get method return the games fence dictionary. The fence dictionary stores all the fences that are
        currently on the board (both player 1 and player 2)"""
        return self.fence_dictionary

    def set_dictionary_of_fences(self, v_or_h, new_fence_position):
        """given a coordinate position, when this method is called,
        the coordinate is added onto the list of fences in the board.
        This method will be called by the place_fence method in the QuoridorGame class."""
        self.fence_dictionary.setdefault(v_or_h, [])
        self.fence_dictionary[v_or_h].append(new_fence_position)
        return

    def set_forbidden_fence_coordinates(self, v_or_h):
        """this method will only be called, when the starting board method is called in the beginning of the
        game. these coordinates are forbidden because they reside on the edges of the board. This has no effect on the
        game, since it would not block a player from moving their pawn, hence these fence spaces are disposable.
        """
        self.f_coordinates_not_allowed.setdefault(v_or_h, [])
        for column in range(9):
            if v_or_h == "v":
                self.f_coordinates_not_allowed[v_or_h].append((0, column))
                self.f_coordinates_not_allowed[v_or_h].append((9, column))
            if v_or_h == "h":
                self.f_coordinates_not_allowed[v_or_h].append((column, 0))
                self.f_coordinates_not_allowed[v_or_h].append((column, 9))

        return self.f_coordinates_not_allowed

    def get_forbidden_fence_coordinates(self, v_or_h):
        """when called and given the single string letter argument, h or v, this method returns the
        the fence dictionary of forbidden fence coordinates in the board."""
        return self.f_coordinates_not_allowed.get(v_or_h)


class QuoridorPlayer:
    """
    Data Class represents a general Player object for the Quoridor Game. Object has a few built in attributes, such as: 
        - the list of valid moves they can make
        - coordinates of where player is currently located.
        - number of pawns on the board (when there is more than 1 pawn on the board, one pawn needs to be removed)
        - number of fences available (when a player places a fence, number of fences available is decremented by 1)
        - array of winning coordinates (opponents baseline)

    Methods either alters (basic CRUD) or retrieves the data for the Player object. 
     """

    def __init__(self, player):
        """method creates a player object. Method creates an object with a list of moves a player may take,
        the number representing player 2, the coordinates for player 2, the number of pawns on the board for player 2,
        the number of fences player 2 has."""
        self.list_of_valid_moves = []
        self.player_pawn = player
        self.coordinates = None
        self.pawns_on_board = 0
        self.fences_available = 10
        self.winning_coordinates = []

    def get_num_of_pawns_on_board(self):
        """returns the number of pawns in the board."""
        return self.pawns_on_board

    def increment_num_of_pawns(self, number):
        """alters the number of pawns on the board"""
        self.pawns_on_board += number

    def get_player_coordinates(self):
        """returns the coordinates for player 2"""
        return self.coordinates

    def set_player_coordinates(self, new_position):
        """when given a new position, method sets the players coordinates equal to the new position."""
        self.coordinates = new_position
        return self.coordinates

    def get_list_of_valid_moves(self):
        """when called, method returns the list of valid moves a player can make."""
        return self.list_of_valid_moves

    def reset_list_of_valid_moves(self):
        """when called, this method empties the list of valid moves player 2 can make."""
        del self.list_of_valid_moves[:]
        return self.list_of_valid_moves

    def get_num_of_fences(self):
        """when called, method returns the number of fences available for player 2 to use."""
        return self.fences_available

    def reduce_num_of_fences(self):
        """When called this method reduces the number of fences a player may use by 1."""
        self.fences_available -= 1
        return self.fences_available

    def get_winning_coordinates(self):
        """when called, this method returns the winning coordinates for player 2. This method will be used to compare,
        player current coordinates. If current coordinates are in the winning coordinates, then the data member
        is_winner will be set to True. Once this data member is set to true, the game is over."""
        return self.winning_coordinates

    def set_winning_coordinates(self):
        """winning coordinates are unique to the player; therefore, when inheriting from this parent class, child-class should have a method 
        including the winning coordinates for that specific player. NOTE: winning coordinates include all the coordinates in an opponents baseline on the opposite
        side of the board. """
        pass


class Player1(QuoridorPlayer):
    """The Player1 class is primarily responsible for updating and recording
        data that belongs to player 1. Class inherits data and methods from the Player Class.
        """

    def __init__(self, player):
        super().__init__(player)

    def set_winning_coordinates(self):
        """method is called at the starting board method in the QuoridorGame class,
        method sets the winning coordinates for player 1. If current coordinate for player 1 is in the list
        of winning coordinates, then player 1 wins."""
        for number in range(0, 9):
            self.winning_coordinates.append((number, 8))
        return self.winning_coordinates


class Player2(QuoridorPlayer):
    """The Player2 class is primarily responsible for updating and recording data that
        belongs to player 2. Class inherits data and methods from the Player Class. """

    def __init__(self, player):
        super().__init__(player)

    def set_winning_coordinates(self):
        """method is called at the starting board method in the QuoridorGame class,
        method sets the winning coordinates for player 2. If current coordinate for player 2 is in the list
        of winning coordinates, then player 2 wins."""
        for number in range(0, 9):
            self.winning_coordinates.append((number, 0))
        return self.winning_coordinates


def main():
    q = QuoridorGame()


if __name__ == "__main__":
    main()
