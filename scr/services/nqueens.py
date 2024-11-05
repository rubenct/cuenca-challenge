def n_queens(n: int, row: int, cols: int, diagonal_45: int, diagonal_135: int):
    """
    Function that find all solutions to n queens, using the backtracking algorithm
    :param n: size of the board and number of queens
    :param row: number of the row that evaluate
    :param cols: columns that have been occupied
    :param diagonal_45: diagonal at 45 degrees
    :param diagonal_135: diagonal at 135 degrees
    :return: List of lists with all solutions to n queens
    """

    #when row == n the algorithm have been found a solution and return a list:
    if row == n:
        yield []
        return

    #Calculates a bitmask of all valid positions
    # where a queen can be placed in the current row
    available_positions = ((1 << n)-1) & ~(cols | diagonal_45 | diagonal_135)

    #If available_position is different of zero, there are available positions
    while available_positions:
        #Gets the "1" LSB, that is, the rightmost bit "1"
        position = available_positions & -available_positions
        #Get the position available rightmost,
        column = bin(position-1).count('1')
        #Delegate the generation of solutions values to the nex recursive call.
        yield from ([column] + solution
                    for solution in
                    n_queens
                        (
                        n,
                        row+1,
                        cols | position,
                        (diagonal_45 | position) << 1,
                        (diagonal_135 | position) >> 1
                        )
                    )
        #Elimitate the LBS
        available_positions &= available_positions-1
