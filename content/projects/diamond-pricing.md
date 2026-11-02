# Pricing Diamonds with Real-World Market Data
How to edit: change the text after each colon. Sections start with "## ". Items in a section start with "- ".
This project uses the short "brief" layout: a summary, workflow steps, and a results gallery.
In "Workflow", the parts of an item are separated by " | ". In "Student work", add "- size: wide" to show an image full width.
"badge" sets the label color: funded (black), capstone (greenish grey), or student (grey).

- type: group
- label: Student project
- order: 2
- layout: brief
- badge: student
- image: projects/diamond-pricing/dashboard.png
- summary: Students learn business analytics hands-on with real-world diamond prices. Each student is assigned a carat range, collects current natural diamond listings from online retailers, and analyzes how price per carat changes with the 4Cs: carat, color, clarity, and cut. Results are benchmarked against the Rapaport industry price list and compared with lab-grown diamonds.

## Workflow
- Domain knowledge | Learn the 4Cs and how grading reports set diamond value.
- Data acquisition | Collect prices and grades from retailer websites.
- Data preparation | Clean the data and calculate price per carat.
- Analysis | Pivot tables, heat maps, regression, and a 95% confidence interval.
- Communication | Build a dashboard, present in class, and write a report.

## Domain knowledge
### Sample GIA grading report
- text: This is a sample grading report where the 4Cs data can be identified: carat weight, color grade, clarity grade, and cut grade. Each listing students collect becomes one row with these same fields.
- link: projects/diamond-pricing/gia-sample-report.jpg
- linktext: View the sample GIA report ↗

## Student work
- intro: These are a fraction of one student's raw dataset and visuals, from a project on round, ideal-cut diamonds of 0.70 to 0.89 carat.

### Raw data
- text: Price, carat, cut, color, and clarity for each stone, with price per carat calculated.
- image: projects/diamond-pricing/raw-data.png

### 95% confidence interval
- text: A 30-stone sample (D color, VVS1, ideal cut) gives a mean of about $3,992 per carat, with a 95% interval of about $3,813 to $4,176.
- image: projects/diamond-pricing/confidence-interval.png

### Price per carat by color and clarity
- text: Prices fall steadily as color and clarity grades decline.
- image: projects/diamond-pricing/pivot-table.png

### Student prices vs. the Rapaport report
- text: Most retail prices fall between 70% and 96% of the Rapaport list price.
- image: projects/diamond-pricing/rapaport-heatmap.png

### Regression on color and clarity
- text: Each step down in color or clarity lowers price per carat by about $270 (R² = 0.99 and 0.96).
- image: projects/diamond-pricing/regression.png
- size: wide

### Dashboard: natural vs. lab-grown
- text: Lab-grown stones sell for about a fifth of the natural price per carat.
- image: projects/diamond-pricing/dashboard.png
- size: wide

## For instructors
- This project can be adapted to other carat ranges, product categories, or courses. Detailed assignment instructions are available on request, and you are welcome to contact me.
