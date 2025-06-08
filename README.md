# Clickbot with Keys and Origins

This tool simulates real user behavior on Google Maps using rotating search keywords and origin points. It clicks on a target business and requests directions.

## How to Run

1. Clone the repo:
```
git clone https://github.com/princeshergill/Clickbotwithkeysandorigins.git
cd Clickbotwithkeysandorigins
```

2. Set up your virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
playwright install
```

4. Place your `keywords.txt` and `origins.txt` files in the root.

5. Run:
```
python search_click_bot.py
```

## Output

- Logs: `~/maps-bot/maps_requests.log`
- Screenshots: `~/maps-bot/failures/`
