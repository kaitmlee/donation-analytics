This was written for the Insight Data Engineering coding challenge. More info [here](https://github.com/InsightDataScience/donation-analytics).

## Dependencies
- **python:** 3.5.2
- **pandas:** 0.17.1

## Description
To run this program just use the bash script, run.sh.

There are two input files, itcont.txt and percentile.txt in the input directory. itcont.txt has information on individual donors to political candidates on each line while percentile.txt can be changed to calculate the nth percentile of donation amounts.

The output file is called repeat_donors.txt. The output is the recipient id, zipcode of donor, year of donation, running percentile of contributions streamed in so far with same year and zipcode, total amount of contributions so far from the same zipcode and year, and the total number of contributions streamed in so far from the same zipcode and year. Sepearated by "|". This program only considered repeat donors so if a donor only contributed once then they were not considered for further analysis.

## Approach
As the data is being 'streamed in' it is added to a pandas dataframe and cleaned up. Any rows with essential missing or malformed data is dropped. Then unique donors are found and added to a list, and there is also a check to see if the donation information was streamed in the wrong order. First time donations are dropped from the dataframe, but remain on the unique donors list. If a repeat donor is found then the row index is sent to another function that calculates and finds the neccessary information for the output.

I chose to use a pandas dataframe because it's functionality makes this type of running analysis very simple and easy to use.


## Assumptions
- I assumed that the sum of the contributions would be rounded to the nearest dollar the same way the percentile amount was.
- A donor was only considered a repeat donor if they donated in a previous year, and all donations from the earliest year are not considered.
