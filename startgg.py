#!/usr/bin/env python3

"""Command-line interface for pysmashgg."""

import os
from dotenv import load_dotenv
import pysmashgg

# Load environment variables and initialize SmashGG
load_dotenv()
key = os.getenv('KEY')
if not key:
    raise ValueError("API key not found. Please set the KEY environment variable.")

# Make the SmashGG instance available globally
smash = pysmashgg.SmashGG(key)

if __name__ == "__main__":
    from cli import app
    app()
