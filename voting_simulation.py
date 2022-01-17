"""CSC108: Fall 2021 -- Assignment 2: Simulating Canadian Elections

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Tom Fairgrieve, Sadia Sharmin, and 
Jacqueline Smith.
"""

from typing import List, Callable
import voting_systems as vs

CSV_FILENAME = 'sample_votes.csv'

SYSTEMS = {"Plurality": (vs.voting_plurality, None),
           "Approval": (vs.voting_approval, vs.COLUMN_APPROVAL),
           "Range": (vs.voting_range, vs.COLUMN_RANGE),
           "Borda": (vs.voting_borda, vs.COLUMN_RANK),
           "IRV": (vs.voting_irv, vs.COLUMN_RANK)}


def read_data(filename: str) -> List[list]:
    """Return the data found in the file filename as a list of lists.
    Each inner list corresponds to a row in the file.

    Docstring examples not given since the results depend on filename.

    Precondition: The data in filename is in a valid format
    """
    f = open(filename)
    data = []
    f.readline()  # remove header
    for line in f:
        data.append(line.strip().split(','))
    f.close()
    return data


def print_list_items(lst: list, delimiter: str) -> None:
    """Print the items of lst separated by delimiter.
    """
    print('  ', end='')
    for item in lst[:-1]:
        print(item, end=delimiter)
    if len(lst) >= 1:
        print(lst[-1])


def prompt_from_list(prompt: str, lst: list) -> str:
    """Prompt the user to enter a value using prompt, present the user with
    the options from lst, and return the value entered.
    """
    print(prompt)
    print_list_items(lst, ', ')

    # Continuously prompt the user to enter a value until they
    # enter a value that appears in lst.
    answer = input()
    while answer not in lst:
        print(answer, 'Invalid choice. You must select from these options: ')
        print_list_items(lst, ', ')
        answer = input()
    return answer


def prompt_for_riding(prompt: str, maximum: int) -> str:
    """Prompt the user to enter all or a value between 0 and maximum - 1
    inclusive, using prompt, and return the value entered.
    """

    # Continuously prompt the user to enter a value until they
    # enter a value between 0 and maximum - 1, or 'all'.
    answer = input(prompt.format(maximum))
    while not (answer.isnumeric() and 0 <= int(answer) <= maximum) \
            and answer != 'all':
        print('Invalid choice. Enter a riding between 0 and '
              '{0}, or all.'.format(maximum))
        answer = input(prompt)

    return answer


def print_all_riding_results(seats: List[int]) -> None:
    """Given a four-element list representing the seats assigned to the parties
    in the order of PARTY_ORDER, print a formatted message.
    """
    print("\nResults for All Ridings")
    print("=======================")

    for index in range(len(vs.PARTY_ORDER)):
        party_formatted = (vs.PARTY_ORDER[index] + ':').ljust(10)
        print("{0}       {1}".format(party_formatted, seats[index]))


def print_single_riding_results(riding: int, winning_party: str,
                                distribution: List[int]) -> None:
    """Print a formatted message showing that winning_party has won for
    this riding and, if applicable, also print the distribution of the votes
    in the order of PARTY_ORDER.
    """
    print("\nResults for Riding {0}".format(riding))
    print("=====================")
    print("The seat is won by the {0} candidate.".format(winning_party))

    if isinstance(distribution, list):
        print("The distribution of the results is as follows: ")
        for index in range(len(vs.PARTY_ORDER)):
            party_formatted = (vs.PARTY_ORDER[index] + ':').ljust(10)
            print("{0}       {1}".format(party_formatted, distribution[index]))


def single_riding_election(riding: int, system_func: Callable,
                           vote_data: 'VoteData', system_column: int) -> None:
    """Simulate an election for the given riding number and the voting system
    implemented in system_func. The voting system is at column system_column
    in vote_data.
    """
    print(type(system_func), type(vote_data), type(system_column))

    riding_votes = vs.get_votes_in_riding(vote_data, riding)
    if not system_column:
        ballots = vs.extract_single_ballots(riding_votes)
    else:
        ballots = vs.extract_column(riding_votes, system_column)

    full_results = system_func(ballots)
    if isinstance(full_results, list):
        winner = vs.points_to_winner(full_results)
    else:
        winner = full_results

    print_single_riding_results(riding, winner, full_results)


def all_riding_election(num_ridings: int, system_func: Callable,
                        vote_data: 'VoteData', system_column: int) -> None:
    """Simulate an election for all num_ridings ridings and the voting system
    implemented in system_func. The voting system is at column system_column
    in vote_data.
    """
    seats = [0, 0, 0, 0]
    for riding in range(num_ridings):
        riding_votes = vs.get_votes_in_riding(vote_data, riding)
        if not system_column:
            ballots = vs.extract_single_ballots(riding_votes)
        else:
            ballots = vs.extract_column(riding_votes, system_column)

        full_results = system_func(ballots)
        if isinstance(full_results, list):
            winner = vs.points_to_winner(full_results)
        else:
            winner = full_results
        seats[vs.PARTY_ORDER.index(winner)] += 1

    print_all_riding_results(seats)


def simulate_elections() -> None:
    """Run the voting simulations based on user input.
    """

    system_name = prompt_from_list(
        "Select a voting system or Q to quit:", list(SYSTEMS.keys()) + ['Q'])

    while system_name != 'Q':
        
        data = read_data(CSV_FILENAME)
        vs.clean_data(data)      
        
        print('Running for {0}.'.format(system_name))

        num_ridings = len(set(vs.extract_column(data, vs.COLUMN_RIDING)))

        prompt = ("Which riding would you like to see results for? "
                  "(Enter a number between 0 and {0}, or all.): ")

        riding = prompt_for_riding(prompt, num_ridings - 1)
        system_func = SYSTEMS[system_name][0]
        system_col = SYSTEMS[system_name][1]

        if riding != 'all':
            single_riding_election(int(riding), system_func, data, system_col)

        else:
            all_riding_election(num_ridings, system_func, data, system_col)

        system_name = prompt_from_list("Select a voting system or Q to quit:",
                                       list(SYSTEMS.keys()) + ['Q'])
    print('End of voting simulation')


#########################################


if __name__ == '__main__':
    simulate_elections()
