#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen
import sys


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    directory = 'repository-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]
    no_weekends = args.no_weekends
    frequency = args.frequency

    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        print(f"Directory '{directory}' already exists. Using existing directory.")

    os.chdir(directory)
    run(['git', 'init', '-b', 'main']) 

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])
    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    # Hardcoded date range: Jan 1, 2017 to Dec 31, 2020
    start_date = datetime(2017, 1, 1, 20, 0) 
    end_date = datetime(2019, 12, 15, 20, 0)
    total_days = (end_date - start_date).days + 1

    for day in (start_date + timedelta(n) for n in range(total_days)):
        if (not no_weekends or day.weekday() < 5) and randint(0, 100) < frequency:
            for commit_time in (day + timedelta(minutes=m) for m in range(contributions_per_day(args))):
                contribute(commit_time)

    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation \x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    Popen(commands).wait()


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    max_c = args.max_commits
    if max_c > 20:
        max_c = 20
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends', action='store_true', default=False,
                        help="Do not commit on weekends.")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        help="Maximum commits per day (1–20).")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        help="Chance of committing on a given day (0–100).")
    parser.add_argument('-r', '--repository', type=str,
                        help="Remote git repository to push to.")
    parser.add_argument('-un', '--user_name', type=str,
                        help="Git user.name override.")
    parser.add_argument('-ue', '--user_email', type=str,
                        help="Git user.email override.")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
