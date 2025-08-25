#!/usr/bin/env python3
"""
Smart Batch PDF Printer

This script recursively finds all PDF files in a directory and subdirectories,
sorts them alphabetically by directory and filename, and prints them using
the default system printer with default settings.
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import List, Tuple


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('batch_pdf_printer.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def find_pdf_files(root_directory: str) -> List[Tuple[str, str]]:
    """
    Recursively find all PDF files in the given directory and subdirectories.
    
    Args:
        root_directory: Root directory to search for PDF files
        
    Returns:
        List of tuples (directory_path, filename) for sorting
    """
    pdf_files = []
    
    for root, dirs, files in os.walk(root_directory):
        # Sort directories to ensure consistent order
        dirs.sort()
        
        # Find PDF files in current directory
        pdf_files_in_dir = [f for f in files if f.lower().endswith('.pdf')]
        pdf_files_in_dir.sort()  # Sort filenames alphabetically
        
        for pdf_file in pdf_files_in_dir:
            pdf_files.append((root, pdf_file))
    
    return pdf_files


def sort_pdf_files(pdf_files: List[Tuple[str, str]]) -> List[str]:
    """
    Sort PDF files by directory path and then by filename.
    
    Args:
        pdf_files: List of tuples (directory_path, filename)
        
    Returns:
        List of full file paths sorted alphabetically
    """
    # Sort by directory path first, then by filename
    pdf_files.sort(key=lambda x: (x[0], x[1]))
    
    # Return full file paths
    return [os.path.join(directory, filename) for directory, filename in pdf_files]


def print_pdf(file_path: str) -> bool:
    """
    Print a PDF file using the default system printer.
    
    Args:
        file_path: Full path to the PDF file
        
    Returns:
        True if printing was successful, False otherwise
    """
    try:
        # Use lp command on Linux to print with default printer settings
        result = subprocess.run(['lp', file_path], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        logging.info(f"Successfully printed: {file_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to print {file_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        logging.error("lp command not found. Make sure CUPS is installed and configured.")
        return False


def print_pdfs_in_batches(pdf_files: List[str], batch_size: int = 10):
    """
    Print PDF files in batches to avoid overwhelming the printer.
    
    Args:
        pdf_files: List of PDF file paths to print
        batch_size: Number of files to print in each batch
    """
    total_files = len(pdf_files)
    successful_prints = 0
    failed_prints = 0
    
    logging.info(f"Starting to print {total_files} PDF files...")
    
    for i in range(0, total_files, batch_size):
        batch = pdf_files[i:i + batch_size]
        batch_number = (i // batch_size) + 1
        total_batches = (total_files + batch_size - 1) // batch_size
        
        logging.info(f"Processing batch {batch_number}/{total_batches} ({len(batch)} files)")
        
        for pdf_file in batch:
            if print_pdf(pdf_file):
                successful_prints += 1
            else:
                failed_prints += 1
        
        # Add a small delay between batches if not the last batch
        if i + batch_size < total_files:
            import time
            time.sleep(2)  # 2 second delay between batches
    
    logging.info(f"Printing completed. Success: {successful_prints}, Failed: {failed_prints}")


def main():
    """Main function to handle command line arguments and execute the printing process."""
    parser = argparse.ArgumentParser(description='Smart Batch PDF Printer')
    parser.add_argument('directory', 
                       help='Root directory to search for PDF files')
    parser.add_argument('--batch-size', 
                       type=int, 
                       default=10,
                       help='Number of files to print in each batch (default: 10)')
    parser.add_argument('--dry-run',
                       action='store_true',
                       help='Show what would be printed without actually printing')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        logging.error(f"Directory not found: {args.directory}")
        sys.exit(1)
    
    # Find PDF files
    logging.info(f"Searching for PDF files in: {args.directory}")
    pdf_files_tuples = find_pdf_files(args.directory)
    
    if not pdf_files_tuples:
        logging.info("No PDF files found.")
        return
    
    # Sort PDF files
    sorted_pdf_files = sort_pdf_files(pdf_files_tuples)
    
    logging.info(f"Found {len(sorted_pdf_files)} PDF files:")
    for i, pdf_file in enumerate(sorted_pdf_files, 1):
        logging.info(f"  {i:3d}. {pdf_file}")
    
    if args.dry_run:
        logging.info("Dry run mode - no files will be printed.")
        return
    
    # Ask for confirmation
    try:
        response = input(f"\nDo you want to print {len(sorted_pdf_files)} PDF files? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            logging.info("Printing cancelled by user.")
            return
    except KeyboardInterrupt:
        logging.info("\nPrinting cancelled by user.")
        return
    
    # Print PDF files in batches
    print_pdfs_in_batches(sorted_pdf_files, args.batch_size)


if __name__ == "__main__":
    main()