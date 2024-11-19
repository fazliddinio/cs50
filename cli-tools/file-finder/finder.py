#!/usr/bin/env python3
"""
File Finder - Find files with various filters
"""
import argparse
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Generator


def find_files(
    directory: Path,
    pattern: str = "*",
    extension: Optional[str] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    modified_after: Optional[datetime] = None,
    modified_before: Optional[datetime] = None,
    content_pattern: Optional[str] = None,
    recursive: bool = True,
    hidden: bool = False,
) -> Generator[Path, None, None]:
    """
    Find files matching criteria.
    """
    glob_pattern = f"**/{pattern}" if recursive else pattern
    
    for file_path in directory.glob(glob_pattern):
        if not file_path.is_file():
            continue
        
        # Skip hidden files
        if not hidden and file_path.name.startswith("."):
            continue
        
        # Extension filter
        if extension and file_path.suffix.lower() != f".{extension.lower()}":
            continue
        
        try:
            stat = file_path.stat()
            
            # Size filters
            if min_size and stat.st_size < min_size:
                continue
            if max_size and stat.st_size > max_size:
                continue
            
            # Date filters
            mtime = datetime.fromtimestamp(stat.st_mtime)
            if modified_after and mtime < modified_after:
                continue
            if modified_before and mtime > modified_before:
                continue
            
            # Content filter
            if content_pattern:
                try:
                    content = file_path.read_text(errors='ignore')
                    if not re.search(content_pattern, content, re.IGNORECASE):
                        continue
                except:
                    continue
            
            yield file_path
            
        except (PermissionError, OSError):
            continue


def format_size(size: int) -> str:
    """Format file size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def find_duplicates(directory: Path, recursive: bool = True) -> dict:
    """Find duplicate files by size and content hash."""
    import hashlib
    from collections import defaultdict
    
    size_map = defaultdict(list)
    
    # Group by size
    for file_path in find_files(directory, recursive=recursive):
        try:
            size = file_path.stat().st_size
            if size > 0:  # Skip empty files
                size_map[size].append(file_path)
        except:
            continue
    
    # Check content for same-size files
    duplicates = {}
    for size, files in size_map.items():
        if len(files) < 2:
            continue
        
        hash_map = defaultdict(list)
        for f in files:
            try:
                hasher = hashlib.md5()
                with open(f, 'rb') as file:
                    for chunk in iter(lambda: file.read(8192), b''):
                        hasher.update(chunk)
                hash_map[hasher.hexdigest()].append(f)
            except:
                continue
        
        for hash_val, dup_files in hash_map.items():
            if len(dup_files) > 1:
                duplicates[hash_val] = dup_files
    
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="File Finder CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Find command
    find = subparsers.add_parser("find", help="Find files")
    find.add_argument("directory", type=Path, nargs="?", default=".", help="Directory")
    find.add_argument("-p", "--pattern", default="*", help="Glob pattern")
    find.add_argument("-e", "--extension", help="File extension")
    find.add_argument("--min-size", type=int, help="Minimum size in bytes")
    find.add_argument("--max-size", type=int, help="Maximum size in bytes")
    find.add_argument("--newer", type=int, help="Modified within N days")
    find.add_argument("--older", type=int, help="Modified more than N days ago")
    find.add_argument("-c", "--content", help="Content regex pattern")
    find.add_argument("--no-recursive", action="store_true", help="Don't recurse")
    find.add_argument("--hidden", action="store_true", help="Include hidden files")
    
    # Duplicates command
    dups = subparsers.add_parser("duplicates", help="Find duplicate files")
    dups.add_argument("directory", type=Path, nargs="?", default=".", help="Directory")
    dups.add_argument("--no-recursive", action="store_true", help="Don't recurse")
    
    # Stats command
    stats = subparsers.add_parser("stats", help="Directory statistics")
    stats.add_argument("directory", type=Path, nargs="?", default=".", help="Directory")
    
    args = parser.parse_args()
    
    if args.command == "find":
        modified_after = None
        modified_before = None
        
        if args.newer:
            modified_after = datetime.now() - timedelta(days=args.newer)
        if args.older:
            modified_before = datetime.now() - timedelta(days=args.older)
        
        print(f"\n🔍 Searching in: {args.directory.absolute()}")
        print("-" * 50)
        
        count = 0
        for f in find_files(
            args.directory,
            args.pattern,
            args.extension,
            args.min_size,
            args.max_size,
            modified_after,
            modified_before,
            args.content,
            not args.no_recursive,
            args.hidden,
        ):
            size = format_size(f.stat().st_size)
            print(f"  {size:>8}  {f}")
            count += 1
            
            if count >= 100:
                print(f"\n... and more (limited to 100)")
                break
        
        print("-" * 50)
        print(f"Found: {count} files")
    
    elif args.command == "duplicates":
        print(f"\n🔍 Finding duplicates in: {args.directory.absolute()}")
        print("-" * 50)
        
        dups = find_duplicates(args.directory, not args.no_recursive)
        
        if dups:
            total_waste = 0
            for hash_val, files in dups.items():
                size = files[0].stat().st_size
                waste = size * (len(files) - 1)
                total_waste += waste
                
                print(f"\n📄 {format_size(size)} (wasted: {format_size(waste)})")
                for f in files:
                    print(f"   {f}")
            
            print("-" * 50)
            print(f"Total duplicate groups: {len(dups)}")
            print(f"Space wasted: {format_size(total_waste)}")
        else:
            print("No duplicates found!")
    
    elif args.command == "stats":
        from collections import defaultdict
        
        ext_stats = defaultdict(lambda: {"count": 0, "size": 0})
        
        for f in find_files(args.directory):
            ext = f.suffix.lower() or "(no ext)"
            try:
                size = f.stat().st_size
                ext_stats[ext]["count"] += 1
                ext_stats[ext]["size"] += size
            except:
                continue
        
        print(f"\n📊 Statistics for: {args.directory.absolute()}")
        print("-" * 50)
        print(f"{'Extension':<12} {'Count':>8} {'Size':>12}")
        print("-" * 50)
        
        for ext, data in sorted(ext_stats.items(), key=lambda x: -x[1]["size"])[:20]:
            print(f"{ext:<12} {data['count']:>8} {format_size(data['size']):>12}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
