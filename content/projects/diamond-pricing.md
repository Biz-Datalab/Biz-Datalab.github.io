# Pricing Diamonds with Real-World Market Data
How to edit: change the text after each colon. Sections start with "## ". Items in a section start with "- ".
In "Numbers", "Links", and "Student learning", the parts of an item are separated by " | ".

- type: group
- order: 2
- period: One semester · business analytics course
- status: Recurring course project
- image: projects/diamond-pricing/dashboard.png
- layout: charts
- label: Student project
- summary: Students learn business analytics hands-on with real-world diamond prices. They collect current natural diamond listings from online retailers for an assigned carat range, then clean the data and measure how price per carat changes with the 4Cs: carat, color, clarity, and cut. They also benchmark their prices against the Rapaport industry price list, compare natural with lab-grown stones, estimate a 95% confidence interval, and present the results in an interactive dashboard. The work shown here is from a student project on round, ideal-cut diamonds of 0.70 to 0.89 carat.

## Numbers
- intro: Results from a student project on natural, round, ideal-cut diamonds of 0.70 to 0.89 carat, built entirely from prices the students collected themselves.
- 56 | color and clarity combinations priced (8 colors × 7 clarity grades)
- 0.99 | R² for price per carat vs. color grade
- 30 | stones sampled for the confidence interval
- $3,992 ± $182 | 95% confidence interval for mean price per carat (D color, VVS1)
- 70–112% | student prices as a share of Rapaport list prices
- About 21% | lab-grown price per carat relative to natural (D color, VVS1)

## Student learning
- intro: The project takes students through the full analytics workflow on live market data, from finding the numbers to explaining them.
- Industry knowledge | Students learn how the 4Cs and grading reports from labs such as GIA and IGI set diamond value, and how the industry benchmarks prices.
- Data acquisition | Students collect prices and 4Cs grades from public retailer websites, by hand or with tools such as Python, Microsoft Power Automate, or Easy Scraper.
- Data preparation | They remove errors, duplicates, and irrelevant listings, fill gaps by extending the search, and calculate price per carat.
- Descriptive analytics | Pivot tables and heat maps show how price per carat moves across color and clarity grades, and how student prices compare with the Rapaport benchmark.
- Statistical inference | Students turn letter grades into numbers, fit regression lines with R², and build a 95% confidence interval from a 30-stone sample.
- Communication | Students build an interactive dashboard, presents in class in six minutes plus Q&A, and submits a final report with the raw data.

## Student work
### Domain knowledge: reading a diamond grading report
- text: Before collecting data, students build domain knowledge of the 4Cs. A grading report from a lab such as GIA shows the attributes behind every price: carat weight, color grade, clarity grade, and cut grade. Each listing students collect becomes one row with these same fields, plus price and price per carat.
- image: projects/diamond-pricing/gia-sample-report.jpg

### Data acquisition: raw price data
- text: Students recorded each stone's shape, price, carat, cut, color, and clarity from retailer listings, then calculated price per carat (price ÷ carat weight) so that stones of different sizes can be compared.
- image: projects/diamond-pricing/raw-data.png

### Pivot table: price per carat by color and clarity
- text: A pivot table of average price per carat for ideal-cut natural diamonds, with color grades D to K in rows and clarity grades IF to SI2 in columns. Prices fall steadily as color and clarity grades decline.
- image: projects/diamond-pricing/pivot-table.png

### Heat map: student prices vs. the Rapaport report
- text: Each cell shows the average collected price as a percentage of the Rapaport list price for the same grade. Most retail prices fall between 70% and 96% of the list price, and a few grades sit above it.
- image: projects/diamond-pricing/rapaport-heatmap.png

### Regression: price per carat vs. color and clarity
- text: Converting grades to numbers (D = 1 to K = 8; IF = 1 to SI2 = 7) lets students fit a trend line. Each step down in color lowers price per carat by about $270 (R² = 0.99). Each step down in clarity has a similar effect (R² = 0.96).
- image: projects/diamond-pricing/regression.png

### Confidence interval from a 30-stone sample
- text: For 30 D-color, VVS1, ideal-cut stones, the sample mean is $3,992 per carat with a standard deviation of $486. The 95% confidence interval runs from about $3,813 to $4,176 per carat.
- image: projects/diamond-pricing/confidence-interval.png

### Dashboard: natural vs. lab-grown
- text: The results come together in a Tableau dashboard comparing natural and lab-grown diamonds by color and clarity, with both heat maps and the confidence interval results. It shows that lab-grown stones sell for about a fifth of the natural price per carat.
- image: projects/diamond-pricing/dashboard.png

## For instructors
- This project can be adapted to other carat ranges, product categories, or courses. Detailed assignment instructions are available on request, and you are welcome to contact me.
