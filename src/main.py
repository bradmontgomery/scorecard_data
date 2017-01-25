"""

This just rips a few bits of data out of the latest dataset (14-15 year)
and generates an HTML file.

HIGHDEG: Highest degree awarded

     0	Nondegreegranting
     1	Certificate degree
     2	Associate degree
     3	Bachelor's degree
     4	Graduate degree
INSTNM: Institution name

HCM2: Schools that are on Heightened Cash Monitoring 2 by the
      Department of Education
STABBR: State
CONTROL: Control of institution

     1	Public
     2	Private nonprofit
     3	Private forprofit

SAT_AVG: Average SAT equivalent score of students admitted

UGDS: Enrollment of undergraduate certificate/degreeseeking students

PCTPELL: Percentage of undergraduates who receive a Pell Grant

MEDIAN_HH_INC: Median household income

"""
import csv
from collections import defaultdict, Counter


# Column: number. We'll populate this from the first line of the CSV.
FIELDS = {
    'HIGHDEG': None,
    'INSTNM': None,
    'HCM2': None,
    'STABBR': None,
    'CONTROL': None,
    'SAT_AVG': None,
    'UGDS': None,
    'PCTPELL': None,
    'MEDIAN_HH_INC': None,
}

CONTROL = {
    1: 'Public',
    2: 'Private nonprofit',
    3: 'Private forprofit',
}


def main(file='data/CollegeScorecard_Raw_Data/MERGED2014_15_PP.csv'):
    lines_processed = 0
    results = defaultdict(dict)  # State -> School dict.

    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # read our heading positions
            if lines_processed == 0:
                for field in FIELDS.keys():
                    FIELDS[field] = row.index(field)
            else:
                state = row[FIELDS['STABBR']]
                name = row[FIELDS['INSTNM']]
                control = CONTROL.get(int(row[FIELDS['CONTROL']]))

                hideg = int(row[FIELDS['HIGHDEG']])
                inst_type = 'Community College' if hideg < 3 else "University"

                results[state][name] = {
                    'control': control,
                    'type': inst_type,
                    'average_sat': row[FIELDS['SAT_AVG']],
                    'students': row[FIELDS['UGDS']],
                    'pell_percent': row[FIELDS['PCTPELL']],
                    'median_income': row[FIELDS['MEDIAN_HH_INC']],
                    'monitored': row[FIELDS['HCM2']],
                }

            lines_processed += 1

    print("\n... {} lines of data processed".format(lines_processed))
    types = Counter()  # comm col. vs. university
    states = Counter()  # number of institutions in each state
    controls = Counter()  # number of whatever...
    students = 0

    # this is a giant hack
    with open("index.html", "w") as output_file:
        output = (
            "<html><body>"
            "<p>Menu: <a href='#states'>States</a> | "
            "<a href='#inst'>Institution Types</a> |"
            "<a href='#controls'>Controls</a></p>"
            "<table><thead><tr>"
            "<td>State</td>"
            "<th>Institution</th>"
            "<th>Control</th>"
            "<th>Type</th>"
            "<th>AVG SAT</th>"
            "<th>Degree-seeking students</th>"
            "<th>Percent Pell</th>"
            "<th>Med. Income</th>"
            "<th>Monitored</th>"
            "</tr><tbody>"
        )
        for state, data in results.items():
            for inst, details in data.items():
                controls[details['control']] += 1
                types[details['type']] += 1
                states[state] += 1
                try:
                    students += int(details['students'])
                except ValueError:
                    pass

                output += "<tr><td>{}</td><td>{}</td>".format(state, inst)
                output += "<td>{}</td>".format(details['control'])
                output += "<td>{}</td>".format(details['type'])
                output += "<td>{}</td>".format(details['average_sat'])
                output += "<td>{}</td>".format(details['students'])
                output += "<td>{}</td>".format(details['pell_percent'])
                output += "<td>{}</td>".format(details['median_income'])
                output += "<td>{}</td>".format(details['monitored'])
                output += "</tr>"
        output += "</tbody></table>"

        output += "<h2 id='students'>Students</h2><p>~{} total students</p>".format(students)
        output += "<h2 id='states'>States</h2>"
        output += "<table><thead><tr><th>State</th><th>Count</th></tr></thead><tbody>"
        for state, count in states.items():
            output += "<tr><td>{}</td><td>{}</td></tr>".format(state, count)
        output += "</tbody><table>"
        output += "<h2 id='inst'>Institution Types</h2>"
        output += "<table><thead><tr><th>Type</th><th>Count</th></tr></thead><tbody>"
        for inst, count in types.items():
            output += "<tr><td>{}</td><td>{}</td></tr>".format(inst, count)
        output += "</tbody></table>"

        output += "<h2 id='controls'>Controls</h2>"
        output += "<table><thead><tr><th>Type</th><th>Count</th></tr></thead><tbody>"
        for control, count in controls.items():
            output += "<tr><td>{}</td><td>{}</td></tr>".format(control, count)
        output += "</tbody></table>"
        output += "</body></html>"
        output_file.write(output)

    print("Finished writing report to ../index.html")


if __name__ == "__main__":
    main()
