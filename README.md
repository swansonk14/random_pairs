# Random Pairs

Randomly pairs people using [round-robin scheduling](https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm).

## Installation

Requires Python 3.6+.

Clone the repo and then install the requirements as follows:

```
git clone https://github.com/swansonk14/random_pairs.git
cd random_pairs
pip install -r requirements.txt
```

## Usage

First, create a text file containing all the people to be paired, one on each line. For instance, `examples/people.txt` contains the following:

```
Person A
Person B
Person C
Person D
```

Then run `random_pairs.py`, indicating which file contains the people to pair and where the pairings should be saved. For example:

```
python random_pairs.py --people_path examples/people.txt --pairings_path examples/pairings.txt
```

This will then save the pairings to `examples/pairings.txt`, which will look like the following:

```
---------- Pairing 1 ----------

Person B + Person C
Person D + Person A

---------- Pairing 2 ----------

Person B + Person A
Person C + Person D

---------- Pairing 3 ----------

Person B + Person D
Person A + Person C
```

If there are an odd number of people, then one person will be paired with "Nobody" in each pairing.

## Options

### Number of pairings

You can specify the number of pairings to create by adding `--num_pairings n` where `n` is the number of pairings. By default, each person will be paired with everyone else exactly once, i.e., there will be `n = #people - 1` pairings.

### Random seed

You can set a random seed for reproducibility with `--seed r` where `r` is the random seed.
