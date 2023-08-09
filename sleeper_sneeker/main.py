#!/usr/bin/env python3
import datetime
import json
import logging

import click
import requests

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

BASE_URL = "https://api.sleeper.app/v1"
USER_BASE_URL = "https://api.sleeper.app/v1/user"
USER_LEAGUE_BASE_URL = f"{BASE_URL}/user"
LEAGUE_BASE_URL = f"{BASE_URL}/league"
CURRENT_YEAR = datetime.date.today().year


def get_user_id(user):
    """
    Returns a user_id for a user
    """
    response = requests.get(f"{USER_BASE_URL}/{user}")
    if response.status_code != 200:
        logger.error(f"Error getting user id for {user}")
        return None
    else:
        return response.json()["user_id"]


def get_users_by_league(league):
    logger.info(f"Checking league: {league}")
    league_url = f"{LEAGUE_BASE_URL}/{league}/users"
    logger.info(f"Getting league details for '{league}'")
    logger.info(f"Sending request to {league_url}")
    response = requests.get(league_url)
    if response.status_code != 200:
        logger.error(f"Error getting league details for {league}")
        return None
    logger.info(f"Received response with status code {response.status_code}")
    league_users = response.json()

    logger.debug(f"League details: {json.dumps(league_users, indent=2)}")
    logger.info(f"Users in league: {len(league_users)}")
    users = [
        {"user_id": user["user_id"], "display_name": user["display_name"]}
        for user in league_users
    ]
    logger.info("------------------------------------------")

    return users


def get_leagues_for_users(user, year):
    logger.info(f"Checking {str(len(user))} users")

    for usr in user:
        if type(usr) is dict:
            usr = usr["display_name"]
        user_url = f"{BASE_URL}/user/{usr}"
        logger.info(f"Getting user details for '{usr}'")
        logger.info(f"Sending request to {user_url}")
        response = requests.get(user_url)

        if response.status_code != 200:
            logger.error(f"Error getting user id for {usr}")
            continue

        logger.debug(f"Received response with status code {response.status_code}")
        user_details = response.json()
        # Print out json response pretty print
        user_id = user_details["user_id"]
        logger.info(f"User ID: {get_user_id(usr)}")

        leagues_url = f"{USER_BASE_URL}/{user_id}/leagues/nfl/{year}"
        logger.info(f"Getting league details for '{usr}'")
        logger.debug(f"Querying url -> '{leagues_url}'")
        response = requests.get(leagues_url)
        logger.debug(f"Received response with status code {response.status_code}")

        # Print out json response pretty print
        logger.debug(f"Leagues response: {json.dumps(response.json(), indent=2)}")
        leagues = response.json()
        logger.info(f"Leagues user is in: {str(len(leagues))}")
        logger.info("------------------------------------------")


@click.command(no_args_is_help=True)
@click.option("-l", "--league", help="League ID to query")
@click.option("-u", "--user", "user_lst", help="User names/ids to query", multiple=True)
@click.option(
    "-y", "--year", help="Year to query, defaults to current year", default=CURRENT_YEAR
)
@click.option("-v", "--verbose", is_flag=True, help="Print debug messages")
def cli(user_lst, year, league, verbose):
    if verbose:
        logger.setLevel(logging.DEBUG)

    users = user_lst
    if league:
        users = get_users_by_league(league)

    get_leagues_for_users(users, year)


if __name__ == "__main__":
    cli()
    logger.info("------------------------------------------")
    logger.info("               SLEEPER SNEAKER            ")
    logger.info("------------------------------------------")
    logger.info("Done!")
