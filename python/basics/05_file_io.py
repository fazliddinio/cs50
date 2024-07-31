# file I/O practice
import json
import csv
import os
from pathlib import Path


# ============ Basic File Operations ============

def write_text_file(filename, content):
    """Write content to a text file."""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Written to {filename}")


def read_text_file(filename):
    """Read content from a text file."""
    with open(filename, 'r') as f:
        content = f.read()
    return content


def append_to_file(filename, content):
    """Append content to a file."""
    with open(filename, 'a') as f:
        f.write(content + '\n')


def read_lines(filename):
    """Read file line by line."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


# ============ Working with JSON ============

def save_json(data, filename):
    """Save data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to {filename}")


def load_json(filename):
    """Load data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


# ============ Working with CSV ============

def write_csv(data, filename, headers=None):
    """Write data to CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        writer.writerows(data)
    print(f"Saved CSV to {filename}")


def read_csv(filename):
    """Read data from CSV file."""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


# ============ Path Operations ============

def explore_directory(path='.'):
    """List contents of a directory."""
    p = Path(path)
    
    print(f"\nContents of: {p.absolute()}")
    print("-" * 50)
    
    for item in sorted(p.iterdir()):
        if item.is_dir():
            print(f"  [DIR]  {item.name}/")
        else:
            size = item.stat().st_size
            print(f"  [FILE] {item.name} ({size} bytes)")


def find_files_by_extension(directory, extension):
    """Find all files with given extension recursively."""
    p = Path(directory)
    files = list(p.rglob(f"*.{extension}"))
    return files


# ============ Practical Examples ============

class SimpleLogger:
    """Simple file-based logger."""
    
    def __init__(self, log_file='app.log'):
        self.log_file = log_file
    
    def _write(self, level, message):
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] [{level}] {message}"
        append_to_file(self.log_file, entry)
    
    def info(self, message):
        self._write("INFO", message)
    
    def warning(self, message):
        self._write("WARNING", message)
    
    def error(self, message):
        self._write("ERROR", message)


class ConfigManager:
    """JSON-based configuration manager."""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load()
    
    def _load(self):
        if os.path.exists(self.config_file):
            return load_json(self.config_file)
        return {}
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()
    
    def save(self):
        save_json(self.config, self.config_file)


if __name__ == "__main__":
    import tempfile
    
    # Create a temp directory for our tests
    with tempfile.TemporaryDirectory() as tmpdir:
        # Text file operations
        print("=== Text File Operations ===")
        txt_file = os.path.join(tmpdir, "test.txt")
        write_text_file(txt_file, "Hello, World!\nThis is line 2\n")
        content = read_text_file(txt_file)
        print(f"Content: {content}")
        
        append_to_file(txt_file, "Appended line")
        lines = read_lines(txt_file)
        print(f"Lines: {lines}")
        
        # JSON operations
        print("\n=== JSON Operations ===")
        json_file = os.path.join(tmpdir, "data.json")
        data = {
            "name": "Fazliddin",
            "skills": ["Python", "C", "SQL"],
            "projects": 12
        }
        save_json(data, json_file)
        loaded = load_json(json_file)
        print(f"Loaded: {loaded}")
        
        # CSV operations
        print("\n=== CSV Operations ===")
        csv_file = os.path.join(tmpdir, "grades.csv")
        headers = ["name", "subject", "grade"]
        grades = [
            ["Alice", "Math", "A"],
            ["Bob", "Science", "B"],
            ["Charlie", "English", "A"],
        ]
        write_csv(grades, csv_file, headers)
        csv_data = read_csv(csv_file)
        print(f"CSV data: {csv_data}")
        
        # Path operations
        print("\n=== Path Operations ===")
        explore_directory(tmpdir)
        
        print("\nAll tests passed!")
