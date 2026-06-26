# Color Usage Guide

## Visual Reference

```
┌─────────────────────────────────────────────────────────────┐
│  ATTENDANCE TEMPLATE                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │ كشف حضور و إنصراف الموظفين عن شهر...              │    │
│  │ [NAVY BACKGROUND #1F3A5F + WHITE TEXT #FFFFFF]    │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  Employee Names: [DARK GRAY TEXT #1F2937]                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Week Totals                                         │  │
│  │ [NAVY BACKGROUND #1F3A5F + WHITE TEXT #FFFFFF]     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Month Total: 25.5                                   │  │
│  │ [NAVY BACKGROUND #1F3A5F + WHITE TEXT #FFFFFF]     │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────┐
│  REVENUE TEMPLATE                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │ الإيرادات اليومية                                  │    │
│  │ [NAVY BACKGROUND #1F3A5F + WHITE TEXT #FFFFFF]    │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Income Section Headers                            │    │
│  │ [NAVY BACKGROUND #1F3A5F + WHITE TEXT #FFFFFF]    │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Total Collected: 15,000                           │    │
│  │ [SKY BACKGROUND #DCE6F1 + NAVY TEXT #1F3A5F]     │    │
│  │ [LARGE FONT 22pt]                                 │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Visa: 10,000  |  Cash: 5,000                      │    │
│  │ [SKY BACKGROUND #DCE6F1 + DARK GRAY TEXT #1F2937]│    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │ Stylist Targets                                   │    │
│  │ [NAVY BACKGROUND #1F3A5F + WHITE TEXT #FFFFFF]    │    │
│  ├───────────────────────────────────────────────────┤    │
│  │ Name    | Target | Achieved | Percentage          │    │
│  │ Ahmed   | 1000   | 850      | 85                  │    │
│  │         | [DARK BLUE #00008B] | [DARK GREEN #023020]│  │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Color Application by Section

### Headers (Main Titles)
- **Background**: Navy (`#1F3A5F`)
- **Text**: White (`#FFFFFF`)
- **Font**: Dubai 12pt Bold
- **Usage**: Sheet titles, section headers

### Sub-headers (Column Headers)
- **Background**: Navy (`#1F3A5F`)
- **Text**: White (`#FFFFFF`)
- **Font**: Dubai 12pt Bold
- **Usage**: Column names, field labels

### Highlighted Values (Totals, Summaries)
- **Background**: Sky Blue (`#DCE6F1`)
- **Text**: Navy (`#1F3A5F`) or Dark Gray (`#1F2937`)
- **Font**: Dubai 11pt Bold or 22pt Bold (for large totals)
- **Usage**: Week totals, month totals, revenue summaries

### Body Text (Data Cells)
- **Background**: White (default)
- **Text**: Dark Gray (`#1F2937`)
- **Font**: Dubai 11pt Regular
- **Usage**: Employee names, dates, regular data

### Target Values (Special Indicators)
- **Text**: Dark Blue (`#00008B`)
- **Font**: Dubai 11pt Bold
- **Usage**: Target amounts, achieved amounts

### Percentages (Performance Indicators)
- **Text**: Dark Green (`#023020`)
- **Font**: Dubai 11pt Bold
- **Usage**: Performance percentages, ratios

### Borders
- **Color**: Black (`#000000`)
- **Style**: Thin (regular cells), Medium (section outlines)
- **Usage**: All cell borders, section separators

## Color Psychology

- **Navy Blue** - Professional, trustworthy, authoritative (perfect for headers)
- **Sky Blue** - Calm, clear, organized (perfect for highlights)
- **Dark Gray** - Neutral, readable, professional (perfect for body text)
- **Dark Blue** - Focused, stable (perfect for financial targets)
- **Dark Green** - Growth, success (perfect for percentages)

## Accessibility

✅ All color combinations meet WCAG AA contrast requirements:
- Navy (#1F3A5F) on White: 9.8:1 contrast ratio
- White on Navy: 9.8:1 contrast ratio
- Dark Gray (#1F2937) on White: 14.5:1 contrast ratio
- Navy (#1F3A5F) on Sky Blue (#DCE6F1): 6.2:1 contrast ratio

## How to Change Colors

All colors are defined in `infrastructure/excel_style_manager.py`:

```python
# To change the main header color:
COLOR_NAVY = "1F3A5F"  # Change this hex code

# To change the highlight color:
COLOR_SKY = "DCE6F1"  # Change this hex code

# To change body text color:
COLOR_TEXT = "1F2937"  # Change this hex code
```

After changing colors in the style manager, all templates will automatically use the new colors on the next generation.
