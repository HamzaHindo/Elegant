I want to make a salaries excel writer with the following specs:
- The number of sections = the number of weeks 
- I am paying salaries Weeky
- Each week Has the following structure:
 - From B to J a big header of 1 row > "رواتب الموظفين عن شهر الاسبوع الاول"
 - B > "اسم الموظف" which is employee.name
 - C > "يوميه الموظف" which is employee.daily_rate
 - D > "عدد ايام العمل خلال الاسبوع" Total Working Hours/ith week, which you can find in attendance workbook in each total between the days
 - E > "الخصومات" Which is the punishments and it's just plain zeros as default
 - F > "عدد ايام العمل بعد الخصومات" D - E
 - G > "الراتب الاسبوعى" C * D This is total without punishments 
 - H > "الراتب الاسبوعي بعد الخصم" C * F This is total with punishments 
 - I > "سلف الموظف خلال الاسبوع" This we can get it from an outer table Let it 0 for now I will edit it
 - J > "نهائى الراتب المدفوع بعد خصم السلف" This is the final total which is H - I 

- Big Total Row at the button merged from B -> I and J cell is the total of all salaries

Rules:
- Make sure that You take the same approch in Styling which is makeing all cells without border except what we use
- Make sure to use the same color scheme 
- Make sure to use employees and stylists from the configuration 
- The salaries table is the same for both employees and stylists so put them in the same table 
- Make sure that the number of days in the first week matches the number of days in the Attendance's first week (week ends at sat regardless the start day)
- Create salary table for all weeks in the month and make a gap of 2 cells between each 

