CREATE TABLE computer (rowid INTEGER PRIMARY KEY, uni_name TEXT, major TEXT, degree TEXT(5), season TEXT(3), decision TEXT(15), decision_method TEXT(15), decision_date TEXT(10), decision_timestamp INTEGER, ugrad_gpa FLOAT, gre_verbal INTEGER, gre_quant INTEGER, gre_writing FLOAT, is_new_gre INTEGER, gre_subject INTEGER, status TEXT(28), post_date TEXT(10), post_timestamp INTEGER, comments BLOB);

.mode csv
.import cs_clean.csv computer


update computer set decision = NULL where decision="";
update computer set decision_method = NULL where decision_method="";
update computer set decision_date = NULL where decision_date="";
update computer set decision_timestamp = NULL where decision_timestamp="";
update computer set ugrad_gpa = NULL where ugrad_gpa="";
update computer set gre_verbal = NULL where gre_verbal="";
update computer set gre_quant = NULL where gre_quant="";
update computer set gre_writing = NULL where gre_writing="";
update computer set is_new_gre = NULL where is_new_gre="";
update computer set gre_subject = NULL where gre_subject="";
update computer set status = NULL where status="";
update computer set comments = NULL where comments="";
