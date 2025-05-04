#!/usr/bin/env python3

import argparse
import json
import os

# Constants
DEFAULT_CONFIG_FILE = os.path.expanduser("~/.unit_converter.json")

# Conversion rates and formulas
CONVERSIONS = {
    "length": {
        "units": ["mm", "cm", "m", "km", "inch", "feet", "yard", "mile"],
        "base": "m",  # Base unit for conversion
        "conversions": {
            "mm": 0.001,
            "cm": 0.01,
            "m": 1,
            "km": 1000,
            "inch": 0.0254,
            "feet": 0.3048,
            "yard": 0.9144,
            "mile": 1609.344
        }
    },
    "weight": {
        "units": ["mg", "g", "kg", "ton", "ounce", "pound", "stone"],
        "base": "kg",
        "conversions": {
            "mg": 0.000001,
            "g": 0.001,
            "kg": 1,
            "ton": 1000,
            "ounce": 0.0283495,
            "pound": 0.453592,
            "stone": 6.35029
        }
    },
    "temperature": {
        "units": ["celsius", "fahrenheit", "kelvin"],
        "base": "celsius",
        "conversions": {
            # Special handling for temperature in convert_temperature()
        }
    },
    "volume": {
        "units": ["ml", "l", "m³", "cup", "pint", "quart", "gallon"],
        "base": "l",
        "conversions": {
            "ml": 0.001,
            "l": 1,
            "m³": 1000,
            "cup": 0.236588,
            "pint": 0.473176,
            "quart": 0.946353,
            "gallon": 3.78541
        }
    },
    "area": {
        "units": ["mm²", "cm²", "m²", "km²", "acre", "hectare"],
        "base": "m²",
        "conversions": {
            "mm²": 0.000001,
            "cm²": 0.0001,
            "m²": 1,
            "km²": 1000000,
            "acre": 4046.86,
            "hectare": 10000
        }
    },
    "speed": {
        "units": ["km/h", "m/s", "mph", "knots"],
        "base": "m/s",
        "conversions": {
            "km/h": 0.277778,
            "m/s": 1,
            "mph": 0.44704,
            "knots": 0.514444
        }
    },
    "time": {
        "units": ["second", "minute", "hour", "day", "week", "month", "year"],
        "base": "second",
        "conversions": {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 2628000,  # Average month
            "year": 31536000   # 365 days
        }
    },
    "data": {
        "units": ["byte", "KB", "MB", "GB", "TB", "PB"],
        "base": "byte",
        "conversions": {
            "byte": 1,
            "KB": 1024,
            "MB": 1048576,
            "GB": 1073741824,
            "TB": 1099511627776,
            "PB": 1125899906842624
        }
    }
}

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between different units"""
    # Convert to Celsius first
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {from_unit}")
    
    # Convert from Celsius to target unit
    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit == "kelvin":
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {to_unit}")

def convert_unit(value, from_unit, to_unit, category):
    """Convert value from one unit to another"""
    if category not in CONVERSIONS:
        return None, f"Unknown category: {category}"
    
    # Handle temperature separately
    if category == "temperature":
        try:
            result = convert_temperature(value, from_unit, to_unit)
            return result, None
        except ValueError as e:
            return None, str(e)
    
    # Check if units are valid
    cat_data = CONVERSIONS[category]
    if from_unit not in cat_data["units"]:
        return None, f"Unknown unit: {from_unit} for category: {category}"
    if to_unit not in cat_data["units"]:
        return None, f"Unknown unit: {to_unit} for category: {category}"
    
    # Convert to base unit first, then to target unit
    base_value = value * cat_data["conversions"][from_unit]
    result = base_value / cat_data["conversions"][to_unit]
    
    return result, None

def list_categories():
    """List all available conversion categories"""
    print("\nAvailable conversion categories:")
    print("=" * 40)
    for i, category in enumerate(CONVERSIONS.keys(), 1):
        print(f"{i}. {category.capitalize()}")
    print("=" * 40)

def list_units(category):
    """List all units in a category"""
    if category not in CONVERSIONS:
        print(f"Unknown category: {category}")
        return
    
    units = CONVERSIONS[category]["units"]
    print(f"\n{category.capitalize()} units:")
    print("=" * 40)
    for unit in units:
        print(f"- {unit}")
    print("=" * 40)

def save_history(conversion):
    """Save conversion to history"""
    history_file = DEFAULT_CONFIG_FILE
    history = []
    
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except:
            pass
    
    conversion["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, conversion)  # Add to beginning
    
    # Keep only last 50 conversions
    if len(history) > 50:
        history = history[:50]
    
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except:
        pass

def view_history(limit=10):
    """View conversion history"""
    history_file = DEFAULT_CONFIG_FILE
    
    if not os.path.exists(history_file):
        print("No conversion history found")
        return
    
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
    except:
        print("Error reading history file")
        return
    
    if not history:
        print("No conversion history found")
        return
    
    print("\nConversion History:")
    print("=" * 60)
    print(f"{'Time':<20} {'From':<15} {'To':<15} {'Category':<12}")
    print("-" * 60)
    
    for entry in history[:limit]:
        timestamp = entry.get("timestamp", "Unknown")
        from_str = f"{entry['value']} {entry['from']}"
        to_str = f"{entry['result']} {entry['to']}"
        category = entry.get("category", "Unknown")
        
        print(f"{timestamp:<20} {from_str:<15} {to_str:<15} {category:<12}")
    
    print("=" * 60)

def find_category(unit):
    """Find which category a unit belongs to"""
    for category, data in CONVERSIONS.items():
        if unit.lower() in [u.lower() for u in data["units"]]:
            return category
    return None

def main():
    parser = argparse.ArgumentParser(description="Unit Converter - Convert between different units")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert between units")
    convert_parser.add_argument("value", type=float, help="Value to convert")
    convert_parser.add_argument("from_unit", help="Source unit")
    convert_parser.add_argument("to_unit", help="Target unit")
    convert_parser.add_argument("-c", "--category", help="Conversion category (optional, can be auto-detected)")
    
    # List categories command
    categories_parser = subparsers.add_parser("categories", help="List all conversion categories")
    
    # List units command
    units_parser = subparsers.add_parser("units", help="List units in a category")
    units_parser.add_argument("category", help="Category name")
    
    # History command
    history_parser = subparsers.add_parser("history", help="View conversion history")
    history_parser.add_argument("-l", "--limit", type=int, default=10, help="Number of history items to show")
    
    args = parser.parse_args()
    
    from datetime import datetime
    
    if args.command == "convert":
        # Try to detect category if not provided
        if not args.category:
            args.category = find_category(args.from_unit)
            if not args.category:
                args.category = find_category(args.to_unit)
        
        if not args.category:
            print(f"Could not determine category for units: {args.from_unit}, {args.to_unit}")
            print("Use --category to specify the category explicitly")
            return
        
        # Convert
        result, error = convert_unit(args.value, args.from_unit, args.to_unit, args.category)
        
        if error:
            print(f"Error: {error}")
        else:
            print(f"{args.value} {args.from_unit} = {result:.6g} {args.to_unit}")
            
            # Save to history
            save_history({
                "value": args.value,
                "from": args.from_unit,
                "to": args.to_unit,
                "result": result,
                "category": args.category
            })
    
    elif args.command == "categories":
        list_categories()
    
    elif args.command == "units":
        list_units(args.category)
    
    elif args.command == "history":
        view_history(args.limit)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
