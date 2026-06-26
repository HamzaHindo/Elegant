### I want to add an extra sheet in revenue workbook, total borrows in the month for each emp/stylist It will have the following structure
- The same header in attendance sheet with date taking 2 rows(B2, B3) and Row 3 col starting from C having emp/stylists name
- The same days in the side (col B) end the week at every sat like what did in attendance sheet 

### Or in another words clone the attendance table in total borrows and put it as a sheet in revenue workbook but remove all formulas except the tatal borrows in each week let it calculate all cells above it in the same week  and a one big total at the end of the month.


Rules:
Stick to the styles used in styles manager
Stick to emp/stylists in config 
Do not change any of exsiting code for any sheet just create the new one and work in it 


great work, Some small changes
- Merge the two cols A and B in each row you will find two types of rows (Day row, Total row)
    - In day row just merge 
    - In total merge and remove the data in colB

At the end add a Big 2 rows to take all the space with total borrows for all emp/stylists
