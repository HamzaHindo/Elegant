import os
import shutil

from utils.calendar_utils import get_arabic_month


class FileManager:
    def __init__(self, output_directory):
        self.output_directory = output_directory

    def _get_year_path(self, year):
        return os.path.join(self.output_directory, str(year))

    def _get_current_path(self, year):
        return os.path.join(self._get_year_path(year), "current")

    def _get_archive_path(self, year):
        return os.path.join(self._get_year_path(year), "archive")

    def _get_month_name(self, month):
        return get_arabic_month(month).lower()

    def ensure_directories(self, year):
        os.makedirs(self._get_current_path(year), exist_ok=True)
        os.makedirs(self._get_archive_path(year), exist_ok=True)

    def archive_current_files(self, year, current_month):
        """Move all files from current/ to archive/{prev_month}/"""
        current_path = self._get_current_path(year)
        if not os.path.exists(current_path):
            return

        files = [f for f in os.listdir(current_path) if os.path.isfile(os.path.join(current_path, f))]
        if not files:
            return

        # Archive under the previous month name (the month that was in current)
        # We archive all existing files from current into the folder named after the month
        # they belong to. Since we only keep one month in current, we archive by that month.
        # But we need to know which month was there. We'll infer from filenames or just use
        # a generic approach. Actually, the user said: put all prev months in archive.
        # Since current only has one month, we archive it under its month name.
        # We'll extract month from the filename: {Prefix}_{month}_{year}.xlsx
        for filename in files:
            try:
                # Remove known prefixes and extension
                clean = filename
                for prefix in ["Attendance_", "Revenue_"]:
                    clean = clean.replace(prefix, "")
                clean = clean.replace(".xlsx", "")
                parts = clean.split("_")
                if len(parts) >= 2:
                    prev_month = int(parts[0])
                    month_name = self._get_month_name(prev_month)
                else:
                    month_name = "unknown"
            except (ValueError, IndexError):
                month_name = "unknown"

            archive_month_path = os.path.join(self._get_archive_path(year), month_name)
            os.makedirs(archive_month_path, exist_ok=True)

            src = os.path.join(current_path, filename)
            dst = os.path.join(archive_month_path, filename)
            shutil.move(src, dst)

    def _get_month_folder_path(self, year, month):
        """Return the path to the month folder in current directory."""
        month_name = self._get_month_name(month)
        return os.path.join(self._get_current_path(year), month_name)

    def get_output_path(self, year, month):
        """Return the full path where the new file should be saved."""
        self.ensure_directories(year)
        filename = f"Attendance_{month}_{year}.xlsx"
        return os.path.join(self._get_current_path(year), filename)

    def get_month_folder_output_path(self, year, month, filename):
        """
        Return the full path for a file in the month folder.
        
        Args:
            year: Year number
            month: Month number
            filename: Name of the file (e.g., "Attendance_12_2026.xlsx")
            
        Returns:
            Full path to the file in the month folder
        """
        month_folder = self._get_month_folder_path(year, month)
        os.makedirs(month_folder, exist_ok=True)
        return os.path.join(month_folder, filename)

    def prepare_for_generation(self, year, month):
        """Archive current files and return the output path for the new file."""
        self.ensure_directories(year)
        self.archive_current_files(year, month)
        return self.get_output_path(year, month)
    
    def prepare_month_folder_for_generation(self, year, month):
        """
        Prepare a month folder for generation.
        Archives existing month folder if it exists, then creates a new one.
        
        Args:
            year: Year number
            month: Month number
            
        Returns:
            Path to the month folder
        """
        self.ensure_directories(year)
        
        month_folder = self._get_month_folder_path(year, month)
        
        # If month folder already exists, archive it
        if os.path.exists(month_folder):
            month_name = self._get_month_name(month)
            archive_month_path = os.path.join(self._get_archive_path(year), month_name)
            
            # If archive already has this month, add timestamp
            if os.path.exists(archive_month_path):
                import time
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                archive_month_path = os.path.join(
                    self._get_archive_path(year), 
                    f"{month_name}_{timestamp}"
                )
            
            shutil.move(month_folder, archive_month_path)
        
        # Create fresh month folder
        os.makedirs(month_folder, exist_ok=True)
        
        return month_folder
