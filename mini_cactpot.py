"""
This program is written for the Mini Cactpot minigame in Final Fantasy 14 MMORPG.

The game consists of a 3x3 scratch off ticket with 1 number given to the user. User can pick 3 additional numbers to
fill in the matrix. For example:

4   5   6   7  8
3 | 1 | 3 | x
2 | x | 9 | x
1 | x | x | 7

Then user has to pick a 3-number lines. There are 3 rows, 3 columns, and 2 diagonals, making a total of 8 lines.
Indcated by number 1-8 on the outside of the board. The payout for the game depends on the sum of numbers for that line.

This program calculates the average of all possible payout for each of those lines.
"""


class Color:
    # Text decoration
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Game:
    """
    This class works with graphical representation of the ticket, getting user inputs, and updating ticket.
    """
    def __init__(self, ticket):
        self.ticket = ticket

    def new_ticket(self):
        """
        Return a display of the ticket.

        Assumes that ticket is a dictionary with 9 letter keys from a-i for each position.
        """
        display = [
            '--------------',
            Color.BOLD + '4  5  6  7  8' + Color.END,
            Color.BOLD + '3' + Color.END + '  {}  {}  {}'.format(self.ticket['a'], self.ticket['b'], self.ticket['c']),
            Color.BOLD + '2' + Color.END + '  {}  {}  {}'.format(self.ticket['d'], self.ticket['e'], self.ticket['f']),
            Color.BOLD + '1' + Color.END + '  {}  {}  {}'.format(self.ticket['g'], self.ticket['h'], self.ticket['i']),
            '--------------'
        ]
        return '\n'.join(display)

    @classmethod
    def user_numbers(cls):
        """
        Return dictionary of 4 key-value pairs of letter positions and user's numbers.
        """
        user_inputs = {}
        for i in range(1, 5):
            c, n = input('Number {}: '.format(i)).split()
            user_inputs[c] = int(n)
        return user_inputs

    def fill_numbers(self, num):
        """
        Fill in numbers to ticket from dictionary of user's inputs
        """
        for k, v in num.items():
            for c in self.ticket:
                if c == k:
                    self.ticket[c] = v
        return self.ticket


class Calculate:
    """
    This class deals with the positions for each 3-number line, calculating possible combinations of numbers, and
    potential payout for each line
    """
    def __init__(self, positions):
        self.positions = positions

    def lines(self):
        """
        Return each line's positions on ticket
        """
        ticket_lines = {
            1: [self.positions['g'], self.positions['h'], self.positions['i']],
            2: [self.positions['d'], self.positions['e'], self.positions['f']],
            3: [self.positions['a'], self.positions['b'], self.positions['c']],
            4: [self.positions['a'], self.positions['e'], self.positions['i']],
            5: [self.positions['a'], self.positions['d'], self.positions['g']],
            6: [self.positions['b'], self.positions['e'], self.positions['h']],
            7: [self.positions['c'], self.positions['f'], self.positions['i']],
            8: [self.positions['c'], self.positions['e'], self.positions['g']]
        }
        return ticket_lines

    @classmethod
    def combinations(cls, iterable, r):
        """
        Return combinations of elements for iterable of length r with no repeating elements
        """
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)

    def lists_combinations(self, l1, l2):
        """
        Find possible combinations of lines by replacing string with integer.
        """
        indices = [i for i, j in enumerate(l1) if isinstance(j, str)]

        # Find all indices of letters in list 1 and replace them with outputs from list 2's combinations
        for combo in self.combinations(l2, len(indices)):
            for index, char in zip(indices, combo):
                list_1[index] = char
            yield tuple(l2)

    def lines_combinations(self, num_lines, num_list):
        """
        Return dictionary of lists for all combinations for each line
        """
        lines_combo = {}
        for line in num_lines:
            lines_combo[line] = list(self.lists_combinations(num_lines[line], num_list))
        return lines_combo

    @classmethod
    def lines_payout(cls, comb):
        """
        Return average of potential payout for each line
        """
        payout = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108,
                  13: 72, 14: 54, 15: 180, 16: 72, 17: 180, 18: 119,
                  19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

        # Sum of each combination in list
        sum_payout = dict()
        for line in comb:
            sum_payout[line] = [sum(combo) for combo in comb[line]]

        # Replace the sum with its payout and find the average for each line
        for line in sum_payout:
            sum_payout[line] = sum([payout[value] for value in sum_payout[line]]) // len(sum_payout[line])
        return sum_payout

    @classmethod
    def recommendation(cls, user_payout):
        """
        Recommend the highest payout line(s) to user
        """
        print('---------------')
        highest = max(user_payout.values())
        recommend = [key for key, value in user_payout.items() if value == highest]
        string = ''
        for key in recommend:
            string += Color.BOLD + '> Line {} has the highest payout of {}!\n'.format(key, user_payout[key]) + Color.END
        return string


def cactpot():
    print(Color.BOLD + 'Welcome to FFXIV Mini Cactpot Solver!\n' + Color.END)
    while True:
        start = input('Start (yes/no): ').lower()
        if start == 'yes':

            # Ticket dictionary
            ticket = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i'}
            new_game = Game(ticket)
            print(new_game.new_ticket())

            print('Enter the 4 numbers you picked by its letter, then number.')
            print(Color.UNDERLINE + 'For Example' + Color.END + ": enter 'a 1' if position a on ticket is 1.\n")

            # Populate board with user numbers
            numbers = new_game.user_numbers()
            new_game.fill_numbers(numbers)

            # List of numbers not on ticket
            availables = [x for x in range(1, 10) if x not in ticket.values()]
            calc = Calculate(ticket)

            # Calculate combinations and potential payout
            ticket_lines = calc.lines()
            possibilities = calc.lines_combinations(ticket_lines, availables)
            expected_value = calc.lines_payout(possibilities)

            # Recommend the highest payout line(s) for user
            print(calc.recommendation(expected_value))

        elif start == 'no':
            print('Thank you for using the program.')
            break

        else:
            print('Please enter yes or no.')
            continue


if __name__ == "__main__":
    cactpot()
