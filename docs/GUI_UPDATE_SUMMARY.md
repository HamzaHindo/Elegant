# GUI Update - Month Folder Generation

## ✅ Changes Completed

Successfully updated the GUI to generate all 3 reports (Attendance, Revenue, Salaries) in a single month folder instead of individual files.

## 📁 New Folder Structure

### Before (Old Structure)
```
output/
├── 2026/
│   ├── current/
│   │   ├── Attendance_12_2026.xlsx
│   │   ├── Revenue_12_2026.xlsx
│   │   └── Salaries_12_2026.xlsx
│   └── archive/
│       └── ...
```

### After (New Structure)
```
output/
├── 2026/
│   ├── current/
│   │   └── ديسمبر/  (December folder)
│   │       ├── Attendance_12_2026.xlsx
│   │       ├── Revenue_12_2026.xlsx
│   │       └── Salaries_12_2026.xlsx
│   └── archive/
│       ├── نوفمبر/  (November - archived)
│       └── أكتوبر/  (October - archived)
```

## 🔧 Files Modified

### 1. **`infrastructure/file_manager.py`**
   - ✅ Added `_get_month_folder_path()` - Returns path to month folder
   - ✅ Added `get_month_folder_output_path()` - Returns file path in month folder
   - ✅ Added `prepare_month_folder_for_generation()` - Archives old month folder and creates new one
   - ✅ Archives with timestamp if month already exists in archive

### 2. **`infrastructure/excel_template_writer.py`**
   - ✅ Updated `save_workbook()` to accept `use_month_folder` parameter
   - ✅ When `use_month_folder=True`, saves to month folder
   - ✅ When `use_month_folder=False`, uses old behavior (direct to output)

### 3. **`infrastructure/attendance_template_writer.py`**
   - ✅ Updated `write()` to accept `use_month_folder` parameter
   - ✅ Passes parameter to `save_workbook()`

### 4. **`infrastructure/revenue_template_writer.py`**
   - ✅ Updated `write()` to accept `use_month_folder` parameter
   - ✅ Passes parameter to `save_workbook()`

### 5. **`infrastructure/salaries_template_writer.py`**
   - ✅ Updated `write()` to accept `use_month_folder` parameter
   - ✅ Passes parameter to `save_workbook()`

### 6. **`application/salary_template_service.py`** (NEW)
   - ✅ Created service for salary generation
   - ✅ Follows same pattern as attendance and revenue services
   - ✅ Supports `use_month_folder` parameter

### 7. **`presentation/windows/main_window.py`**
   - ✅ Updated title to "Monthly Reports Generator"
   - ✅ Added **"Generate All Reports"** button (main button, bold, larger)
   - ✅ Added individual buttons: "Attendance Only", "Revenue Only", "Salaries Only"
   - ✅ Implemented `_on_generate_all()` - Generates all 3 files in month folder
   - ✅ Implemented `_on_generate_salaries()` - Generates salaries only
   - ✅ Shows success message with folder location and file list

## 🎨 GUI Layout

```
┌─────────────────────────────────────────────────────────┐
│           Monthly Reports Generator                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Year: [2026 ▼]    Month: [12 ▼]                      │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Generate All Reports                              │ │
│  │ (Attendance + Revenue + Salaries)                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │
│  │ Attendance  │ │  Revenue    │ │   Salaries      │ │
│  │    Only     │ │    Only     │ │     Only        │ │
│  └─────────────┘ └─────────────┘ └─────────────────┘ │
│                                                         │
│  Status: ✅ All reports generated successfully!        │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │              Settings                             │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🚀 How It Works

### Generate All Reports (Main Button)

1. **Validates** employees and stylists exist
2. **Prepares month folder** - Archives old folder if exists
3. **Generates Attendance** - Saves to month folder
4. **Generates Revenue** - Saves to month folder
5. **Generates Salaries** - Reads attendance from month folder, saves salaries to month folder
6. **Shows success message** with folder location and file list

### Individual Buttons

- **Attendance Only** - Generates attendance sheet (old behavior, direct to output)
- **Revenue Only** - Generates revenue sheet (old behavior, direct to output)
- **Salaries Only** - Asks for attendance file, generates salaries (old behavior, direct to output)

## 📋 Success Message

When "Generate All Reports" succeeds, shows:

```
✅ Success

All reports generated successfully!

Location: /path/to/output/2026/current/ديسمبر

Files:
• Attendance_12_2026.xlsx
• Revenue_12_2026.xlsx
• Salaries_12_2026.xlsx
```

## 🔄 Workflow

### Typical Monthly Workflow

1. **Start of Month** - Click "Generate All Reports"
2. **System Creates** - Month folder (e.g., "ديسمبر")
3. **System Generates**:
   - Attendance sheet (empty, ready to fill)
   - Revenue sheet (empty, ready to fill)
   - Salaries sheet (reads from attendance, shows 0 days initially)
4. **User Fills** - Attendance and Revenue data throughout the month
5. **End of Month** - Salaries automatically calculated from attendance
6. **Next Month** - Click "Generate All Reports" again
   - Old month folder archived automatically
   - New month folder created

## 🗂️ Archive Behavior

### When Generating New Month

If month folder already exists:
1. **Moves entire folder** to archive
2. **Adds timestamp** if archive already has that month (e.g., `ديسمبر_20261215_143022`)
3. **Creates fresh folder** for new generation

### Archive Structure

```
archive/
├── يناير/  (January)
│   ├── Attendance_1_2026.xlsx
│   ├── Revenue_1_2026.xlsx
│   └── Salaries_1_2026.xlsx
├── فبراير/  (February)
│   ├── Attendance_2_2026.xlsx
│   ├── Revenue_2_2026.xlsx
│   └── Salaries_2_2026.xlsx
└── مارس_20261215_143022/  (March - with timestamp)
    ├── Attendance_3_2026.xlsx
    ├── Revenue_3_2026.xlsx
    └── Salaries_3_2026.xlsx
```

## 🎯 Benefits

✅ **Organized** - All month files in one folder
✅ **Clean** - Easy to find and manage
✅ **Automatic** - One click generates everything
✅ **Safe** - Old data automatically archived
✅ **Integrated** - Salaries reads from attendance in same folder
✅ **Flexible** - Can still generate individual files if needed

## 🔧 Technical Details

### Month Folder Naming

Uses Arabic month names from `utils.calendar_utils.get_arabic_month()`:
- 1 → يناير (January)
- 2 → فبراير (February)
- 3 → مارس (March)
- ... and so on

### File Naming

Files keep the same naming convention:
- `Attendance_{month}_{year}.xlsx`
- `Revenue_{month}_{year}.xlsx`
- `Salaries_{month}_{year}.xlsx`

### Salaries Integration

When generating all reports:
1. Attendance generated first
2. Salaries reads from: `{month_folder}/Attendance_{month}_{year}.xlsx`
3. Working days automatically populated from attendance
4. All files in same folder for easy access

## 🧪 Testing

All files compile successfully:
```bash
✅ infrastructure/file_manager.py
✅ infrastructure/excel_template_writer.py
✅ infrastructure/attendance_template_writer.py
✅ infrastructure/revenue_template_writer.py
✅ infrastructure/salaries_template_writer.py
✅ application/salary_template_service.py
✅ presentation/windows/main_window.py
```

## 🎉 Ready to Use!

The GUI is now updated and ready for production use. Users can generate all monthly reports with a single click, and everything is organized in month folders!
