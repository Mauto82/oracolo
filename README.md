# Oracolo

A Python application that uses machine learning to analyze Italian Lotto extractions.
Features an interactive CLI, statistical visualizations, and predictive analysis.

## 🚀 Features

- **Number Prediction**: Uses Decision Trees for predictive analysis
- **Interactive CLI**: User-friendly command-line interface
- **Statistical Analysis**: Detailed statistics and visualizations
- **System Generation**: Creates integral, reduced and guaranteed systems
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

sistema <date> <wheel> <type> [params] - Generate playing systems
                        Types:
                        - integrale N: All possible N number combinations (2-4)
                        - ridotto N: Optimized subset of N number combinations (2-4)
                        - garantito N/P: System guaranteeing P points with N numbers
                        Example: sistema 01/01/2024 MI integrale 2

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
(oracolo) sistema 01/01/2024 MI integrale 2
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

### Data Analysis
- Historical trends
- Pattern recognition
- Statistical correlations
- Frequency distribution

### Statistical Analysis
- Number frequency analysis
- Recurring patterns detection
- Delay numbers tracking
- Frequent number pairs identification

### System Generation
- Integral systems (all possible combinations)
- Reduced systems (optimized subsets)
- Guaranteed systems (with win conditions)
- Support for pairs, triples and quadruples

### System Generation Examples

```bash
# Predict numbers and generate systems
(oracolo) predict 01/01/2024 MI
Predizione per Milano: 1, 13, 27, 45, 82

# Generate all possible pairs (sistema integrale)
(oracolo) sistema 01/01/2024 MI integrale 2
==================================================
SISTEMA INTEGRALE 2 NUMERI
==================================================
Numeri base: 1, 13, 27, 45, 82
Combinazioni di 2 numeri:
--------------------------------------------------
 1) 1 - 13
 2) 1 - 27
 3) 1 - 45
 4) 1 - 82
 5) 13 - 27
 6) 13 - 45
 7) 13 - 82
 8) 27 - 45
 9) 27 - 82
10) 45 - 82
--------------------------------------------------
Totale combinazioni: 10
==================================================

# Generate reduced triplets (sistema ridotto)
(oracolo) sistema 01/01/2024 MI ridotto 3
==================================================
SISTEMA RIDOTTO 3 NUMERI
==================================================
Numeri base: 1, 13, 27, 45, 82
Combinazioni ridotte di 3 numeri:
--------------------------------------------------
 1) 1 - 13 - 27
 2) 1 - 45 - 82
 3) 13 - 27 - 45
 4) 13 - 45 - 82
 5) 27 - 45 - 82
--------------------------------------------------
Totale combinazioni: 5
==================================================

# Generate a system guaranteeing ambo with 3 numbers (sistema garantito)
(oracolo) sistema 01/01/2024 MI garantito 3/2
==================================================
SISTEMA GARANTITO 3/2
==================================================
Numeri base: 1, 13, 27, 45, 82
Combinazioni che garantiscono 2 punti con 3 numeri:
--------------------------------------------------
 1) 1 - 13 - 27
 2) 1 - 45 - 82
 3) 13 - 27 - 45
--------------------------------------------------
Totale combinazioni: 3
Vincita garantita: 2 punti
==================================================

# Examples with different wheels
(oracolo) sistema 01/01/2024 NA integrale 2  # Naples wheel
(oracolo) sistema 01/01/2024 BA ridotto 3    # Bari wheel
(oracolo) sistema 01/01/2024 RO garantito 4/2 # Rome wheel

# Common error scenarios
(oracolo) sistema 01/01/2024 MI integrale 5   # Error: numbers must be between 2 and 4
(oracolo) sistema 01/01/2024 MI ridotto 1     # Error: numbers must be between 2 and 4
(oracolo) sistema 01/01/2024 MI garantito 2/3 # Error: cannot guarantee 3 points with 2 numbers

# Progressive system building
(oracolo) predict 01/01/2024 MI           # First get prediction
(oracolo) sistema 01/01/2024 MI ridotto 2  # Try with pairs
(oracolo) sistema 01/01/2024 MI ridotto 3  # Try with triplets
(oracolo) sistema 01/01/2024 MI ridotto 4  # Try with quadruplets

# System analysis workflow
(oracolo) predict 01/01/2024 MI           # Get prediction
(oracolo) stats MI                        # Analyze wheel statistics
(oracolo) sistema 01/01/2024 MI integrale 2  # Generate complete system
(oracolo) sistema 01/01/2024 MI ridotto 2    # Generate optimized system
```

Tips for System Generation:
- Start with a prediction to get the base numbers
- Use `stats` command to analyze the wheel's behavior
- For small bets, use `ridotto` to get fewer combinations
- For maximum coverage, use `integrale`
- Use `garantito` when you want specific win conditions
- Consider using multiple wheels for diversification
- Always verify the number of combinations before playing
- Start with pairs (2 numbers) and progressively increase if needed

Remember:
- The system generator works with the predicted numbers
- All systems are based on the 5 numbers from the prediction
- The number of combinations increases with the number of base numbers
- Reduced systems offer a good balance between coverage and cost
- Guaranteed systems ensure specific win conditions but may have more combinations

## 🔧 Technical Implementation

### Prediction System
- Decision Tree based analysis
- Historical data processing
- Pattern recognition algorithms
- Statistical modeling

### System Generator
- Combinatorial algorithms
- System optimization
- Win guarantee verification
- Efficient storage and display

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
- Advanced system optimization algorithms
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
- 1.4.0: Added system generation and data conversion

---

Made with ❤️ by Matteo