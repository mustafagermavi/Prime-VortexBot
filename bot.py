name: Crypto Bot Auto Run

on:
  schedule:
    - cron: '*/30 * * * *'  # هەر ٣٠ خۆلەکان جارەکێ کار دکەت
  workflow_dispatch:        # دا تو ب دەستێ خۆ ژی بشێی "Run" بکەی

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install ccxt requests

      - name: Run Python Script
        run: python bot.py
