from Quoridor import QuoridorGame


class TestClass:
    """
    Tests include
    - Turn Validation
    - Movement Placement Validation (pawns can move orthogonally one space at a time)
    - Fence Placemenet Validation (players can place their pawns either horizontally or vertically)
    - Fence Capacity Validation (app keeps track of the number of fences a player has placed/ has available.)
    """

    def test_one(self):
        """If player 1 moves to a valid space on their turn, return True"""
        q = QuoridorGame()
        bool = q.move_pawn(1, (4, 1))
        assert bool is True

    def test_two(self):
        """If player 2 moves to a valid space on their turn, return True """
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        bool = q.move_pawn(2, (5, 8))
        assert bool is True

    def test_three(self):
        """If player 1 makes invalid move, return False"""
        q = QuoridorGame()
        bool = q.move_pawn(1, (2, 1))
        assert bool is False

    def test_four(self):
        """If player 2 makes invalid move, return False"""
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        bool = q.move_pawn(2, (3, 7))
        assert bool is False

    def test_five(self):
        """If player 1 tries to move out of turn, return false"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        bool = q.move_pawn(1, (3, 1))
        assert bool is False

    def test_six(self):
        """If player 1 tries to place a fence out of turn, return false"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        bool = q.place_fence(1, 'h', (3, 3))
        assert bool is False

    def test_seven(self):
        """If player 2 tries to move out of turn, return false"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q.move_pawn(2, (3, 8))
        bool = q.move_pawn(2, (2, 8))
        assert bool is False

    def test_eight(self):
        """If player 1 tries to move to the same space they are currently in, return False"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q.move_pawn(2, (4, 7))
        bool = q.move_pawn(1, (3, 0))
        assert bool is False

    def test_nine(self):
        """If player 2 tries to move to the same space they are currently in, return False"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q.move_pawn(2, (4, 7))
        q.move_pawn(1, (2, 0))
        bool = q.move_pawn(2, (4, 7))
        assert bool is False

    def test_ten(self):
        """If player 1 tries to place a fence in a space where they previously placed a fence, return False"""
        q = QuoridorGame()
        q.place_fence(1, 'h', (3, 0))
        q.move_pawn(2, (4, 7))
        bool = q.place_fence(1, 'h', (3, 0))
        assert bool is False

    def test_eleven(self):
        """If player 2 tries to place a fence in a space where they previously placed a fence, return False """
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q.place_fence(2, 'v', (4, 7))
        q.move_pawn(1, (3, 1))
        bool = q.place_fence(2, 'v', (4, 7))
        assert bool is False

    def test_twelve(self):
        """If a player tries to place a fence in a space where a fence was previously placed by the opposite player, return False"""
        q = QuoridorGame()
        q.place_fence(1, 'v', (4, 7))
        bool = q.place_fence(2, 'v', (4, 7))
        assert bool is False

    def test_thirteen(self):
        """A player can place at most 10 fences on the board. Here we are testing whether a player will receive any errors
        when they try to place all the fences they have available. If test returns no errors, player is 
        able to successfully place all their fences in unique positions in the board"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q.place_fence(2, 'v', (1, 1))
        q.move_pawn(1, (2, 0))
        q.place_fence(2, 'h', (2, 1))
        q.move_pawn(1, (1, 0))
        q.place_fence(2, 'v', (3, 1))
        q.move_pawn(1, (0, 0))
        q.place_fence(2, 'h', (4, 1))
        q.move_pawn(1, (0, 1))
        q.place_fence(2, 'v', (5, 1))
        q.move_pawn(1, (0, 2))
        q.place_fence(2, 'h', (6, 1))
        q.move_pawn(1, (0, 3))
        q.place_fence(2, 'v', (7, 1))
        q.move_pawn(1, (0, 4))
        q.place_fence(2, 'h', (8, 1))
        q.move_pawn(1, (0, 5))
        q.place_fence(2, 'v', (1, 2))
        q.move_pawn(1, (0, 6))
        bool = q.place_fence(2, 'h', (2, 2))
        assert bool is True

    def test_fourteen(self):
        """If player tries to place more fences than their max (10) available, it should return false"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q.place_fence(2, 'v', (1, 1))
        q.move_pawn(1, (2, 0))
        q.place_fence(2, 'h', (2, 1))
        q.move_pawn(1, (1, 0))
        q.place_fence(2, 'v', (3, 1))
        q.move_pawn(1, (0, 0))
        q.place_fence(2, 'h', (4, 1))
        q.move_pawn(1, (0, 1))
        q.place_fence(2, 'v', (5, 1))
        q.move_pawn(1, (0, 2))
        q.place_fence(2, 'h', (6, 1))
        q.move_pawn(1, (0, 3))
        q.place_fence(2, 'v', (7, 1))
        q.move_pawn(1, (0, 4))
        q.place_fence(2, 'h', (8, 1))
        q.move_pawn(1, (0, 5))
        q.place_fence(2, 'v', (1, 2))
        q.move_pawn(1, (0, 6))
        q.place_fence(2, 'h', (2, 2))
        q.move_pawn(1, (0, 7))
        # 11th fence for player 2. invalid move
        bool = q.place_fence(2, 'v', (3, 2))
        assert bool is False

    def test_fifteen(self):
        """If a player tries to share the same space with the oppsite player, return False"""
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        bool = q.move_pawn(2, (4, 4))
        assert bool is False

    def test_sixteen(self):
        """EDGE CASE -- When a player is orthogonally adjacent to another player (right next to each other), if a player is able
        to jump over another pawn, return True -- """
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        bool = q.move_pawn(2, (4, 3))
        assert bool is True

    def test_seventeen(self):
        """EDGE CASE: In a specific instance where a player is orthogonally adjacent to their opponent (right next to a player), but there is a 
        fence behind the opponent, a player is allowed to move diagonally (if player is in front of opponent, they are now next to each other horizontally). 
        When the above rule is implemented, this test case should return True. """
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        q.place_fence(2, "h", (4, 6))
        bool = q.move_pawn(1, (5, 5))
        assert bool is True

    def test_eighteen(self):
        """If a player tries moving to a space where a fence is blocking them to move to that space, return False"""
        q = QuoridorGame()
        q.place_fence(1, "h", (4, 8))
        bool = q.move_pawn(2, (4, 7))
        assert bool is False

    def test_nineteen(self):
        """if a player has not won, the method .is_winner(player) should return False. Only way for a player to win is if they have reached their opponents baseline."""
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        q.move_pawn(2, (4, 3))
        bool = q.is_winner(1)
        assert bool is False

    def test_twenty(self):
        """If a player has won, then .is_winner(player) should return True"""
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        q.move_pawn(2, (4, 3))
        q.move_pawn(1, (4, 5))
        q.move_pawn(2, (4, 2))
        q.move_pawn(1, (4, 6))
        q.move_pawn(2, (4, 1))
        q.move_pawn(1, (4, 7))
        q.move_pawn(2, (4, 0))
        bool = q.is_winner(2)
        assert bool is True

    def test_twenty_one(self):
        """If a player has won, then .is_winner(player) should return False if the parameter value for the method is not the correct player. """
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        q.move_pawn(2, (4, 3))
        q.move_pawn(1, (4, 5))
        q.move_pawn(2, (4, 2))
        q.move_pawn(1, (4, 6))
        q.move_pawn(2, (4, 1))
        q.move_pawn(1, (4, 7))
        q.move_pawn(2, (4, 0))
        bool = q.is_winner(1)
        assert bool is False

    def test_twenty_two(self):
        """If a player has reached the opponents baseline, that player has won. When a player reaches another players base coordinate, any other move after
        should not matter, and we should return False"""
        q = QuoridorGame()
        q.move_pawn(1, (4, 1))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (4, 2))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (4, 3))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (4, 4))
        q.move_pawn(2, (4, 3))
        q.move_pawn(1, (4, 5))
        q.move_pawn(2, (4, 2))
        q.move_pawn(1, (4, 6))
        q.move_pawn(2, (4, 1))
        q.move_pawn(1, (4, 7))
        q.move_pawn(2, (4, 0))
        bool = q.move_pawn(1, (4, 8))
        assert bool is False

    def test_twenty_three(self):
        """If a player attempts to move out of range, we should return False"""
        q = QuoridorGame()
        q.move_pawn(1, (3, 0))
        q. move_pawn(2, (4, 7))
        q.move_pawn(1, (2, 0))
        q.move_pawn(2, (4, 6))
        q.move_pawn(1, (1, 0))
        q.move_pawn(2, (4, 5))
        q.move_pawn(1, (0, 0))
        q.move_pawn(2, (4, 3))
        bool = q.move_pawn(1, (8, 0))
        assert bool is False
