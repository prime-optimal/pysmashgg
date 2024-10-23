"""Results export functionality."""

import json
import csv
from pathlib import Path
from typing import Dict, Optional

from .. import console

def export_results(
    results: Dict,
    json_file: Optional[Path] = None,
    csv_file: Optional[Path] = None,
    txt_file: Optional[Path] = None
):
    """Export tournament results to various file formats."""
    if json_file:
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        console.print(f"\n[green]Results exported to {json_file} in JSON format.[/]")
        
    if csv_file:
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Event", "Placement", "Name"])
            for event in results:
                for player in results[event]:
                    writer.writerow([event, player["placement"], player["name"]])
        console.print(f"[green]Results exported to {csv_file} in CSV format.[/]")
        
    if txt_file:
        with open(txt_file, 'w') as f:
            for event in results:
                f.write(f"{event}:\n")
                for player in results[event]:
                    f.write(f"{player['placement']}: {player['name']}\n")
                f.write("\n")
        console.print(f"[green]Results exported to {txt_file} in TXT format.[/]")
