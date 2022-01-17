"""CSC108: Fall 2021 -- Assignment 2: Simulating Canadian Elections

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Tom Fairgrieve, Sadia Sharmin, and 
Jacqueline Smith.


### Reminder about ballot types

An approval ballot: a voter indicates approval or disapproval for each
candidate.
  Example: ['YES', 'YES', 'NO', 'YES']

A range ballot: a voter assigns each candidate a number of points between
1 and 5 inclusive, where more points means more preferred.
  Example: [5, 4, 1, 4]

A rank ballot: a voter puts the candidates in ranked order of preference
from 1st to 4th choice.
  Example: ['LIBERAL', 'GREEN', 'CPC', 'NDP']

A single-candidate ballot: a voter selects exactly one candidate from a list.
  In this program, we consider the highest ranked candidate as the 
  single-candidate vote.
  Example: 'LIBERAL'
"""
from typing import List

###############################################################################
# Constants
###############################################################################

# A list of the names of each party in the order they appear in a 4-element list
PARTY_ORDER = ['CPC', 'GREEN', 'LIBERAL', 'NDP']

# Indexes for columns in the vote data
COLUMN_RIDING = 0
COLUMN_VOTER = 1
COLUMN_RANK = 2
COLUMN_RANGE = 3
COLUMN_APPROVAL = 4

# Strings used in the approval ballots
APPROVAL_TRUE = "YES"
APPROVAL_FALSE = "NO"

###############################################################################
# VoteData Type
###############################################################################

"""
In the docstrings below, you will see a new type, VoteData. This represents the 
VoteData type introduced in the handout. You can read 'VoteData' in function
type contracts as follows:
VoteData = List[int, int, List[str], List[int], List[bool]]
"""

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['CPC', 'LIBERAL', 'NDP', 'GREEN'], [5, 0, 3, 2], 
                  [True, False, True, True]]]

###############################################################################
# Task 0: Creating testing data
###############################################################################

SAMPLE_DATA_2 = [] 


###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to their
    appropriate type.

    The indexes of the string values that are converted, and their
    corresponding type, are:
        - COLUMN_RIDING is an int
        - COLUMN_VOTER is an int
        - COLUMN_RANK is a list of strings
        - COLUMN_RANGE is a list of integers
        - COLUMN_APPROVAL is a list of booleans

    >>> row = ['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']
    >>> clean_data([row])
    >>> row == SAMPLE_DATA_1[0]
    True
    >>> row = ['117', '12', 'Liberal;CPC;NDP;Green', '4;0;5;0', 'YES;NO;YES;NO']
    >>> clean_data([row])
    >>> row == SAMPLE_DATA_2[0]
    True
    """


###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> List:
    """Return a list containing only the elements at index column for each
    item in data.

    Precondition: each inner list has an item at position column. 

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 0)
    [1, 4]
    >>> extract_column(SAMPLE_DATA_1, COLUMN_APPROVAL)[0]
    [False, True, False, False]
    """


def extract_single_ballots(vote_data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from each
    rank ballot in vote_data. The highest ranked candidate is considered
    the single-candidate ballot for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'CPC']
    """


def get_votes_in_riding(vote_data: List['VoteData'], riding: int
                        ) -> List['VoteData']:
    """Return a list containing only the vote_data for this riding.

    >>> get_votes_in_riding(SAMPLE_DATA_1, 0)
    [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3], \
[False, True, False, False]]]
    """


###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(votes: List[str]) -> List[int]:
    """Based on the single-candidate ballots in votes, return a list with the
    totals for each party in the order specified in PARTY_ORDER.

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'])
    [1, 3, 0, 1]
    """


###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

def voting_approval(av_ballots: List[List[bool]]) -> List[int]:
    """Return the total number of approvals received for each party in 
    av_ballots. The list elements are ordered by PARTY_ORDER.

    >>> voting_approval(extract_column(SAMPLE_DATA_1, COLUMN_APPROVAL))
    [1, 2, 2, 3]
    """


###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]]) -> List[int]:
    """Return a list of the total scores received by each party on 
    range_ballots. The list elements are ordered by PARTY_ORDER.

    >>> voting_range(extract_column(SAMPLE_DATA_1, COLUMN_RANGE))
    [9, 10, 10, 9]
    """


###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]]) -> List[int]:
    """Return the Borda count for each party applied to rank_ballots. 
    The list elements are ordered by PARTY_ORDER.

    >>> voting_borda(extract_column(SAMPLE_DATA_1, COLUMN_RANK))
    [4, 5, 7, 8]
    """
    

###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Mutate rank_ballots to remove the party_to_remove from each of the given 
    rank ballots.

    Pre-condition: party_to_remove is in all of the ballots in rank_ballots.

    >>> party = [['LIBERAL', 'GREEN', 'CPC', 'NDP'], \
                ['CPC', 'NDP', 'LIBERAL', 'GREEN'], \
                ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(party, 'NDP')
    >>> party
    [['LIBERAL', 'GREEN', 'CPC'], ['CPC', 'LIBERAL', 'GREEN'], \
['CPC', 'GREEN', 'LIBERAL']]
    """


def get_lowest_not_removed(votes: List[int], removed_parties: List[str]) -> str:
    """Return the name of the party with the lowest number of votes that is
    not in removed_parties. votes is ordered by PARTY_ORDER.

    Pre-condition: len(removed_parties) < len(PARTY_ORDER)
                   There is at least one party that has not been removed yet.
                   Elements of votes >= 0.
                   
    >>> get_lowest_not_removed([16, 100, 4, 200], [])
    'LIBERAL'
    >>> get_lowest_not_removed([16, 100, 4, 200], ['LIBERAL', 'CPC'])
    'GREEN'
    >>> get_lowest_not_removed([10, 10, 10, 10], ['CPC'])
    'GREEN'
    """


def voting_irv(rank_ballots: List[List[str]]) -> str:
    """Given a list of rank ballots, return the winning party when using IRV.

    rank_ballots should be mutated as needed, removing parties that are
    eliminated in the process.

    >>> voting_irv(extract_column(SAMPLE_DATA_1, COLUMN_RANK))
    'NDP'
    """


###############################################################################
# Task 4: Determine winner
###############################################################################

def points_to_winner(points_per_party: List[int]) -> str:
    """Return the party with the highest number of points in points_per_party.
    points_per_party is in the order specified in PARTY_ORDER.

    Precondition: len(points_per_party == len(PARTY_ORDER)

    >>> points_to_winner([1, 3, 0, 1])
    'GREEN'
    """
