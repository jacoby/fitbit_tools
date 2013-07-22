FitBit Tools
============

These are my tools and libraries, which I use to manage and interact with
the FitBit API. If you wish to use them, you will have to register a new
app and get credentials from dev.fitbit.com, which is not a difficult task.


Libraries
---------

These are libraries I use to deal with my FitBit data

-   fitbit.py - access to the FitBit API
-   mydb.py - store data locally so I don't abuse the API
-   pushover.py - alerting to my phone
-   spark.py - creating sparklines for Twitter and other social media

Configuration
-------------

I use YAML configuration files to keep from having to hardcode passwords
and tokens into my code. These files show format only.

-   fitbit.cnf
-   my.yaml
-   pushover.yml
-   fitbit.txt - description of the MySQL table I use to store my FitBit data. Not valid SQL.

Python
------

-   fitbit.battery.py - checks current battery level and alerts if not "high"
-   fitbit.date.py - full db download of FitBit data
-   fitbit.download.py - last few days of FitBit data to configure
-   fitbit.no_sync.py - check if my FitBit has sync'd in the last 3 days
-   fitbit.spark.py - outputs a sparkline showing the ups and downs of my last week's steps
-   fitbit.weight.py - uploads my weight via the FitBit API

RScript
-------

I use R to generate plots of my FitBit data. I'm including two RScripts
which run via crontab. My R is very remedial, and the plots could be made
much prettier with ggplot2 and similar libraries.

-   fb_floors_week.rs
-   fb_steps_week.rs

Copyright and License
---------------------

Copyright (c) 2013 Dave Jacoby (jacoby.david@gmail.com) and contributors

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
