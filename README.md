# Price Monitoring Dashboard

![Python](https://img.shields.io/badge/-Python-blue) ![Flask](https://img.shields.io/badge/-Flask-blue) ![SQLite](https://img.shields.io/badge/-SQLite-blue) ![Chart.js](https://img.shields.io/badge/-Chart.js-blue) ![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-blue)

Full-stack price tracking app. Scrapes product prices daily and visualizes trends. (Demo project)

## Features

- Monitors product prices across sites
- Stores historical data in SQLite
- Web dashboard with price charts
- Email alerts for price drops
- REST API for adding products

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/price-monitor.git
cd price-monitor

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py --url "https://example.com" --output output/results.csv
```

## Output Format

Results are saved as CSV with the following columns:

| Column | Description |
|--------|-------------|
| name   | Item name   |
| value  | Item value  |
| url    | Source URL  |

## Testing

```bash
pytest tests/
```

## License

MIT License

## Contact

For questions or custom scraping projects, contact me at [your-email]

---

**Note:** This is a portfolio project demonstrating web scraping capabilities. Use responsibly and respect websites' Terms of Service.
