from itertools import cycle
import random
from typing import List, Optional, Tuple

from fire import Fire


def create_random_pairings(people: List[str],
                           num_pairings: int,
                           seed: Optional[int] = None) -> List[List[Tuple[str, str]]]:
    """Creates random pairings.

    Creates pairings with random people in the list of people,
    avoiding duplicates until each person has been paired with
    everyone else. On each cycle, the order is re-randomized.
    """
    if seed is not None:
        random.seed(seed)

    pairings: List[List[Tuple[str, str]]] = []

    for shift in cycle(range(1, len(people))):
        if len(pairings) >= num_pairings:
            break

        # Shuffle on each cycle through all the people
        if shift == 1:
            random.shuffle(people)

        # Create a pairing
        pairing = [(people[j], people[(j + shift) % len(people)]) for j in range(len(people))]
        pairings.append(pairing)

    return pairings


def random_pairs(people_path: str = 'people.txt',
                 num_pairings: int = 1,
                 seed: Optional[int] = None,
                 pairings_path: str = 'pairings.txt'):
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
            f.write(f'{"-" * 10} Pairing {i} {"-" * 10}\n\n')
            f.write('\n'.join(' + '.join(pair) for pair in pairing))
            f.write('\n\n')


if __name__ == '__main__':
    Fire(random_pairs)
