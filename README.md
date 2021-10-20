# Managing-Tournament
Application for managing a sporting tournament

The source data file should not contain a ranking table - this should be computed
by your application.

Create a new Python project. Make the source file part of the project. Load data from the file
to program memory. The source file may contain many statistical points about each match,
you just need the following:

– Date of the match

– Team names

– Score

Aggregate all results and make a ranking of teams. Add a separate file to your project that
shows the rules of the competition, which are especially important for breaking the ties (when
two or more teams score the same number of points). For example, the following rules are
used for the English Premier league ( source ):
If any clubs finish with the same number of points, their position in the Premier League table
is determined by goal difference, then the number of goals scored. If the teams still cannot be
separated, they will be awarded the same position in the table.

Make a simple request-response workflow for the user with the following functions:

– Show all matches of a given team

– Show matches played on a given date

– Show the ranking table (should be visualized as a true table with columns properly
aligned). The ranking table should contain the following columns:
*Ranking place - note, that this can be the same for several teams if the teams cannot
be separated

*Team name

*Number of games played

*Number of wins

*Number of draws

*Number of losses

*Goal difference

*Points

The exact indicators may differ depending on the chosen sport and tournament.

Extra task 1 (Multiple tournaments with the same ranking regulations):
3 points

Adjust your program in such a way that it loads data from multiple source files, each storing results
of 1 tournament. The rules for ranking teams within each tournament are the same and can be
hardcoded in your application.

The program should provide a 2-level menu. The top level menu is a selection of tournaments.
The inner menu is the same as in the basic task (3 functions)
