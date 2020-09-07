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

First, create a CSV file containing all the people to be paired with their email addresses, one on each line. For instance, `examples/people.csv` contains the following:

```
Name,Email
Person A,person_a@random_pairs.com
Person B,person_b@random_pairs.com
Person C,person_c@random_pairs.com
Person D,person_d@random_pairs.com
```

Then run `random_pairs.py`, indicating which file contains the people to pair and where the pairings should be saved. For example:

```
python random_pairs.py --people_path examples/people.csv --pairings_dir examples/pairings
```

This will then save the pairings to `examples/pairings/pairing_<i>.csv` for each pairing `<i>`, which will look like the following:

```
Name_1,Email_1,Name_2,Email_2
Person B,person_b@random_pairs.com,Person C,person_c@random_pairs.com
Person D,person_d@random_pairs.com,Person A,person_a@random_pairs.com
```

If there is an odd number of people, then one person will be unpaired in each pairing.

## Options

### Number of pairings

You can specify the number of pairings to create by adding `--num_pairings n` where `n` is the number of pairings. By default, each person will be paired with everyone else exactly once, i.e., there will be `n = #people - 1` pairings.

### Random seed

You can set a random seed for reproducibility with `--seed r` where `r` is the random seed.

## Sending emails automatically via Gmail

First, follow steps 1 and 2 of the following link to set up authentication and to install the required packages: https://developers.google.com/gmail/api/quickstart/python

Next, run the following to email a pairing:

```
python email_pairs --pairings_dir examples/pairings --pairing_num 1 --sender_name John
```

Additional options include:

* `--my_email <email>` to specify the email of the sender if the sender is a participant in the pairing.
* `--subject_prefix <prefix>` to specify the prefix in the subject line of the email prior to `pairing_num`.
