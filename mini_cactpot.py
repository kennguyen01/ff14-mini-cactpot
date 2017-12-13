import itertools


# Text decoration
class Color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def current_board(positions):
    """
    Graphical display of the board
    :param positions: dictionary
    :return: string containing integer
    """
    print('--------------')
    line_1 = Color.BOLD + '{}  {}  {}  {}  {}\n'.format('4', '5', '6', '7', '8') + Color.END
    line_2 = Color.BOLD + '3' + Color.END + '  {}  {}  {}\n'.format(positions['a'], positions['b'], positions['c'])
    line_3 = Color.BOLD + '2' + Color.END + '  {}  {}  {}\n'.format(positions['d'], positions['e'], positions['f'])
    line_4 = Color.BOLD + '1' + Color.END + '  {}  {}  {}\n'.format(positions['g'], positions['h'], positions['i'])
    return line_1 + line_2 + line_3 + line_4


def user_numbers():
    """
    Get user input of 4 picked numbers
    :return: dictionary
    """
    print('--------------')
    print('Enter the 4 numbers you picked by its letter, then number.')
    print(Color.UNDERLINE + 'For example' + Color.END +
          ": if position 'a' is 1 then you enter 'a 1' (separated by space).\n")
    pos_1, num_1 = input('-> 1st number: ').split()
    pos_2, num_2 = input('-> 2nd number: ').split()
    pos_3, num_3 = input('-> 3rd number: ').split()
    pos_4, num_4 = input('-> 4th number: ').split()
    return {pos_1: num_1, pos_2: num_2, pos_3: num_3, pos_4: num_4}


def fill_numbers(user_inputs, board_pos):
    """
    Change board value based on user inputs
    :param user_inputs: dictionary
    :param board_pos: dictionary
    :return: dictionary
    """
    for key, value in user_inputs.items():
        for letter in board_pos:
            if letter == key:
                board_pos[letter] = int(value.strip())
    return board_pos


def board_lines(positions):
    """
    Return dictionary for 3 number lines on board
    :param positions: dictionary
    :return: dictionary
    """
    lines = dict()
    lines[1] = [positions['g'], positions['h'], positions['i']]
    lines[2] = [positions['d'], positions['e'], positions['f']]
    lines[3] = [positions['a'], positions['b'], positions['c']]
    lines[4] = [positions['a'], positions['e'], positions['i']]
    lines[5] = [positions['a'], positions['d'], positions['g']]
    lines[6] = [positions['b'], positions['e'], positions['h']]
    lines[7] = [positions['c'], positions['f'], positions['i']]
    lines[8] = [positions['c'], positions['e'], positions['g']]
    return lines


def combination_letters(list_1, list_2):
    """
    Find possible combinations between two lists by replacing string
    in first list with integer from second list
    :param list_1: list of string and integers
    :param list_2: list of integers
    :return: list of tuples
    """
    list_1 = list(list_1)
    indices = [i for i, x in enumerate(list_1) if isinstance(x, str)]
    for combo in itertools.combinations(list_2, r=len(indices)):
        for index, char in zip(indices, combo):
            list_1[index] = char
        yield tuple(list_1)


def lines_combinations(num_lines, num_list):
    """
    Return dictionary of lists for all combinations for each line
    :param num_lines: dictionary of lists
    :param num_list: list of integers
    :return: dictionary of lists
    """
    lines_combo = dict()
    for line in num_lines:
        lines_combo[line] = list(combination_letters(num_lines[line], num_list))
    return lines_combo


def lines_payout(combinations):
    """
    Takes in all combinations and return potential payout for each line
    :param combinations: list of tuples
    :return: dictionary of integers
    """
    # Payout for each sum
    payout = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108,
              13: 72, 14: 54, 15: 180, 16: 72, 17: 180, 18: 119,
              19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

    # Sum of each combination in list
    sum_payout = dict()
    for line in combinations:
        sum_payout[line] = [sum(combo) for combo in combinations[line]]

    # Replace the sum with its payout and find the integer average for each line
    for line in sum_payout:
        sum_payout[line] = sum([payout[value] for value in sum_payout[line]])//len(sum_payout[line])

    return sum_payout


def recommendation(user_payout):
    """
    Recommend the highest payout line(s) to user
    :param user_payout: dictionary
    :return: string
    """
    print('---------------')
    highest = max(user_payout.values())
    recommend = [key for key, value in user_payout.items() if value == highest]
    string = ''
    for key in recommend:
        string += Color.BOLD + '> Line {} has the highest payout of {}!\n'.format(key, user_payout[key]) + Color.END
    return string


def main():
    print(Color.BOLD + 'Welcome to FFXIV Mini Cactpot Solver!\n' + Color.END)
    while True:
        start = input('Start (yes/no): ').lower()
        if start == 'yes':
            # Dictionary for each position of board
            board = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i'}
            print(current_board(board))

            # Populate board with user numbers
            filled_num = user_numbers()
            fill_numbers(filled_num, board)

            # Calculate possible combinations of sums on board
            avail_num = [x for x in range(1, 10) if x not in board.values()]
            possible_combo = lines_combinations(board_lines(board), avail_num)
            expected_value = lines_payout(possible_combo)

            # Recommend the highest payout line(s) for user
            print(recommendation(expected_value))

        elif start == 'no':
            print('Thank you for using the program.')
            break

        else:
            print('Please enter yes or no.')
            continue


if __name__ == "__main__":
    main()