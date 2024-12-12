#!/usr/bin/env python3
"""
File Organizer - Automatically organize files by type
"""
import argparse
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# File type mappings
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs", ".ts"],
    "Data": [".json", ".xml", ".csv", ".sql", ".db", ".sqlite"],
    "Executables": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
}


def get_category(extension: str) -> str:
    """Get category for a file extension."""
    ext = extension.lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_files(
    source_dir: Path,
    dest_dir: Path = None,
    dry_run: bool = False,
    by_date: bool = False,
) -> dict:
    """Organize files in directory by type."""
    if dest_dir is None:
        dest_dir = source_dir
    
    stats = defaultdict(int)
    moved_files = []
    
    for file_path in source_dir.iterdir():
        if file_path.is_file() and not file_path.name.startswith("."):
            category = get_category(file_path.suffix)
            
            if by_date:
                # Organize by date
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                target_dir = dest_dir / mtime.strftime("%Y") / mtime.strftime("%m-%B")
            else:
                target_dir = dest_dir / category
            
            target_path = target_dir / file_path.name
            
            if dry_run:
                print(f"Would move: {file_path.name} -> {target_dir.name}/")
            else:
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Handle duplicates
                if target_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    counter = 1
                    while target_path.exists():
                        target_path = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                
                shutil.move(str(file_path), str(target_path))
                print(f"Moved: {file_path.name} -> {target_dir.name}/")
            
            stats[category] += 1
            moved_files.append((file_path.name, category))
    
    return dict(stats)


def undo_organize(directory: Path) -> None:
    """Move all files back to root directory."""
    count = 0
    for subdir in directory.iterdir():
        if subdir.is_dir() and subdir.name in FILE_TYPES or subdir.name == "Other":
            for file_path in subdir.iterdir():
                if file_path.is_file():
                    target = directory / file_path.name
                    if not target.exists():
                        shutil.move(str(file_path), str(target))
                        count += 1
            
            # Remove empty directory
            if not any(subdir.iterdir()):
                subdir.rmdir()
    
    print(f"Restored {count} files to root directory")


def main():
    parser = argparse.ArgumentParser(description="File Organizer")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Organize command
    org = subparsers.add_parser("organize", help="Organize files")
    org.add_argument("directory", type=Path, help="Directory to organize")
    org.add_argument("-o", "--output", type=Path, help="Output directory")
    org.add_argument("-d", "--dry-run", action="store_true", help="Preview only")
    org.add_argument("--by-date", action="store_true", help="Organize by date")
    
    # Undo command
    undo = subparsers.add_parser("undo", help="Undo organization")
    undo.add_argument("directory", type=Path, help="Directory to restore")
    
    # Stats command
    stats = subparsers.add_parser("stats", help="Show file statistics")
    stats.add_argument("directory", type=Path, help="Directory to analyze")
    
    args = parser.parse_args()
    
    if args.command == "organize":
        if not args.directory.exists():
            print(f"❌ Directory not found: {args.directory}")
            return
        
        print(f"\n📁 Organizing: {args.directory}")
        print("-" * 40)
        
        result = organize_files(
            args.directory,
            args.output,
            args.dry_run,
            args.by_date,
        )
        
        print("-" * 40)
        print("📊 Summary:")
        for category, count in sorted(result.items()):
            print(f"   {category}: {count} files")
    
    elif args.command == "undo":
        undo_organize(args.directory)
    
    elif args.command == "stats":
        if not args.directory.exists():
            print(f"❌ Directory not found: {args.directory}")
            return
        
        stats = defaultdict(lambda: {"count": 0, "size": 0})
        
        for file_path in args.directory.rglob("*"):
            if file_path.is_file():
                category = get_category(file_path.suffix)
                stats[category]["count"] += 1
                stats[category]["size"] += file_path.stat().st_size
        
        print(f"\n📊 File Statistics: {args.directory}")
        print("-" * 50)
        print(f"{'Category':<15} {'Count':>8} {'Size':>15}")
        print("-" * 50)
        
        total_count = 0
        total_size = 0
        for cat, data in sorted(stats.items()):
            size_mb = data["size"] / (1024 * 1024)
            print(f"{cat:<15} {data['count']:>8} {size_mb:>12.2f} MB")
            total_count += data["count"]
            total_size += data["size"]
        
        print("-" * 50)
        print(f"{'TOTAL':<15} {total_count:>8} {total_size/(1024*1024):>12.2f} MB")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# duplicates
