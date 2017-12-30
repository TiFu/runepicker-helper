# Data Transformation

This module transforms data collected with the crawler into one database row
per participant.

# Using this module

Create your config in [./config](./config). Then use the [Makefile](./Makefile)
to download the necessary data and start transforming data.

By default it creates one million rows in the target database. If a different amount 
of rows should be used, check the [Makefile](./Makefile) to find out how the
[perkstyle/perkstyle.py](perkstyle/perkstyle.py) should be called.