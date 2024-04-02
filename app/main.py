from collections import Counter, defaultdict
from itertools import combinations
from typing import Optional


class NotEnoughShipsError(Exception):
    pass


class CountShipError(Exception):
    pass


class ShipPositionError(Exception):
    pass


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int, int],
            end: tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)
        ]
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Optional[Deck]:

        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

        return None

    def fire(self, row: int, column: int) -> str | None:
        deck = self.get_deck(row, column)

        if deck is not None:
            deck.is_alive = False

            if all(not deck.is_alive for deck in self.decks):
                self.is_drowned = True
                return "Sunk!"

            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = {}

        ships_object = [Ship(*ship) for ship in ships]

        for ship in ships_object:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field(ships_object)

    def fire(self, location: tuple) -> str:

        if location in self.field:
            return self.field[location].fire(*location)

        return "Miss!"

    def print_field(self) -> None:
        battlefield = "┌" + "───┬" * 9 + "───┐\n"

        for row in range(10):
            battlefield += "│"
            for column in range(10):
                if (row, column) in self.field:
                    ship = self.field[(row, column)]
                    if ship.is_drowned:
                        battlefield += " x "
                    else:
                        for deck in ship.decks:
                            if deck.row == row and deck.column == column:
                                if deck.is_alive:
                                    battlefield += u" \u25A1 "
                                else:
                                    battlefield += " * "
                else:
                    battlefield += " ~ "
                battlefield += "│"
            if row < 9:
                battlefield += "\n" + "├" + "───┼" * 9 + "───┤\n"

        battlefield += "\n└" + "───┴" * 9 + "───┘"
        print(battlefield)


    def _validate_field(self, ships: list[Ship]) -> None:

        if len(ships) != 10:
            raise NotEnoughShipsError("Total number of ships should be 10.")

        ship_decks_counts = Counter(len(ship.decks) for ship in ships)

        if ship_decks_counts[1] != 4:
            raise CountShipError("There should be 4 single-deck ships.")

        if ship_decks_counts[2] != 3:
            raise CountShipError("There should be 3 double-deck ships.")

        if ship_decks_counts[3] != 2:
            raise CountShipError("There should be 2 three-deck ships.")

        if ship_decks_counts[4] != 1:
            raise CountShipError("There should be 1 four-deck ship.")

        for location, ship in self.field.items():
            for neighbor_row in range(location[0] - 1, location[0] + 1):
                for neighbor_column in range(location[1] - 1, location[1] + 1):
                    neighbor_location = (neighbor_row, neighbor_column)

                    if (
                            neighbor_location in self.field
                            and not self.field[neighbor_location] == ship
                    ):
                        raise ShipPositionError(
                            "Ships shouldn't be located in "
                            "the neighboring cells."
                        )
