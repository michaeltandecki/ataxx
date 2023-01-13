

from board import AtaxxBoard, CellMove



if __name__ == "__main__":

    game_board = AtaxxBoard()

    active_player = 1

    # game loop
    while game_board.in_progress():
        # print board
        game_board.print_board()

        # get input
        print(f"Make your move, player {active_player}, current score: {game_board.get_score()}")
        correct_origin = False
        cell_move = None
        while not correct_origin:
            origin_cell_input = input("Choose the cell to move from: ")
            origin_cell, x, y = game_board.get_cell(origin_cell_input)
            if origin_cell is None or origin_cell.state != active_player:
                print(f"{origin_cell_input} is not a valid cell for you, try again")
            else:
                cell_move = CellMove(x, y)
                correct_origin = True

        correct_destination = False
        while not correct_destination:
            destination_cell_input = input("Choose the destination of the cell: ")
            destination_cell, x, y = game_board.get_cell(destination_cell_input)
            if destination_cell is None:
                print(f"Invalid cell input: {destination_cell_input}, try again.")
            elif destination_cell.state != 0:
                print(f"Destination cell {destination_cell_input} is occupied, try again.")
            else:
                cell_move.set_destination(x, y)
                if cell_move.is_valid():
                    correct_destination = True
                else:
                    print("Incorrect move, try again")

        game_board.do_move(cell_move)

        active_player = active_player % 2 + 1

    game_board.print_board()
    game_board.print_score()