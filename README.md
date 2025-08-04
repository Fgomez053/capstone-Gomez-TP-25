# Weather Dashboard Capstone

A Python-based weather dashboard built with CustomTkinter that fetches and displays current weather data, maintains a history log, and offers activity suggestions based on conditions.

## Features

- **Current Weather**: Fetches live weather data for any city via the OpenWeatherMap API.
- **Weather History Tracker**: Saves daily weather snapshots to CSV and displays the last 7 days.
- **Activity Suggester**: Recommends outdoor activities based on the day's weather.
- **Theme Switcher**: Dynamically changes UI theme (light/dark or weather-based colors).
- **City Tracking**: Select a city to auto-log its weather each day and view 3/5/7-day history.
- **Customizable Preferences**: Store API keys and user settings in `config.py`.

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/<https://github.com/Fgomez053/capstone-Gomez-TP-25.git
   cd <capstone>
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows PowerShell
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open `config.py` and set your `API_KEY` for OpenWeatherMap.
2. Run the app:
   ```bash
   python main.py
   ```
3. Use the GUI to:
   - Enter a city and fetch current weather.
   - View the last 3, 5, or 7 days of logged weather.
   - Toggle themes or let it auto-switch based on temperature.
   - Start/stop city tracking.
   - A graph that displays and compares our group city's weather

## File Structure

```
CAPSTONE-GOMEZ-TP-25/
├── __pycache__/                 
├── cache/                       
├── core/                        
│   ├── __pycache__/             
│   ├── __init__.py              
│   ├── .env                     
│   ├── api.py                   
│   └── storage.py               
├── data/                        
│   ├── __init__.py              
│   ├── my_ctkcolor.json         
│   ├── tracking_button_data.csv 
│   └── weather_history.csv      
├── docs/                        
│   ├── W15_After_class_assignment.md  
│   └── week11_reflection.md     
├── features/                    
│   ├── __pycache__/             
│   ├── __init__.py              
│   ├── activity_suggester.py    
│   ├── dark_theme.py            
│   └── tracking_button.py       
├── Group3/                      
│   ├── __pycache__/             
│   ├── abil_csv.csv             
│   ├── felix.csv                
│   ├── group_feature.py         
│   ├── kendra.csv               
│   ├── practiceskillscheck.py   
│   ├── README.md                
│   ├── ricky.csv                
│   └── tashoy_csv.csv           
├── gui/                         
│   ├── __pycache__/             
│   ├── __init__.py              
│   └── app.py                   
├── tests/                       
├── venv/                        
├── __init__.py                  
├── config.py                    
├── example.py                   
├── main.py                      
├── README.md                    
└── requirements.txt             

```

## Contributing

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes and open a PR.
4. Ensure all tests pass and update documentation as needed.

## License

Distributed under the MIT License. See `LICENSE` for details.
