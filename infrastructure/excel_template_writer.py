"""
Excel Template Writer - Base abstract class for Excel template generation.
Provides common functionality for all template writers.
"""
from abc import ABC, abstractmethod

from openpyxl import Workbook

from infrastructure.excel_style_manager import ExcelStyleManager
from infrastructure.excel_worksheet_helper import ExcelWorksheetHelper
from infrastructure.file_manager import FileManager


class ExcelTemplateWriter(ABC):
    """
    Abstract base class for Excel template writers.
    
    Provides common functionality and enforces implementation of write method.
    """

    def __init__(self, output_directory: str = "./output"):
        """
        Initialize the template writer.
        
        Args:
            output_directory: Directory where Excel files will be saved
        """
        self.output_directory = output_directory
        self.style_manager = ExcelStyleManager()
        self.worksheet_helper = ExcelWorksheetHelper(self.style_manager)
        self.file_manager = FileManager(output_directory)

    def cell(self, col: int, row: int) -> str:
        """
        Convert column and row numbers to Excel cell reference.
        Delegates to worksheet helper for consistency.
        
        Args:
            col: Column number (1-indexed)
            row: Row number (1-indexed)
            
        Returns:
            Excel cell reference (e.g., "A1", "B2")
        """
        return self.worksheet_helper.cell(col, row)

    def create_workbook(self) -> Workbook:
        """
        Create a new workbook instance.
        
        Returns:
            New Workbook object
        """
        return Workbook()

    def save_workbook(self, wb: Workbook, year: int, month: int, filename_prefix: str = "", use_month_folder: bool = False):
        """
        Save the workbook to the output directory.
        
        Args:
            wb: Workbook to save
            year: Year for filename
            month: Month for filename
            filename_prefix: Optional prefix for filename (e.g., "Revenue_", "Attendance_")
            use_month_folder: If True, saves to a month folder instead of directly to output
        """
        if use_month_folder:
            # Generate filename
            if not filename_prefix:
                filename_prefix = "Attendance_"
            filename = f"{filename_prefix}{month}_{year}.xlsx"
            
            # Get path in month folder
            output_path = self.file_manager.get_month_folder_output_path(year, month, filename)
        else:
            # Original behavior - save directly to output directory
            output_path = self.file_manager.prepare_for_generation(year, month)
            
            if filename_prefix:
                # Replace default prefix with custom one
                output_path = output_path.replace("Attendance_", filename_prefix)
        
        wb.save(output_path)

    @abstractmethod
    def write(self, template):
        """
        Write the template to an Excel file.
        Must be implemented by subclasses.
        
        Args:
            template: Template object containing data to write
        """
        pass
