.mode csv
.import cs.csv computer
# remember to delete header row of CSV
create table computer (rowid TEXT, uni_name TEXT, major TEXT, degree TEXT, season TEXT, decision TEXT, decision_method TEXT, decision_date TEXT, decision_timestamp TEXT, ugrad_gpa TEXT, gre_verbal TEXT, gre_quant TEXT, gre_writing TEXT, is_new_gre TEXT, gre_subject TEXT, status TEXT, post_date TEXT, post_timestamp TEXT, comments BLOB);

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

