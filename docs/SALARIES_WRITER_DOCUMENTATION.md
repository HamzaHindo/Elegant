# Salaries Template Writer Documentation

## Overview

The `SalariesTemplateWriter` generates weekly salary sheets that automatically read attendance data and calculate salaries with deductions and advances.

## Features

✅ **Weekly Salary Sections** - One section per week in the month
✅ **Automatic Attendance Integration** - Reads working days from attendance Excel file
✅ **Comprehensive Calculations** - Handles deductions, advances, and final salaries
✅ **Professional Styling** - Uses the same Navy/Sky Blue color scheme
✅ **Clean Borders** - Only borders on used cells, matching other templates
✅ **Combined Employee List** - Includes both employees and stylists in the same table

## File Structure

```
domain/
  └── salary_template.py          # Domain model for salary data

infrastructure/
  └── salaries_template_writer.py # Excel writer for salary sheets
```

## Usage Example

```python
from domain.salary_template import SalaryTemplate
from infrastructure.salaries_template_writer import SalariesTemplateWriter

# Create salary template
template = SalaryTemplate(
    month=12,
    year=2026,
    employees=employees_list,
    stylists=stylists_list,
    attendance_file_path="./output/Attendance_12_2026.xlsx"
)

# Generate salary sheet
writer = SalariesTemplateWriter(output_directory="./output")
writer.write(template)

# Output: ./output/Salaries_12_2026.xlsx
```

## Excel Sheet Structure

### Week Section Layout

Each week has the following structure:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ رواتب الموظفين عن شهر ديسمبر - الأسبوع الأول                                │
│ [NAVY BACKGROUND - Merged B:J]                                              │
├────────┬──────────┬──────────┬─────────┬──────────┬─────────┬─────────┬─────┤
│ اسم    │ يومية    │ عدد أيام │ الخصومات│ عدد أيام │ الراتب  │ الراتب  │ سلف │
│ الموظف │ الموظف   │ العمل    │         │ العمل بعد│ الأسبوعي│ الأسبوعي│ الموظف│
│        │          │ خلال     │         │ الخصومات │         │ بعد الخصم│ خلال │
│        │          │ الأسبوع  │         │          │         │         │ الأسبوع│
├────────┼──────────┼──────────┼─────────┼──────────┼─────────┼─────────┼─────┤
│ Ahmed  │ 200      │ 5.5      │ 0       │ =D-E     │ =C*D    │ =C*F    │ 0   │
│ Mohamed│ 180      │ 6.0      │ 0       │ =D-E     │ =C*D    │ =C*F    │ 0   │
│ Sara   │ 220      │ 5.0      │ 0       │ =D-E     │ =C*D    │ =C*F    │ 0   │
├────────┴──────────┴──────────┴─────────┴──────────┴─────────┴─────────┴─────┤
│ إجمالي الرواتب للأسبوع [Merged B:I]                    │ =SUM(J:J)        │
└─────────────────────────────────────────────────────────────────────────────┘

[2 empty rows gap]

┌─────────────────────────────────────────────────────────────────────────────┐
│ رواتب الموظفين عن شهر ديسمبر - الأسبوع الثاني                               │
│ [Next week section...]                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

...

┌─────────────────────────────────────────────────────────────────────────────┐
│ إجمالي الرواتب للشهر بالكامل [Merged B:I]              │ =SUM(all weeks)  │
│ [NAVY BACKGROUND - Large Font]                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Column Definitions

| Column | Header | Formula/Value | Description |
|--------|--------|---------------|-------------|
| **B** | اسم الموظف | Employee name | Employee or stylist name |
| **C** | يومية الموظف | Daily rate | Daily rate from employee object |
| **D** | عدد أيام العمل خلال الأسبوع | From attendance | Working days read from attendance file |
| **E** | الخصومات | 0 (default) | Deductions/punishments (editable) |
| **F** | عدد أيام العمل بعد الخصومات | =D-E | Working days after deductions |
| **G** | الراتب الأسبوعي | =C*D | Weekly salary without deductions |
| **H** | الراتب الأسبوعي بعد الخصم | =C*F | Weekly salary with deductions |
| **I** | سلف الموظف خلال الأسبوع | 0 (default) | Employee advances (editable) |
| **J** | نهائي الراتب المدفوع بعد خصم السلف | =H-I | Final salary after advances |

## Attendance Data Integration

The writer automatically reads working days from the attendance Excel file:

1. **Locates the Attendance sheet** in the specified file
2. **Finds employee columns** by matching names in row 3
3. **Identifies week total rows** by looking for "نهاية الأسبوع" in column A
4. **Extracts working days** for each employee per week
5. **Handles missing data** gracefully (defaults to 0)

### Attendance File Requirements

- File must exist at the specified path
- Must have a sheet named "Attendance"
- Employee names in row 3 must match exactly
- Week totals must be marked with "نهاية الأسبوع" in column A

## Week Alignment

The salary weeks **match exactly** with the attendance weeks:

- Both use the same `get_weeks()` function from `utils.calendar_utils`
- Weeks end on Saturday regardless of start day
- First week may be partial (e.g., if month starts on Thursday)
- Number of weeks is identical in both files

## Styling Details

### Colors Used

- **Headers**: Navy background (`#1F3A5F`) + White text (`#FFFFFF`)
- **Totals**: Navy background (`#1F3A5F`) + White text (`#FFFFFF`)
- **Final Salary Column**: Sky Blue background (`#DCE6F1`)
- **Body Text**: Dark Gray (`#1F2937`)
- **Borders**: Black (`#000000`) - only on used cells

### Fonts

- **Headers**: Dubai 12pt Bold, White
- **Employee Names**: Dubai 11pt Bold, Dark Gray
- **Regular Data**: Dubai 11pt Regular, Dark Gray
- **Grand Total**: Dubai 22pt Bold, Navy

### Layout

- **RTL (Right-to-Left)**: Yes (for Arabic text)
- **Gridlines**: Hidden (only borders on used cells)
- **Freeze Panes**: Row 3 (keeps headers visible)
- **Column Widths**: Auto-adjusted for readability

## Editable Fields

Users can manually edit these fields after generation:

1. **Column E (الخصومات)** - Add deduction days
2. **Column I (سلف الموظف)** - Add advance amounts

All other columns will automatically recalculate based on formulas.

## Error Handling

The writer handles errors gracefully:

- **Missing attendance file**: Uses 0 for all working days
- **Missing employee in attendance**: Uses 0 for that employee
- **Invalid data in attendance**: Defaults to 0
- **Formula errors**: Excel will show #VALUE! (user can fix)

## Output File

- **Filename**: `Salaries_MM_YYYY.xlsx` (e.g., `Salaries_12_2026.xlsx`)
- **Location**: Specified output directory
- **Sheet Name**: "Salaries"

## Integration with Existing System

The salaries writer follows the same patterns as other writers:

✅ Inherits from `ExcelTemplateWriter`
✅ Uses `ExcelStyleManager` for all styling
✅ Uses `ExcelWorksheetHelper` for operations
✅ Uses `FileManager` for file handling
✅ Uses `get_weeks()` for week calculation
✅ Follows the same OOP structure

## Example Workflow

```python
# 1. Generate attendance sheet
attendance_template = AttendanceTemplate(...)
attendance_writer = AttendanceTemplateWriter()
attendance_writer.write(attendance_template)

# 2. Fill in attendance data manually

# 3. Generate salary sheet (reads from attendance)
salary_template = SalaryTemplate(
    month=12,
    year=2026,
    employees=employees,
    stylists=stylists,
    attendance_file_path="./output/Attendance_12_2026.xlsx"
)
salary_writer = SalariesTemplateWriter()
salary_writer.write(salary_template)

# 4. Review and edit deductions/advances if needed

# 5. Final salaries are calculated automatically
```

## Benefits

✅ **Automated Calculations** - No manual formula entry needed
✅ **Attendance Integration** - Working days pulled automatically
✅ **Error Prevention** - Formulas ensure consistency
✅ **Easy Editing** - Can adjust deductions and advances
✅ **Professional Output** - Matches company color scheme
✅ **Scalable** - Works with any number of employees/weeks

## Future Enhancements

Potential improvements:

- [ ] Support for different deduction types (late, absent, etc.)
- [ ] Advance tracking across weeks
- [ ] Overtime calculations
- [ ] Bonus/incentive columns
- [ ] Year-to-date totals
- [ ] Export to PDF
- [ ] Email distribution
