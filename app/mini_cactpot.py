
"""
This program calculate the best payouts for the mini cactpot web app

The ticket will be represented in this format:

4   5   6   7  8
3 | a | b | c
2 | d | e | f
1 | g | h | i

Each number the user picked will correspond to letters a to i.
The numbers 1-8 indicate the 3-number lines used to calculate payout.
"""


class Calculate:
    """
    Calculate possible combinations of numbers, and best payouts
    """

    def __init__(self, ticket):
        self.ticket = ticket

        # List of numbers not selected by user
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

        Note: built in function from itertools, using inside class to avoid import
        https://docs.python.org/2/library/itertools.html#itertools.combinations
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

    def lists_combinations(self, ticket_lines):
        """
        Find possible combinations of numbers by replacing string from ticket_lines with numbers still available on ticket
        """
        indices = [i for i, x in enumerate(ticket_lines) if isinstance(x, str)]
        combos = self.combinations(self.nums_left, len(indices))
        for combo in combos:
            for index, char in zip(indices, combo):
                ticket_lines[index] = char
            yield tuple(ticket_lines)

    def lines_combinations(self):
        """
        Return dictionary of lists for all combinations of each line
        """
        lines_combo = {}
        num_lines = self.lines()
        for line in num_lines:
            lines_combo[line] = list(self.lists_combinations(num_lines[line]))
        return lines_combo

    @classmethod
    def lines_payout(cls, possibles):
        """
        Return average of potential payout for each line
        """

        # Payout for each sum
        payout = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108,
                  13: 72, 14: 54, 15: 180, 16: 72, 17: 180, 18: 119,
                  19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

        # Sum of each combination in list
        sum_payout = {}
        for line in possibles:
            sum_payout[line] = [sum(combo) for combo in possibles[line]]

        # Replace the sum with its payout and find the average for each line
        for line in sum_payout:
            sum_payout[line] = sum([payout[value] for value in sum_payout[line]]) // len(sum_payout[line])

        return sum_payout

    @classmethod
    def recommendation(cls, user_payout):
        """
        Recommend the highest payout line(s) to user
        """

        # Dictionary of table lines and ids
        lines_id = {
            1: [7, 8, 9],
            2: [4, 5, 6],
            3: [1, 2, 3],
            4: [1, 5, 9],
            5: [1, 4, 7],
            6: [2, 5, 8],
            7: [3, 6, 9],
            8: [3, 5, 7]
        }

        # Get key of highest payout
        highest = max(user_payout.values())
        recommend = [key for key, value in user_payout.items() if value == highest]

        # First element is cell ids of highest payout
        best = [
            {i: lines_id[i] for i in recommend}
        ]

        for key in recommend:
            best.append(f"Line {key} has the highest average payout of {user_payout[key]}")

        return best


def fill_ticket(numbers_list):
    """
    Create a dictionary of letter position and numbers
    """

    # letter position on ticket
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    # assign each number to letter if not 0
    ticket = {letter: (number if number else letter) for letter, number in zip(letters, numbers_list)}

    return ticket


def calculate(user_inputs):
    """
    Return a dictionary of all
    """

    # Fill empty ticket with user inputs
    ticket = fill_ticket(user_inputs)

    # Calculate combinations and potential payout
    calc = Calculate(ticket)
    possibilities = calc.lines_combinations()
    expected_value = calc.lines_payout(possibilities)

    # Recommend the highest payout line(s) to user
    recommendation = calc.recommendation(expected_value)

    # Dictionary of results
    results = {
        "payouts": expected_value,
        "suggestion": recommendation
    }

    return results