"""Randomly pairs people using round-robin scheduling."""
from collections import deque
import random
from typing import List, Optional, Tuple

from fire import Fire


def create_random_pairings(people: List[str],
                           num_pairings: Optional[int] = None,
                           seed: Optional[int] = None) -> List[List[Tuple[str, str]]]:
    """
    Randomly pairs people using round-robin scheduling.

    :param people: A list of people to pair (including a dummy person if needed to have an even number).
    :param num_pairings: The number of pairings to create. Defaults to a full pairing (everyone
                         paired with everyone else exactly once).
    :param seed: Random seed to control the pairings.
    :return: A list of pairings where each pairing is a list of tuples of paired people.
    """
    assert len(people) >= 2
    assert len(people) % 2 == 0

    num_unique_pairs = len(people) - 1
    pairings: List[List[Tuple[str, str]]] = []

    if num_pairings is None:
        num_pairings = num_unique_pairs

    if seed is not None:
        random.seed(seed)

    for i in range(num_pairings):
        if i % num_unique_pairs == 0:
            random.shuffle(people)
            stationary_person = people[0]
            shifting_people = deque(people[1:])

        shifting_people.rotate(1)
        shifted_people = list(shifting_people)
        row_1 = [stationary_person] + shifted_people[:num_unique_pairs // 2]
        row_2 = list(reversed(shifted_people[num_unique_pairs // 2:]))

        assert len(row_1) == len(row_2)

        pairing = [(person_1, person_2) for person_1, person_2 in zip(row_1, row_2)]
        pairings.append(pairing)

    return pairings


def random_pairs(people_path: str,
                 pairings_path: str,
                 num_pairings: Optional[int] = None,
                 seed: Optional[int] = None) -> None:
    """
    Randomly pairs people using round-robin scheduling, including loading/saving to file.

    See https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm

    :param people_path: Path to a text file containing people to pair, one on each line.
    :param num_pairings: The number of pairings to create. Defaults to a full pairing (everyone
                         paired with everyone else exactly once).
    :param seed: Random seed to control the pairings.
    :param pairings_path: Path where the random pairings should be saved.
    """
    # Load people
    with open(people_path) as f:
        people = sorted(line.strip() for line in f if line.strip() != '')

    # If odd number of people, add nobody to have an even number of people
    if len(people) % 2 == 1:
        people.append('Nobody')

    # Create pairings
    pairings = create_random_pairings(
        people=people,
        num_pairings=num_pairings,
        seed=seed
    )

    # Save pairings
    with open(pairings_path, 'w') as f:
        for i, pairing in enumerate(pairings):
            f.write(f'{"-" * 10} Pairing {i + 1} {"-" * 10}\n\n')
            f.write('\n'.join(' + '.join(pair) for pair in pairing))
            f.write('\n\n')


if __name__ == '__main__':
    Fire(random_pairs)
