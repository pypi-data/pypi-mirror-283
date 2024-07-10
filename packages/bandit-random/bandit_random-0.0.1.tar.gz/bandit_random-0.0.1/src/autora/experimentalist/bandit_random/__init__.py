"""
Experimentalist that returns
probability sequences: Sequences of vectors with elements between 0 and 1
or
reward sequences: Sequences of vectors with binary elements
"""

import numpy as np

from typing import Union, List, Optional
from collections.abc import Iterable


def pool_proba(
        num_probabilities: int,
        sequence_length: int,
        initial_probabilities: Optional[Iterable[Union[float, Iterable]]] = None,
        drift_rates: Optional[Iterable[Union[float, Iterable]]] = None,
        num_samples: int = 1,
        random_state: Optional[int] = None,
) -> List[List[List[float]]]:
    """
    Returns a list of probability sequences.
    A probability sequence is a sequence of vectors of dimension `num_probabilities`. Each entry
    of this vector is a number between 0 and 1.
    We can set a fixed initial value for the first vector of each sequence and a constant drif rate.
    We can also set a range to randomly sample these values.


    Args:
        num_probabilities: The number of probilities/ dimention of each element of the sequence
        sequence_length: The length of the sequence
        initial_probabilities: A list of initial values for each element of the probalities. Each
        entry can be a range.
        drift_rates: A list of constant drift rate for each element of the probabilites. Each
        entry can be a range. The drift rate is defined as change per step
        num_samples: number of experimental conditions to select
        random_state: the seed value for the random number generator
    Returns:
        Sampled pool of experimental conditions

    Examples:
        We create a reward probabilty sequence for five two arm bandit tasks. The reward
        probabilities for each arm should be .5 and constant.
        >>> pool_proba(num_probabilities=2, sequence_length=3, num_samples=1)
        [[[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]]

        If we want more arms:
        >>> pool_proba(num_probabilities=4, sequence_length=3, num_samples=1)
        [[[0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5]]]

        longer sequence:
        >>> pool_proba(num_probabilities=2, sequence_length=5, num_samples=1)
        [[[0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]]

        more sequences:
        >>> pool_proba(num_probabilities=2, sequence_length=3, num_samples=2)
        [[[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]], [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]]

        We  can set fixed initial values:
        >>> pool_proba(num_probabilities=2, sequence_length=3,
        ...     initial_probabilities=[0.,.4])
        [[[0.0, 0.4], [0.0, 0.4], [0.0, 0.4]]]

        And drift rates:
        >>> pool_proba(num_probabilities=2, sequence_length=3,
        ...     initial_probabilities=[0.,.4],
        ...     drift_rates=[.2, -.2])
        [[[0.0, 0.4], [0.2, 0.2], [0.4, 0.0]]]
        
        We can also sample the initial values by passing a range:
        >>> pool_proba(num_probabilities=2, sequence_length=3,
        ...     initial_probabilities=[[0, .2],[.8, 1.]],
        ...     drift_rates=[[0, .2], [-.2, 0.]],
        ...     random_state=42)
        [[[0.15479120971119267, 0.9717195839822765], \
[0.24256689766160314, 0.9111931897941493], \
[0.3303425856120136, 0.8506667956060221]]]
    """
    rng = np.random.default_rng(random_state)
    if initial_probabilities:
        assert len(initial_probabilities) == num_probabilities
    else:
        initial_probabilities = [.5 for _ in range(num_probabilities)]
    if drift_rates:
        assert len(drift_rates) == num_probabilities
    else:
        drift_rates = [0 for _ in range(num_probabilities)]
    res = []
    for _ in range(num_samples):
        seq = []
        for idx, el in enumerate(initial_probabilities):
            prob = []
            if _is_iterable(el):
                start = rng.uniform(el[0], el[1])
            else:
                start = el
            if _is_iterable(drift_rates[idx]):
                drift = rng.uniform(drift_rates[idx][0], drift_rates[idx][1])
            else:
                drift = drift_rates[idx]
            for _ in range(sequence_length):
                prob.append(start)
                start += drift
                start = max(0., min(start, 1.))
            seq.append(prob)
        res.append(seq)
    for idx in range(len(res)):
        res[idx] = _transpose_matrix(res[idx])
    return res


def pool_from_proba(
        probability_sequence: Iterable,
        random_state: Optional[int] = None,
) -> List[List[List[float]]]:
    """
    From a given probability sequence sample rewards (0 or 1)

    Example:
        >>> proba_sequence = pool_proba(num_probabilities=2, sequence_length=3,
        ...     initial_probabilities=[0.,1.],
        ...     drift_rates=[.15, -.15])
        >>> proba_sequence
        [[[0.0, 1.0], [0.15, 0.85], [0.3, 0.7]]]
        >>> pool_from_proba(proba_sequence, 42)
        [[[0, 1], [1, 1], [0, 1]]]
    """
    rng = np.random.default_rng(random_state)
    return _sample_from_probabilities(probability_sequence, rng)


def pool(
        num_rewards: int,
        sequence_length: int,
        initial_probabilities: Optional[Iterable[Union[float, Iterable]]] = None,
        drift_rates: Optional[Iterable[Union[float, Iterable]]] = None,
        num_samples: int = 1,
        random_state: Optional[int] = None,
) -> List[List[List[float]]]:
    """
    Returns a list of rewards.
    A reward sequence is a sequence of vectors of dimension `num_probabilities`. Each entry
    of this vector is a number between 0 and 1.
    We can set a fixed initial value for the reward probability of the first vector of each sequence
    and a constant drif rate.
    We can also set a range to randomly sample these values.


    Args:
        num_rewards: The number of rewards/ dimention of each element of the sequence
        sequence_length: The length of the sequence
        initial_probabilities: A list of initial reward-probabilities. Each
        entry can be a range.
        drift_rates: A list of constant drift rate for each element of the probabilites. Each
        entry can be a range. The drift rate is defined as change per step
        num_samples: number of experimental conditions to select
        random_state: the seed value for the random number generator
    Returns:
        Sampled pool of experimental conditions

    Examples:
        We create a reward sequence for five two arm bandit tasks. The reward
        probabilities for each arm should be .5 and constant.
        >>> pool(num_rewards=2, sequence_length=3, num_samples=1, random_state=42)
        [[[1, 0], [1, 1], [0, 1]]]

        If we want more arms:
        >>> pool(num_rewards=4, sequence_length=3, num_samples=1, random_state=42)
        [[[1, 0, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1]]]

        longer sequence:
        >>> pool(num_rewards=2, sequence_length=5, num_samples=1, random_state=42)
        [[[1, 0], [1, 1], [0, 1], [1, 1], [0, 0]]]

        more sequences:
        >>> pool(num_rewards=2, sequence_length=3, num_samples=2, random_state=42)
        [[[1, 0], [1, 1], [0, 1]], [[1, 1], [0, 0], [0, 1]]]

        We  can set fixed initial values:
        >>> pool(num_rewards=2, sequence_length=3,
        ...     initial_probabilities=[0.,.4],
        ...     random_state=42)
        [[[0, 0], [0, 1], [0, 1]]]

        And drift rates:
        >>> pool(num_rewards=2, sequence_length=3,
        ...     initial_probabilities=[0.,.4],
        ...     drift_rates=[.2, -.2],
        ...     random_state=42)
        [[[0, 0], [1, 0], [0, 0]]]

        We can also sample the initial values by passing a range:
        >>> pool(num_rewards=2, sequence_length=3,
        ...     initial_probabilities=[[0, .2],[.8, 1.]],
        ...     drift_rates=[[0., .2], [-.2, 0.]],
        ...     random_state=42)
        [[[0, 1], [1, 1], [0, 1]]]
    """
    _sequence = pool_proba(num_rewards,
                           sequence_length,
                           initial_probabilities,
                           drift_rates,
                           num_samples,
                           random_state)
    return pool_from_proba(_sequence, random_state)


bandit_random_pool_proba = pool_proba
bandit_random_pool_from_proba = pool_from_proba
bandit_random_pool = pool


# Helper functions

def _sample_from_probabilities(prob_list, rng):
    """
    Helper function to sample values from a probability sequence
    """

    def sample_element(prob):
        return int(rng.choice([0, 1], p=[1 - prob, prob]))

    def recursive_sample(nested_list):
        if isinstance(nested_list, list):
            return [recursive_sample(sublist) for sublist in nested_list]
        else:
            return sample_element(nested_list)

    return recursive_sample(prob_list)


def _is_iterable(obj):
    """
    Helper function that returns true if an object is iterable
    """
    return isinstance(obj, Iterable)


def _transpose_matrix(matrix):
    """
    Helper function to transpose a list of lists.
    """
    return [list(row) for row in zip(*matrix)]
