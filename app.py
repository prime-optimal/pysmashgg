import os
import argparse
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
import pysmashgg
from pysmashgg.tournaments import show_events
from pysmashgg.api import run_query
from pysmashgg.t_queries import SHOW_LIGHTWEIGHT_RESULTS_QUERY

# Load environment variables
load_dotenv()

# Initialize SmashGG with API key
smash = pysmashgg.SmashGG(os.getenv('KEY'))

def get_top_8(response):
    if 'data' in response and 'event' in response['data'] and 'standings' in response['data']['event']:
        standings = response['data']['event']['standings']['nodes']
        top_8 = []
        for player in standings[:8]:
            top_8.append({
                "placement": player['placement'],
                "name": player['entrant']['name']
            })
        return top_8
    return None

def export_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def export_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Event", "Placement", "Name"])
        for event in data:
            for player in data[event]:
                writer.writerow([event, player["placement"], player["name"]])

def export_txt(data, filename):
    with open(filename, 'w') as f:
        for event in data:
            f.write(f"{event}:\n")
            for player in data[event]:
                f.write(f"{player['placement']}: {player['name']}\n")
            f.write("\n")

def main():
    # Set up argument parser with more detailed help information
    parser = argparse.ArgumentParser(
        description="Fetch Top 8 results for a Smash.gg tournament",
        epilog="Example usage: python app.py smash-summit-10-online -j results.json"
    )
    parser.add_argument("tournament_slug", 
                        help="The slug of the tournament (e.g., 'smash-summit-10-online'). "
                             "This is typically the last part of the tournament's URL on smash.gg.")
    parser.add_argument("-j", "--json", metavar="FILE",
                        help="Export results in JSON format to the specified file")
    parser.add_argument("-c", "--csv", metavar="FILE",
                        help="Export results in CSV format to the specified file")
    parser.add_argument("-t", "--txt", metavar="FILE",
                        help="Export results in TXT format to the specified file")
    
    # Parse arguments
    args = parser.parse_args()

    # Get tournament information
    try:
        tournament_info = smash.tournament_show(args.tournament_slug)
        print(f"Tournament Info:")
        print(f"Name: {tournament_info['name']}")
        print(f"Location: {tournament_info['city']}, {tournament_info['state']}")
        start_date = datetime.fromtimestamp(tournament_info['startTimestamp']).strftime('%Y-%m-%d')
        end_date = datetime.fromtimestamp(tournament_info['endTimestamp']).strftime('%Y-%m-%d')
        print(f"Date: {start_date} to {end_date}")
        print(f"Entrants: {tournament_info['entrants']}")
    except Exception as e:
        print(f"Error fetching tournament info for {args.tournament_slug}: {str(e)}")
        return

    # Get tournament events
    try:
        events = show_events(args.tournament_slug, smash.header, smash.auto_retry)
        print(f"\nFound {len(events)} events for tournament: {tournament_info['name']}")
        print("Events:")
        for event in events:
            print(f"- {event['name']} (ID: {event['id']})")
    except Exception as e:
        print(f"Error fetching events for tournament {tournament_info['name']}: {str(e)}")
        return

    # Fetch and display Top 8 for each event
    all_results = {}
    for event in events:
        event_name = event['name']
        event_id = event['id']
        print(f"\nAttempting to fetch Top 8 for {event_name} (ID: {event_id}) at {tournament_info['name']}:")
        try:
            # Execute the query directly
            variables = {"eventId": event_id, "page": 1}
            response = run_query(SHOW_LIGHTWEIGHT_RESULTS_QUERY, variables, smash.header, smash.auto_retry)
            
            top_8 = get_top_8(response)
            if top_8:
                all_results[event_name] = top_8
                total_players = len(response['data']['event']['standings']['nodes'])
                print(f"Top 8 Results ({total_players} players total):")
                for player in top_8:
                    print(f"{player['placement']}: {player['name']}")
            else:
                print("No results found for this event.")
        except Exception as e:
            print(f"Error fetching results for {event_name}: {str(e)}")

    # Export results if flags are set
    if args.json:
        export_json(all_results, args.json)
        print(f"\nResults exported to {args.json} in JSON format.")
    if args.csv:
        export_csv(all_results, args.csv)
        print(f"\nResults exported to {args.csv} in CSV format.")
    if args.txt:
        export_txt(all_results, args.txt)
        print(f"\nResults exported to {args.txt} in TXT format.")

if __name__ == "__main__":
    main()
