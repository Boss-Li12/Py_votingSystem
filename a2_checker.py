"""CSC108: Fall 2021 -- Assignment 2: Simulating Canadian Elections

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Tom Fairgrieve, Sadia Sharmin, and 
Jacqueline Smith.
"""

from typing import Any, Dict, List
import unittest
import checker_generic
import voting_systems as vs

PYTA_CONFIG = 'a2_pyta.json'
FILENAME = 'voting_systems.py'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'PARTY_ORDER': ['CPC', 'GREEN', 'LIBERAL', 'NDP'],
    # Indices for columns in the vote data
    'COLUMN_RIDING': 0,
    'COLUMN_VOTER': 1,
    'COLUMN_RANK': 2,
    'COLUMN_RANGE': 3,
    'COLUMN_APPROVAL': 4,
    # Strings used in the approval ballots
    'APPROVAL_TRUE': "YES",
    'APPROVAL_FALSE': "NO"
}


################################################################################
# Sample data to use in checker
################################################################################
def get_sample_vote_data():
    return [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
             [False, True, False, False]],
            [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
             [False, False, True, True]],
            [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
             [False, True, False, True]]]


################################################################################
# Checker test cases
################################################################################
class CheckTest(unittest.TestCase):
    """Sanity checker for assignment functions."""
    
    def test_sample_data_2(self) -> None:
        """Constant SAMPLE_DATA_2."""
        def sample_data_2_length(): return vs.SAMPLE_DATA_2
        self._test_returns_list_of(sample_data_2_length, [], 
                                   [list, list, list])
        def sample_data_2_first_is_VoteData(): return vs.SAMPLE_DATA_2[0]
        self._test_returns_list_of(sample_data_2_first_is_VoteData, [], 
                                   [int, int, list, list, list])
        def sample_data_2_rank_type(): return vs.SAMPLE_DATA_2[1][2]
        self._test_returns_list_of(sample_data_2_rank_type, [], 
                                   [str, str, str, str]) 
        def sample_data_2_range_type(): return vs.SAMPLE_DATA_2[1][3]
        self._test_returns_list_of(sample_data_2_range_type, [], 
                                   [int, int, int, int])
        def sample_data_2_approval_type(): return vs.SAMPLE_DATA_2[2][4]
        self._test_returns_list_of(sample_data_2_approval_type, [], 
                                   [bool, bool, bool, bool])        

    def test_clean_data(self) -> None:
        """Function clean_data."""
        self._check_simple_type(
            vs.clean_data,
            [[['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]],
            type(None))

    def test_extract_column(self) -> None:
        """Function extract_column."""
        sample_data = [[1, 2, 3], [4, 5, 6]]
        self._test_returns_list_of(vs.extract_column,
                                   (sample_data, 0),
                                   [int, int])

        self._check_no_mutation(vs.extract_column, sample_data,
                                [[1, 2, 3], [4, 5, 6]])

    def test_extract_single_ballots(self) -> None:
        """Function extract_single_ballots."""
        sample_data = get_sample_vote_data()
        self._test_returns_list_of(vs.extract_single_ballots,
                                   [sample_data],
                                   [str, str, str])

        self._check_no_mutation(vs.extract_single_ballots, sample_data,
                                get_sample_vote_data())

    def test_get_votes_in_riding(self) -> None:
        """Function get_votes_in_riding."""
        sample_data = get_sample_vote_data()
        self._test_returns_list_of(vs.get_votes_in_riding,
                                   [sample_data, 0],
                                   [list])

        self._check_no_mutation(vs.get_votes_in_riding, sample_data,
                                get_sample_vote_data())

    def test_voting_plurality(self) -> None:
        """Function voting_plurality."""
        sample_data = ['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC']
        self._test_returns_list_of(vs.voting_plurality,
                                   [sample_data],
                                   [int, int, int, int])

        self._check_no_mutation(vs.voting_plurality, sample_data,
                                ['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'])

    def test_voting_approval(self) -> None:
        """Function voting_approval."""

        sample_data = [[True, True, False, False],
                       [False, False, False, True],
                       [False, True, False, False]]
        self._test_returns_list_of(vs.voting_approval,
                                   [sample_data],
                                   [int, int, int, int])

        self._check_no_mutation(vs.voting_approval, sample_data,
                                [[True, True, False, False],
                                 [False, False, False, True],
                                 [False, True, False, False]])

    def test_voting_range(self) -> None:
        """Function voting_range."""
        sample_data = [[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]]
        self._test_returns_list_of(vs.voting_range,
                                   [sample_data],
                                   [int, int, int, int])

        self._check_no_mutation(vs.voting_range, sample_data,
                                [[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]])

    def test_voting_borda(self) -> None:
        """Function voting_borda."""
        sample_data = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                       ['CPC', 'LIBERAL', 'GREEN', 'NDP']]
        self._test_returns_list_of(vs.voting_borda,
                                   [sample_data],
                                   [int, int, int, int])

        self._check_no_mutation(vs.voting_borda, sample_data,
                                [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                                 ['CPC', 'LIBERAL', 'GREEN', 'NDP']])

    def test_remove_party(self) -> None:
        """Function remove_party."""
        sample_data = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                       ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
                       ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
        self._check_simple_type(vs.remove_party,
                                [sample_data, 'NDP'],
                                type(None))
        
    def test_get_lowest_not_removed(self) -> None:
        """Function get_lowest_not_removed."""
        sample_data = [16, 100, 4, 200]
        self._check_simple_type(vs.get_lowest_not_removed,
                                [sample_data, []],
                                str)

        self._check_no_mutation(vs.get_lowest_not_removed, sample_data,
                                [16, 100, 4, 200])

    def test_voting_irv(self) -> None:
        """Function voting_irv."""
        sample_data = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
                       ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
                       ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
        self._check_simple_type(vs.voting_irv,
                                [sample_data],
                                str)

    def test_points_to_winner(self) -> None:
        """Function points_to_winner."""
        sample_data = [1, 3, 0, 1]
        self._check_simple_type(vs.points_to_winner,
                                [sample_data],
                                str)

        self._check_no_mutation(vs.points_to_winner, sample_data,
                                [1, 3, 0, 1])

    ############################################################################
    # Generic checker methods
    ############################################################################
    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, vs)
        print('  check complete')

    def _check_simple_type(self, func: callable, args: list,
                           expected: type) -> None:
        """Check that func called with arguments args returns a value of type
        expected. Display the progress and the result of the check.
        """
        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.type_check_simple(func, args, expected)
        self.assertTrue(result[0], result[1])
        print('  check complete')

    def _check_no_mutation(self, func: callable, actual, expected) -> None:
        """Check that func does not mutate that argument actual so that
        it still matches expected.
        """
        self.assertTrue(expected == actual,
                        '{0} should not mutate its arguments'.format(
                            func.__name__))

    def _check_mutation(self, func: callable, actual, expected) -> None:
        """Check that func mutates the argument actual so that
        it is different from expected.
        """
        self.assertTrue(expected != actual,
                        '{0} should mutate its list argument'.format(
                            func.__name__))

    def _test_returns_list_of(self, func, args, types):
        """Check that func when called with args returns a list of elements
        of typef from types.

        """
        print('\nChecking {}...'.format(func.__name__))

        result = checker_generic.type_check_simple(func, args, list)
        self.assertTrue(result[0], result[1])

        msg = '{} should return a list of length {}'
        self.assertEqual(len(result[1]), len(types),
                         msg.format(func.__name__, len(types)))

        msg = ('Element at index {} in the list returned '
               'should be of type {}. Got {}.')
        for i, typ in enumerate(types):
            self.assertTrue(isinstance(result[1][i], typ),
                            msg.format(i, typ, result[1][i]))

        print('  check complete')

    def _check_constants(self, name2value: Dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            self.assertEqual(expected, actual, msg)


print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
unittest.main(exit=False)
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
