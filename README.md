# Oracolo

A Python application that uses machine learning to analyze Italian Lotto extractions.
Features an interactive CLI, statistical visualizations, and predictive analysis.

## 🚀 Features

- **Number Prediction**: Uses Decision Trees for predictive analysis
- **Interactive CLI**: User-friendly command-line interface
- **Statistical Analysis**: Detailed statistics and visualizations
- **Colored Output**: Intuitive interface with visual feedback
- **Design Patterns**: Implementation of Strategy, Factory, and Template Method
- **Comprehensive Testing**: Test suite with >90% coverage

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Pandas
- Scikit-learn
- Colorama
- Tabulate

## 🛠️ Installation and Running

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Mauto82/oracolo.git
cd oracolo

# Build and start the interactive CLI
docker-compose run --rm oracolo
```

### Local Installation

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r dockerfiles/requirements.txt

# Start the application
python app/cli.py
```

## 💻 Usage

Once the interactive CLI is running, you'll see:
```
--------------------------------------------------
Benvenuto in Oracolo!
Digita 'help' o '?' per la lista dei comandi.
--------------------------------------------------
(oracolo)
```

### Available Commands

```
predict <date> <wheel> - Make a prediction
                        Date format: DD/MM/YYYY
                        Example: predict 01/01/2024 MI

stats <wheel>         - Show statistics for a specific wheel
                        Example: stats MI

ruote                 - Show available wheels

convert               - Convert historical data file from
                        https://www.giocodellotto-online.it/lotto/estrazioni/archivio
                        to application format. 
                        (download the storico.txt file and put it in /data application directory)

clear                 - Clear the screen

help                  - Show this message

quit                  - Exit the program
```

### Example Session
```bash
# Start the interactive CLI
docker-compose run --rm oracolo

# Then in the CLI
(oracolo) predict 01/01/2024 MI
(oracolo) stats MI
(oracolo) ruote
(oracolo) quit
```

## 🧪 Testing

```bash
# Run tests using Docker
docker-compose -f docker-compose-test.yaml up --build

# Run tests locally
pytest
```

### Coverage Report
```bash
pytest --cov=app --cov-report=html
```

## 🔧 Quick Development Commands

```bash
# Start interactive CLI
docker-compose run --rm oracolo

# Run tests
docker-compose -f docker-compose-test.yaml up --build

# Clean up containers
docker-compose down --remove-orphans

# Rebuild and start
docker-compose build
docker-compose run --rm oracolo
```

## 📁 Project Structure

```
.
├── app/
│   ├── cli.py                              # Interactive CLI
│   ├── config.py                           # Configuration
│   ├── data/
│   │   ├── data_loader.py                  # Data Loading
│   │   ├── estrazioni-lotto.csv            # Main data file
│   ├── models/
│   │   └── extraction.py                   # Data Models
│   ├── predictors/
│   │   ├── predictor_interface.py
│   │   ├── predictor_factory.py
│   │   └── decision_tree_predictor.py
│   ├── presentation/
│   │   └── output_formatter.py             # Output Formatting
│   └── services/
│       ├── lotto_service.py                # Business Logic
│       └── format_converter.py             # Data Format Converter
├── tests/
├── dockerfiles/
└── docker-compose.yaml
```

## 📊 Detailed Features

### Statistical Analysis
- Number frequency analysis
- Recurring patterns detection
- Delay numbers tracking
- Frequent number pairs identification

### Data Analysis
- Historical trends
- Pattern recognition
- Statistical correlations
- Frequency distribution

## 🔧 Technical Implementation

### Prediction System
- Decision Tree based analysis
- Historical data processing
- Pattern recognition algorithms
- Statistical modeling

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Use type hints
- Follow SOLID principles

## 📝 Notes

- This application is intended for educational purposes
- Predictions are based on statistical analysis
- No guarantee of lottery wins
- Uses historical data for analysis

## ⚠️ Disclaimer

This application is designed for educational and entertainment purposes only. It does not guarantee any wins in the actual Italian Lotto game. Gambling can be addictive and should be approached responsibly.

## 🐛 Known Issues

See the [Issues](https://github.com/Mauto82/oracolo/issues) page for current known issues and feature requests.

## 📈 Future Plans

- Machine Learning model improvements
- Additional statistical analysis features
- Web interface
- API endpoints
- Mobile application

## ⚖️ License

This project is licensed under the MIT License.

## 👥 Authors

- **Matteo** - *Initial work* - [MAuToBlog](https://mautoblog.com/posts/anatomia-di-un-refactoring/)

## 🙏 Acknowledgments

- Italian Lotto historical data providers
- Python community
- Contributors and testers

## 📞 Contact

For support or queries:
- Create an issue
- Send a pull request
- Contact the maintainers

## 🔍 Version History

- 1.0.0: Initial release
- 1.1.0: Added interactive CLI
- 1.2.0: Added statistical analysis
- 1.3.0: Added visualization features

---

Made with ❤️ by Matteo