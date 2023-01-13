from typing import Union, Tuple, Dict


class Cell:

    state = 0

    def __init__(self, init_state = 0):
        self.state = init_state

    def set_white(self):
        self.state = 1

    def set_black(self):
        self.state = 2


class CellMove:

    origin_x: int = -1
    origin_y: int = -1
    destination_x: int = -1
    destination_y: int = -1

    def __init__(self, x: int, y: int):
        self.origin_x = x
        self.origin_y = y

    def set_destination(self, x: int, y: int):
        self.destination_x = x
        self.destination_y = y

    def is_valid(self) -> bool:
        if self.origin_y == self.destination_y and self.origin_x == self.destination_x:
            return False
        elif abs(self.origin_y - self.destination_y) > 2 or abs(self.origin_x - self.destination_x) > 2:
            return False
        return True

    def replicate(self) -> bool:
        if abs(self.origin_x - self.destination_x) == 2:
            return False
        elif abs(self.origin_y - self.destination_y) == 2:
            return False
        return True


class AtaxxBoard:

    def __init__(self) -> None:
        self.board = [[Cell(0) for _ in range(7)] for _ in range(7)]
        self.board[0][0].state = 1
        self.board[6][6].state = 1
        self.board[0][6].state = 2
        self.board[6][0].state = 2
        self.row_names = ["A", "B", "C", "D", "E", "F", "G"]
        self.col_names = ["1", "2", "3", "4", "5", "6", "7"]

    def in_progress(self) -> bool:
        is_board_full = True
        for row in self.board:
            for cell in row:
                if cell.state == 0:
                    is_board_full = False
                    break

        score = self.get_score()
        if score.get(1, -1) == 0:
            return False
        if score.get(2, -1) == 0:
            return False
        return not is_board_full

    def get_score(self) -> Dict[int, int]:
        result = {1: 0, 2: 0}
        for row in self.board:
            for cell in row:
                if cell.state != 0:
                    result[cell.state] += 1
        return result

    def print_score(self) -> None:
        print(f"Final result: {self.get_score()}")

    def print_board(self) -> None:
        line_strings = []
        for ind, line in enumerate(self.board):
            line_string = f"{self.row_names[ind]} - | "
            for cell in line:
                line_string += f"{str(cell.state)} | "
            line_strings.append(line_string)
        header = "    "
        for i in range(0, 7):
            header += f"  {i+1} "
        header += "\n" + "_" * len(header)
        board_string = f'\n'.join([header] + line_strings)
        print(board_string)

    def get_cell(self, cell_input: str) -> Union[None, Tuple[Cell, int, int]]:
        cell_input = cell_input.strip()
        if len(cell_input) != 2:
            return None
        try:
            row_number = self.row_names.index(cell_input[0].upper())
        except ValueError:
            return None
        try:
            col_number = self.col_names.index(cell_input[1].upper())
        except ValueError:
            return None
        row = self.board[row_number]
        return row[col_number], row_number, col_number

    def convert_adjacent_cells(self, cell_state, x, y):
        neighbours = []
        for neighbour_x in range(x-1, x+2, 1):
            for neighbour_y in range(y-1, y+2, 1):
                if not (neighbour_x == x and neighbour_y == y) and 0 <= neighbour_x < 7 and 0 <= neighbour_y < 7:
                    neighbours.append((neighbour_x, neighbour_y))

        print(neighbours)
        for n_x, n_y in neighbours:
            if self.board[n_x][n_y].state != 0:
                self.board[n_x][n_y].state = cell_state

    def do_move(self, cell_move: CellMove) -> None:
        origin_state = self.board[cell_move.origin_x][cell_move.origin_y].state
        if not cell_move.replicate():
            self.board[cell_move.origin_x][cell_move.origin_y].state = 0

        self.board[cell_move.destination_x][cell_move.destination_y].state = origin_state
        self.convert_adjacent_cells(origin_state, cell_move.destination_x, cell_move.destination_y)
