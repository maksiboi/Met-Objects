## Team project

As an analyst, I need to be able to easily identify an analyze objects from the Met Museum departments.

I need to access that data quickly in Athena without having to use additional operations (e.g. without using unnest/extract functions if the source data contains fields structured as array/list).

* I want to get information on the most popular artworks over departments so I can create my marketing campaigns.
* I want to get information about departments with the highest count of objects/art so I can plan my budget accordingly.
* I want to get the number of art objects by department and accession year.


### Data Source?
Met Museum Public Dataset API https://metmuseum.github.io/

### Target table schema matches the source schema?
No

### Special handling required (i.e. hashing, obfuscation)?
Yes - name field (in constituents) must be hashed

### Data contains sensitive, restricted or PII data?
No

### Size of dataset?
A representative subset of 5 Met departments, at least 1000 random objects per department.

Departments:
* Greek and Roman Art
* Modern Art
* Ancient Near Eastern Art
* Arms and Armor
* The Robert Lehman Collection


### Target schema:
objectid
departmentid
departmentname
ishighlight
accessionnumber
accessionyear
ispublidomain
primaryimage
constituents
objectname
title
culture
period
dynasty
reign
objectdate
objectbegindate
objectenddate
medium
dimensions
measurements
geographytype
city
state
country
region
classification
metadatadate
repository
istimelinework
gallerynumber

### Acceptance criteria:

* Ingestion deployed as IAC
* Code approved and merged to master
* There's a Departments table with department ids and department name from all Met Museum departments.
* Columns constituents and measurements are exploded into separate columns in the final table.
* Queries approved and pushed to master which answer the three points from the description.
* Extra: API: After I make a call, I'm able to analyze data for the specific department.


# Notes:
* API requirements - keep request rate under 80 per second.
* Once you have the initial files in your buckets check the distribution of records by date to consider whether to include the date value in partitioning the parquet dataset.
