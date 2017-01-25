# College Scorecard info

View the results at [https://bradmontgomery.github.io/scorecard_data/](https://bradmontgomery.github.io/scorecard_data/)

___


This code pulls some (interesting) information from the
[college scorecard data set](https://catalog.data.gov/dataset/college-scorecard). (Note: the actual data is at [this link](https://catalog.data.gov/dataset/college-scorecard/resource/b8f3d10b-0974-40db-b5fa-3c87ecae516b)).

There's some [documentation](https://collegescorecard.ed.gov/data/documentation/),
but the interesting fields we're looking for are listed below. (See the
[CollegeScorecardDataDictionary.xlxs](https://collegescorecard.ed.gov/assets/CollegeScorecardDataDictionary.xlsx) file for more info).

- `HIGHDEG`: Highest degree awarded
    - 0	Non-degree-granting
    - 1	Certificate degree
    - 2	Associate degree
    - 3	Bachelor's degree
    - 4	Graduate degree
- `INSTNM`: Institution name
- `HCM2`: Schools that are on Heightened Cash Monitoring 2 by the Department of Education
- `STABBR`: State
- `CONTROL`: Control of institution
    - 1	Public
    - 2	Private nonprofit
    - 3	Private for-profit
- `SAT_AVG`: Average SAT equivalent score of students admitted
- `UGDS`: Enrollment of undergraduate certificate/degree-seeking students
- `PCTPELL`: Percentage of undergraduates who receive a Pell Grant
- `MEDIAN_HH_INC`: Median household income
