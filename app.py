from sleeper_wrapper import League; 

def get_all_roster_id(league: League) -> dict[str,int]:
    '''
    Retrieve a dictionary mapping roster IDs to their respective owner IDs.

    This function takes a 'League' object as input and returns a dictionary that maps roster IDs to their corresponding
    owner IDs in the league.

    Parameters:
        league (League): An object representing the league for which roster IDs and owner IDs are retrieved.

    Returns:
        dict[str, int]: A dictionary containing roster IDs as keys and their respective owner IDs as values.
    '''
    rosters = league.get_rosters()
    roster_owner_id = {}
    for team in rosters: 
        owner_id = team.get('owner_id')
        roster_id = team.get('roster_id')
        roster_owner_id[roster_id] = owner_id
    return roster_owner_id

def get_owner_id_and_display_name(league: League) -> dict[str,str]:
    '''
    Retrieve a dictionary mapping owner IDs to their corresponding display names.

    This function takes a 'League' object as input and returns a dictionary that maps owner IDs to their corresponding
    display names in the league.

    Parameters:
        league (League): An object representing the league for which owner IDs and display names are retrieved.

    Returns:
        dict[str, str]: A dictionary containing owner IDs as keys and their respective display names as values.
    '''
    league_info = league.get_users()
    owner_id_and_display_name_dict = {}
    for i in range(len(league_info)):
        owner_id = league_info[i].get('user_id')
        display_name = league_info[i].get('display_name')
        owner_id_and_display_name_dict[owner_id] = display_name
    return owner_id_and_display_name_dict

def get_weekly_matchups(league: League, week: int) -> list: 
    '''
    Retrieve the matchups for a specific week in the given league.

    This function takes a 'League' object and an integer 'week' as input and returns a list of matchups
    scheduled for the specified week in the league.

    Parameters:
        league (League): An object representing the league for which matchups are retrieved.
        week (int): The week number for which matchups are to be retrieved.

    Returns:
        list: A list of matchups for the specified week in the league. Each matchup is represented as a dictionary
              containing 'matchup_id', 'home_team', and 'away_team'.
    '''
    return league.get_matchups(week)
    

def get_playoff_start_week(league: League) -> int:
    '''
    Retrieve the start week of the playoffs for the given league.

    This function takes a 'League' object as input and returns an integer representing the week
    number when the playoffs start in the league.

    Parameters:
        league (League): An object representing the league for which the playoff start week is retrieved.

    Returns:
        int: The week number when the playoffs start in the league.
    '''
    league_info = league.get_league()
    playoff_start = league_info['settings']['playoff_week_start']
    return playoff_start

def get_league_size(league: League) -> int: 
    '''
    Retrieve the size of the league in terms of the number of rosters.

    This function takes a 'League' object as input and returns an integer representing the total number
    of rosters in the league.

    Parameters:
        league (League): An object representing the league for which the size is retrieved.

    Returns:
        int: The total number of rosters in the league.
    '''
    league_info = league.get_league()
    return league_info['total_rosters']


def get_all_player_points(teamMatchup: dict ) -> int: 
    '''
    Calculate the total points earned by a team in a matchup, excluding points earned by players on the taxi squad.

    This function takes a 'teamMatchup' dictionary as input and returns the total points earned by the team.
    The 'teamMatchup' dictionary contains information about the team's players and their respective points in a matchup.
    The points for each player are stored in the 'players_points' dictionary within the 'teamMatchup' dictionary.

    Parameters:
        teamMatchup (dict): A dictionary representing the matchup for a team. It contains a 'players_points' dictionary
                            with player names as keys and points scored as values.

    Returns:
        int: The total points earned by the team in the matchup, excluding taxi squad player points.
    '''
    all_points = teamMatchup['players_points']
    return sum(all_points[player] for player in all_points)

def total_points_all_weeks(league: League):
    '''
    Calculate the total points scored by each roster/owner in the league across all weeks.

    This function takes a 'League' object as input and returns a dictionary containing the total points
    scored by each roster/owner in the league. The keys of the dictionary are roster/owner IDs, and the values
    are the sum of all points scored by that roster/owner.

    Parameters:
        league (League): An object representing the league for which the total points are calculated.

    Returns:
        dict: A dictionary containing roster/owner IDs as keys and their respective total points as values.
    '''
    playoff_start_week = get_playoff_start_week(league)
    max_points_scored = {}
    league_size = get_league_size(league)
    for i in range(1,league_size+1):
        max_points_scored[i] = 0
    for i in range(1,playoff_start_week):
        weekly_matchups = get_weekly_matchups(league,i)
        for matchup in weekly_matchups:
            #Simply just adding the points... 
            max_points_scored[matchup['roster_id']] += round(get_all_player_points(matchup),2)
    return max_points_scored

def pair_id(roster_id_and_user_id: dict, user_id_and_display_name: dict, points_and_roster_id: dict):
    '''
    Pair roster owner display names with their total points, sorted by total points in descending order.

    This function takes three dictionaries as input: 'roster_id_and_user_id', 'user_id_and_display_name', and 'points_and_roster_id'.
    It returns a list of tuples, each containing a roster owner's display name and their corresponding total points.
    The list is sorted in descending order based on the total points.

    Parameters:
        roster_id_and_user_id (dict): A dictionary mapping roster IDs to user IDs.
        user_id_and_display_name (dict): A dictionary mapping user IDs to display names.
        points_and_roster_id (dict): A dictionary mapping roster IDs to total points.

    Returns:
        list: A list of tuples, each containing a roster owner's display name and their total points.
              The list is sorted in descending order based on the total points.
    '''  
    display_name_total_points = {}

    for key, value in roster_id_and_user_id.items():
        display_name = user_id_and_display_name[value]
        total_points = points_and_roster_id[key]
        display_name_total_points[display_name] = total_points
    return sorted(display_name_total_points.items(), key=lambda item: item[1], reverse=True) 


flag = False

while flag != True: 

    try: 
        league_input = str(input("Enter your Sleeper league ID: "))
        league = League(league_input)
        yearly_points = total_points_all_weeks
        league = League(league_input)
        yearly_points = total_points_all_weeks(league)
        rosterID_userID_dict = get_all_roster_id(league)
        ownerID_display_name_dict = get_owner_id_and_display_name(league)
        all_points_sorted = pair_id(rosterID_userID_dict, ownerID_display_name_dict, yearly_points)
        print('\nSorted list of all points scored: \n', all_points_sorted)
        flag = True
    except TypeError:
        print('That is not a valid Sleeper league ID. Please try again.')



