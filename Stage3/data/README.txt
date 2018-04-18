Movie data have been extracted from two sources. Data corresponding to each source has been stored in separate table (in separate files).

Data Source 1: http://www.imdb.com/
Number of tuples: 3013
Attributes: MID,Title,Certificate,Genre,Rating,Running Time,Directors,Stars Cast,Country,Release Date,Production Company,Release Year,Release Month

Data Source 2: https://www.allmovie.com/
Number of tuples: 3300
Attributes: MID,Title,Certificate,Genre,Rating,Running Time,Directors,Stars Cast,Country,Release Date,Production Company,Release Year,Release Month

File Descriptions -

Table_IMDB_with_ID.csv - Table A contains data from Source 1.
Table_Allmovie_with_ID.csv - Table B contains data from Source 2.
Blocked_output.csv - lists all tuple pairs that survive the blocking step.  
Labelled_data_final.csv -  lists all tuple pairs in the sample we have taken, together with the labels
I_data.csv - Set I
J_data.csv - Set j
