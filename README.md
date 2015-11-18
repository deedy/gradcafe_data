# Gradcafe Data

cs/ - Contains all results with the query "computer*" - 27,822 results

### Schema


The schema of the `all.csv` file which contains all the content on GradCafe and the `allgrad` table in `all.sql` is:

| Column Name        | Type                | Description                                                                                                                                                                                                  |
|--------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rowid              | INTEGER PRIMARY KEY | A unique integer ID identifying the row. There are 271,807 rows.                                                                                                                                                                      |
| uni_name           | TEXT                | The name of the university. The uncleaned field is user-supplied, and very noisy, containing 10,297 distinct strings. The cleaned version reduces this number to 527.                                                                                                                                    |
| major              | TEXT                | The intended major. This field isn't cleaned and is user-supplied and also noisy. It contains 18,957 distinct strings, the most common of which are "Computer Science", "Economics" and "English".                                                          |
| degree             | TEXT(5)             | The degree to be earned. This field is cleaned and takes the following values: "PhD", "MS", "MEng", "MBA", "MFA", "MA", and "Other". The top 3 are "PhD", "MS" and "Other".                                                                               |
| season             | TEXT(3)             | The season is a three letter string of the form [SF][0-9]{2}. "S" is for admission into the Spring semester and "F" represents Fall. The two numbers represent the year for which admission is being sought. |
| decision           | TEXT(15)            | The decision being reported. This field takes the following values: "Accepted", "Rejected", "Wait listed", "Interview" and "Other".                                                                          |
| decision_method    | TEXT(15)            | The method in which the decision was reported. The field takes the following values: "E-mail", "Website", "Phone", "Postal Service" and "Other".                                                             |
| decision_date      | TEXT(10)            | The date the decision was made in the form "dd-mm-yyyy".                                                                                                                                                     |
| decision_timestamp | INTEGER             | The timestamp since epoch that the decision was made.                                                                                                                                                        |
| ugrad_gpa          | FLOAT               | The candidate's self-reported undergraduate GPA. Typically on a 4.0 scale, but often scores on 10.0 scales are reported with no clear disambiguation.                                                        |
| gre_verbal         | INTEGER             | The candidate's self-reported GRE Verbal score. If `is_new_gre` is 1, this field should be between 130 and 170 inclusive. If 0, then it should be between 200 and 800 exclusive.                             |
| gre_quant          | INTEGER             | The candidate's self-reported GRE Quantitative score. If `is_new_gre` is 1, this field should be between 130 and 170 inclusive. If 0, then it should be between 200 and 800 exclusive.                       |
| gre_writing        | FLOAT               | The candidate's self-reported GRE Writing score. It is on a scale of 0.0 to 6.0.                                                                                                                             |
| is_new_gre         | INTEGER             | Whether or not the candidate took the new GRE examination (where scores range from 130 to 170) or not.                                                                                                       |
| gre_subject        | INTEGER             | The candidate's self-reported GRE Subject Test score. It can range in the 900s. Presumably, given that this is a CS dataset, I'd assume the subject in question is Computer Science.                         |
| status             | TEXT(28)            | The status of the candidate. Can take on 4 different values - "American", "International", "International with US degree" and "Other".                                                                       |
| post_data          | TEXT(10)            | The date on which this report was posted by the candidate in the form "dd-mm-yyyy".                                                                                                                          |
| post_timestamp     | INTEGER             | The timestamp since epoch that the post was made.                                                                                                                                                            |
| comments           | BLOB                | All user added comments to the post he submitted


The schema of the `cs.csv` file, which contain all results that have word beginning with "computer", and the `computer` table in `cs.sql` is:

| Column Name        | Type                | Description                                                                                                                                                                                                  |
|--------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rowid              | INTEGER PRIMARY KEY | A unique integer ID identifying the row                                                                                                                                                                      |
| uni_name           | TEXT                | The name of the university. The uncleaned field is user-supplied, and very noisy, containing 2325 distinct strings. The cleaned version reduces this number to 415.                                                                                                                                     |
| major              | TEXT                | The intended major. This field is cleaned and takes the following values: "CS", "ECE", "HCI", "IS" and "Other".                                                                                              |
| degree             | TEXT(5)             | The degree to be earned. This field is cleaned and takes the following values: "PhD", "MS", "MEng", "MBA", "MFA" and "Other".                                                                                |
| season             | TEXT(3)             | The season is a three letter string of the form [SF][0-9]{2}. "S" is for admission into the Spring semester and "F" represents Fall. The two numbers represent the year for which admission is being sought. |
| decision           | TEXT(15)            | The decision being reported. This field takes the following values: "Accepted", "Rejected", "Wait listed", "Interview" and "Other".                                                                          |
| decision_method    | TEXT(15)            | The method in which the decision was reported. The field takes the following values: "E-mail", "Website", "Phone", "Postal Service" and "Other".                                                             |
| decision_date      | TEXT(10)            | The date the decision was made in the form "dd-mm-yyyy".                                                                                                                                                     |
| decision_timestamp | INTEGER             | The timestamp since epoch that the decision was made.                                                                                                                                                        |
| ugrad_gpa          | FLOAT               | The candidate's self-reported undergraduate GPA. Typically on a 4.0 scale, but often scores on 10.0 scales are reported with no clear disambiguation.                                                        |
| gre_verbal         | INTEGER             | The candidate's self-reported GRE Verbal score. If `is_new_gre` is 1, this field should be between 130 and 170 inclusive. If 0, then it should be between 200 and 800 exclusive.                             |
| gre_quant          | INTEGER             | The candidate's self-reported GRE Quantitative score. If `is_new_gre` is 1, this field should be between 130 and 170 inclusive. If 0, then it should be between 200 and 800 exclusive.                       |
| gre_writing        | FLOAT               | The candidate's self-reported GRE Writing score. It is on a scale of 0.0 to 6.0.                                                                                                                             |
| is_new_gre         | INTEGER             | Whether or not the candidate took the new GRE examination (where scores range from 130 to 170) or not.                                                                                                       |
| gre_subject        | INTEGER             | The candidate's self-reported GRE Subject Test score. It can range in the 900s. Presumably, given that this is a CS dataset, I'd assume the subject in question is Computer Science.                         |
| status             | TEXT(28)            | The status of the candidate. Can take on 4 different values - "American", "International", "International with US degree" and "Other".                                                                       |
| post_data          | TEXT(10)            | The date on which this report was posted by the candidate in the form "dd-mm-yyyy".                                                                                                                          |
| post_timestamp     | INTEGER             | The timestamp since epoch that the post was made.                                                                                                                                                            |
| comments           | BLOB                | All user added comments to the post he submitted
