# 📐 Unit Converter

A versatile command-line tool for converting between different units of measurement.

## ✨ Features

- 🔢 Convert between various units of measurement
- 📏 Support for multiple categories (length, weight, temperature, volume, etc.)
- 🌡️ Special handling for temperature conversions
- 📊 Conversion history tracking
- 🔍 Auto-detect unit categories
- 💾 Save conversion history locally

## 🔄 Supported Categories

### Length
- mm, cm, m, km, inch, feet, yard, mile

### Weight/Mass
- mg, g, kg, ton, ounce, pound, stone

### Temperature
- celsius, fahrenheit, kelvin

### Volume
- ml, l, m³, cup, pint, quart, gallon

### Area
- mm², cm², m², km², acre, hectare

### Speed
- km/h, m/s, mph, knots

### Time
- second, minute, hour, day, week, month, year

### Data Size
- byte, KB, MB, GB, TB, PB

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xAr3s/unit-converter.git
cd unit-converter
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `convert`: Convert between units
- `categories`: List all conversion categories
- `units`: List units in a category
- `history`: View conversion history

## 📋 Command Options

### Convert:
```bash
python main.py convert <value> <from_unit> <to_unit> [options]
```

Options:

- `-c, --category`: Conversion category (optional, auto-detected)

### List categories:
```bash
python main.py categories
```

### List units in a category:
```bash
python main.py units <category>
```

### View history:
```bash
python main.py history [options]
```

Options:

- `-l, --limit`: Number of history items to show (default: 10)

## 📝 Examples

### Length conversion:
```bash
python main.py convert 100 cm m
python main.py convert 5.5 feet inch
python main.py convert 10 km mile
```

### Weight conversion:
```bash
python main.py convert 2.5 kg pound
python main.py convert 150 g ounce
python main.py convert 1 ton kg
```

### Temperature conversion:
```bash
python main.py convert 32 fahrenheit celsius
python main.py convert 0 celsius kelvin
python main.py convert 300 kelvin fahrenheit
```

### Volume conversion:
```bash
python main.py convert 1 gallon l
python main.py convert 500 ml cup
python main.py convert 2 m³ gallon
```

### Auto-detect category:
```bash
# The tool automatically detects the category
python main.py convert 100 mph km/h
python main.py convert 1024 byte MB
```

### List available categories:
```bash
python main.py categories
```

### List units in a category:
```bash
python main.py units length
python main.py units temperature
```

### View conversion history:
```bash
python main.py history
python main.py history -l 5
```

## 💡 Tips

- The tool automatically detects the category when possible
- Temperature conversions are handled specially for accuracy
- Use decimal values for precise conversions
- History is saved automatically for last 50 conversions
- You can mix metric and imperial units in the same conversion
- For data sizes, remember that 1 KB = 1024 bytes (binary)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
