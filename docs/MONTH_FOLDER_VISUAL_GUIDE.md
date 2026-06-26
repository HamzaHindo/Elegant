# Month Folder Structure - Visual Guide

## 📁 Complete Folder Structure

```
elegant/
├── output/
│   └── 2026/
│       ├── current/
│       │   └── ديسمبر/  ← Current month folder
│       │       ├── Attendance_12_2026.xlsx
│       │       ├── Revenue_12_2026.xlsx
│       │       └── Salaries_12_2026.xlsx
│       │
│       └── archive/
│           ├── يناير/  ← January (archived)
│           │   ├── Attendance_1_2026.xlsx
│           │   ├── Revenue_1_2026.xlsx
│           │   └── Salaries_1_2026.xlsx
│           │
│           ├── فبراير/  ← February (archived)
│           │   ├── Attendance_2_2026.xlsx
│           │   ├── Revenue_2_2026.xlsx
│           │   └── Salaries_2_2026.xlsx
│           │
│           └── نوفمبر_20261201_120000/  ← November (re-generated, timestamped)
│               ├── Attendance_11_2026.xlsx
│               ├── Revenue_11_2026.xlsx
│               └── Salaries_11_2026.xlsx
```

## 🔄 Generation Flow

### Step 1: User Clicks "Generate All Reports"

```
┌─────────────────────────────────────────┐
│  Year: 2026    Month: 12               │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Generate All Reports              │ │
│  │ (Attendance + Revenue + Salaries) │ │ ← Click here
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Step 2: System Checks for Existing Month Folder

```
Checking: output/2026/current/ديسمبر/

Case A: Folder doesn't exist
  → Create new folder
  → Generate files

Case B: Folder exists
  → Move to archive/ديسمبر/
  → Create new folder
  → Generate files

Case C: Folder exists AND archive/ديسمبر/ exists
  → Move to archive/ديسمبر_20261215_143022/  (with timestamp)
  → Create new folder
  → Generate files
```

### Step 3: Generate Files in Order

```
1. Generate Attendance
   ↓
   output/2026/current/ديسمبر/Attendance_12_2026.xlsx
   
2. Generate Revenue
   ↓
   output/2026/current/ديسمبر/Revenue_12_2026.xlsx
   
3. Generate Salaries (reads from Attendance in same folder)
   ↓
   output/2026/current/ديسمبر/Salaries_12_2026.xlsx
```

### Step 4: Success Message

```
┌─────────────────────────────────────────────────────┐
│  ✅ Success                                         │
│                                                     │
│  All reports generated successfully!                │
│                                                     │
│  Location: /home/user/output/2026/current/ديسمبر   │
│                                                     │
│  Files:                                             │
│  • Attendance_12_2026.xlsx                          │
│  • Revenue_12_2026.xlsx                             │
│  • Salaries_12_2026.xlsx                            │
│                                                     │
│  [OK]                                               │
└─────────────────────────────────────────────────────┘
```

## 📅 Month-by-Month Example

### January 2026

```
User generates reports for January
↓
output/2026/current/يناير/
├── Attendance_1_2026.xlsx
├── Revenue_1_2026.xlsx
└── Salaries_1_2026.xlsx
```

### February 2026

```
User generates reports for February
↓
January folder moved to archive
↓
output/2026/
├── current/
│   └── فبراير/  ← New current month
│       ├── Attendance_2_2026.xlsx
│       ├── Revenue_2_2026.xlsx
│       └── Salaries_2_2026.xlsx
└── archive/
    └── يناير/  ← Previous month archived
        ├── Attendance_1_2026.xlsx
        ├── Revenue_1_2026.xlsx
        └── Salaries_1_2026.xlsx
```

### March 2026

```
User generates reports for March
↓
February folder moved to archive
↓
output/2026/
├── current/
│   └── مارس/  ← New current month
│       ├── Attendance_3_2026.xlsx
│       ├── Revenue_3_2026.xlsx
│       └── Salaries_3_2026.xlsx
└── archive/
    ├── يناير/  ← January archived
    └── فبراير/  ← February archived
```

## 🔄 Re-generation Example

### User Re-generates March (Mistake Correction)

```
Before:
output/2026/
├── current/
│   └── مارس/  ← Existing March folder
│       ├── Attendance_3_2026.xlsx (with data)
│       ├── Revenue_3_2026.xlsx (with data)
│       └── Salaries_3_2026.xlsx (with data)
└── archive/
    ├── يناير/
    └── فبراير/

User clicks "Generate All Reports" for March again
↓
System detects existing March folder
↓
Moves to archive with timestamp

After:
output/2026/
├── current/
│   └── مارس/  ← Fresh March folder
│       ├── Attendance_3_2026.xlsx (empty)
│       ├── Revenue_3_2026.xlsx (empty)
│       └── Salaries_3_2026.xlsx (empty)
└── archive/
    ├── يناير/
    ├── فبراير/
    └── مارس_20261215_143022/  ← Old March with timestamp
        ├── Attendance_3_2026.xlsx (old data preserved)
        ├── Revenue_3_2026.xlsx (old data preserved)
        └── Salaries_3_2026.xlsx (old data preserved)
```

## 🎯 File Relationships

### Salaries Reads from Attendance

```
Month Folder: ديسمبر/
│
├── Attendance_12_2026.xlsx
│   │
│   │ Contains:
│   │ - Employee working days per week
│   │ - Week totals (نهاية الأسبوع)
│   │
│   └──────────────────┐
│                      │
│                      ↓ Reads from
│
├── Revenue_12_2026.xlsx (independent)
│
└── Salaries_12_2026.xlsx
    │
    │ Reads:
    │ - Employee names
    │ - Working days per week
    │ - Week structure
    │
    │ Calculates:
    │ - Weekly salaries
    │ - Deductions
    │ - Final pay
```

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Month Generation                     │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                   ↓
┌───────────────┐                  ┌───────────────┐
│  Attendance   │                  │   Revenue     │
│  Generated    │                  │   Generated   │
└───────┬───────┘                  └───────────────┘
        │
        │ Reads working days
        ↓
┌───────────────┐
│   Salaries    │
│   Generated   │
└───────────────┘
        │
        ↓
┌─────────────────────────────────────────────────────────┐
│  All 3 files in same folder: ديسمبر/                    │
│  - Attendance_12_2026.xlsx                              │
│  - Revenue_12_2026.xlsx                                 │
│  - Salaries_12_2026.xlsx                                │
└─────────────────────────────────────────────────────────┘
```

## 🗂️ Archive Timeline

```
Year 2026 Timeline:

Jan ──→ Feb ──→ Mar ──→ Apr ──→ May ──→ Jun
 │       │       │       │       │       │
 ↓       ↓       ↓       ↓       ↓       ↓
Archive Archive Archive Archive Archive Archive

current/: Always contains latest month
archive/: Contains all previous months

Example at end of June:
current/
└── يونيو/  ← June (current)

archive/
├── يناير/  ← January
├── فبراير/  ← February
├── مارس/  ← March
├── أبريل/  ← April
└── مايو/  ← May
```

## 🎨 Visual Comparison

### Old Way (Individual Files)

```
output/2026/current/
├── Attendance_12_2026.xlsx
├── Revenue_12_2026.xlsx
├── Salaries_12_2026.xlsx
├── Attendance_11_2026.xlsx  ← Mixed months
├── Revenue_11_2026.xlsx
└── Salaries_11_2026.xlsx

❌ Hard to find specific month
❌ Files mixed together
❌ No clear organization
```

### New Way (Month Folders)

```
output/2026/current/
└── ديسمبر/
    ├── Attendance_12_2026.xlsx
    ├── Revenue_12_2026.xlsx
    └── Salaries_12_2026.xlsx

archive/
└── نوفمبر/
    ├── Attendance_11_2026.xlsx
    ├── Revenue_11_2026.xlsx
    └── Salaries_11_2026.xlsx

✅ Easy to find specific month
✅ Files grouped by month
✅ Clear organization
✅ Automatic archiving
```

## 🚀 User Experience

### Before (3 separate clicks)

```
1. Click "Generate Attendance" → Wait → File created
2. Click "Generate Revenue" → Wait → File created
3. Click "Generate Salaries" → Select attendance file → Wait → File created

Total: 3 clicks + 1 file selection
```

### After (1 click)

```
1. Click "Generate All Reports" → Wait → All 3 files created in month folder

Total: 1 click
Time saved: ~70%
```

## 📝 Summary

✅ **One folder per month** - All related files together
✅ **Automatic archiving** - Old months preserved
✅ **Timestamp protection** - Re-generations don't lose data
✅ **Integrated workflow** - Salaries reads from attendance in same folder
✅ **Clean organization** - Easy to navigate and manage
✅ **One-click generation** - All reports at once
