#!/usr/bin/env python3

"""
This program calculates the best payout for the Mini Cactpot minigame in Final Fantasy 14 MMORPG.

The game consists of a 3x3 scratch off ticket with 1 number given to the user.
User can pick 3 additional numbers to fill in the matrix. For example:

4   5   6   7  8
3 | 1 | 3 | x
2 | x | 9 | x
1 | x | x | 7

Then user has to pick a 3-number lines. There are 3 rows, 3 columns, and 2 diagonals, making a total of 8 lines.
Indicated by number 1-8 on the board. The payout for the game depends on the sum of numbers for that line.
"""


class Color:
    # Text decoration
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Game:
    """
    Graphical representation of the ticket, getting user inputs, and updating ticket.
    """
    def __init__(self, ticket):
        self.ticket = ticket

    def current_ticket(self):
        """
        Return a display of the ticket as joined strings.

        Assumes ticket is a dictionary with 9 key-value pairs from a-i for each position.
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

    @staticmethod
    def user_numbers():
        """
        Ask for user's inputs and return inputs as dictionary of position-number
        """
        print('Enter the 4 numbers you picked by its letter, then number.')
        print(Color.UNDERLINE + 'For Example' + Color.END + ": enter 'a 1' if position a value is 1.\n")
        user_inputs = {}
        while True:
            try:
                for counter in range(1, 5):
                    letter, number = input('Number {}: '.format(counter)).split()
                    user_inputs[letter] = int(number)
            except ValueError:
                print('Please enter your numbers in the indicated format')
            finally:
                if len(user_inputs) == 4:
                    break
        return user_inputs

    def fill_ticket(self):
        """
        Replaces values in ticket based on user's numbers
        """
        nums = self.user_numbers()
        for key, value in nums.items():
            if key in self.ticket:
                self.ticket[key] = value
        return self.ticket


class Calculate:
    """
    Calculates possible combinations of numbers, and best payout for ticket
    """
    def __init__(self, ticket):
        self.ticket = ticket
        self.nums_left = [x for x in range(1, 10) if x not in ticket.values()]

    def lines(self):
        """
        Return dictionary of each line and its three positions on ticket
        """
        lines = {
            1: [self.ticket['g'], self.ticket['h'], self.ticket['i']],
            2: [self.ticket['d'], self.ticket['e'], self.ticket['f']],
            3: [self.ticket['a'], self.ticket['b'], self.ticket['c']],
            4: [self.ticket['a'], self.ticket['e'], self.ticket['i']],
            5: [self.ticket['a'], self.ticket['d'], self.ticket['g']],
            6: [self.ticket['b'], self.ticket['e'], self.ticket['h']],
            7: [self.ticket['c'], self.ticket['f'], self.ticket['i']],
            8: [self.ticket['c'], self.ticket['e'], self.ticket['g']]
        }
        return lines

    @staticmethod
    def combinations(iterable, r):
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
            for j in range(i + 1, r):
                indices[j] = indices[j - 1] + 1
            yield tuple(pool[i] for i in indices)

    def lists_combinations(self, l1):
        """
        Find possible combinations of numbers by replacing string from l1 with numbers still available on ticket
        """
        indices = [i for i, x in enumerate(l1) if isinstance(x, str)]
        combos = self.combinations(self.nums_left, len(indices))
        for combo in combos:
            for index, char in zip(indices, combo):
                l1[index] = char
            yield tuple(l1)

    def lines_combinations(self):
        """
        Return dictionary of lists for all combinations for each line
        """
        lines_combo = {}
        num_lines = self.lines()
        for line in num_lines:
            lines_combo[line] = list(self.lists_combinations(num_lines[line]))
        return lines_combo

    @classmethod
    def lines_payout(cls, combinations):
        """
        Return average of potential payout for each line
        """
        payout = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108,
                  13: 72, 14: 54, 15: 180, 16: 72, 17: 180, 18: 119,
                  19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

        # Sum of each combination in list
        sum_payout = {}
        for line in combinations:
            sum_payout[line] = [sum(combo) for combo in combinations[line]]

        # Replace the sum with its payout and find the average for each line
        for line in sum_payout:
            sum_payout[line] = sum([payout[value] for value in sum_payout[line]]) // len(sum_payout[line])
        return sum_payout

    @classmethod
    def recommendation(cls, user_payout):
        """
        Recommend the highest payout line(s) to user
        """
        highest = max(user_payout.values())
        recommend = [key for key, value in user_payout.items() if value == highest]
        string = ''
        for key in recommend:
            string += Color.BOLD + '> Line {} has the highest payout of {}!\n'.format(key, user_payout[key]) + Color.END
        return string


def main():
    print(Color.BOLD + 'Welcome to FFXIV Mini Cactpot Solver!\n' + Color.END)
    while True:
        start = input('Start (y/n): ').lower()
        if start == 'y':
            ticket = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i'}
            # Ask user for inputs and populate ticket
            game = Game(ticket)
            print(game.current_ticket())
            game.fill_ticket()
            # Calculate combinations and potential payout
            calc = Calculate(ticket)
            possibilities = calc.lines_combinations()
            expected_value = calc.lines_payout(possibilities)
            # Recommend the highest payout line(s) for user
            print(game.current_ticket())
            print(calc.recommendation(expected_value))
        elif start == 'n':
            print('Good bye')
            break
        else:
            print('Please enter yes or no.')
            continue


if __name__ == "__main__":
    main()
