"""Randomly pairs people using round-robin scheduling."""
from collections import deque
import os
import random
from typing import Dict, List, Optional, Tuple

from fire import Fire
import pandas as pd


Person = Dict[str, str]


def create_random_pairings(people: List[Person],
                           num_pairings: Optional[int] = None,
                           seed: Optional[int] = None) -> List[List[Tuple[Person, Person]]]:
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
    pairings: List[List[Tuple[Person, Person]]] = []

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
                 pairings_dir: str,
                 name_column: str = 'Name',
                 email_column: str = 'Email',
                 num_pairings: Optional[int] = None,
                 seed: Optional[int] = None) -> None:
    """
    Randomly pairs people using round-robin scheduling, including loading/saving to file.

    See https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm

    :param people_path: Path to a CSV file containing people (and optionally emails) to pair.
    :param pairings_dir: Path to a directory where the random pairings will be saved.
    :param name_column: Name of the column containing people's names.
    :param email_column: Name of the column containing people's emails.
    :param num_pairings: The number of pairings to create. Defaults to a full pairing (everyone
                         paired with everyone else exactly once).
    :param seed: Random seed to control the pairings.
    """
    # Load people
    people = pd.read_csv(people_path)

    # Remove unneeded columns
    people = people[[name_column, email_column]]

    # Sort people
    people.sort_values(by=name_column, inplace=True)

    # Convert people to list of dictionaries
    people = [{name_column: name, email_column: email} for name, email in people.itertuples(index=False)]

    # If odd number of people, add nobody to have an even number of people
    if len(people) % 2 == 1:
        people.append({name_column: None, email_column: None})

    # Create pairings
    pairings = create_random_pairings(
        people=people,
        num_pairings=num_pairings,
        seed=seed
    )

    # Save pairings
    os.makedirs(pairings_dir, exist_ok=True)

    for i, pairing in enumerate(pairings):
        pairing_data = pd.DataFrame(data=[{
            f'Name_1': pair[0][name_column],
            f'Email_1': pair[0][email_column],
            f'Name_2': pair[1][name_column],
            f'Email_2': pair[1][email_column]
        } for pair in pairing])

        pairing_data.to_csv(os.path.join(pairings_dir, f'pairing_{i + 1}.csv'), index=False)


if __name__ == '__main__':
    Fire(random_pairs)
