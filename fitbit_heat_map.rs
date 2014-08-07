#!/usr/bin/env Rscript

# This uses ggplot2 to create a heatmap of your FitBit steps. It is 
# personalized to me, with my MySQL server and file system named. 
# Pulling those details out is my intention.

# RMySQL connects you to MySQL relational database for data storage;
#   connections to other tools are available should you want to use them.
# yaml is used to store configuration information for the MySQL database
#   so it isn't necessary to hard-code passwords and such
# ggplot2 is the current cream of the plotting crop within Rstat.
# By default, R uses X11 to draw images, but when used on machines without
#   X servers, or via crontab (most of my R work is run via crontab), this
#   you need to use the Cairo 2D graphics library.

suppressPackageStartupMessages( require( "RMySQL"  , quietly=TRUE ) )
suppressPackageStartupMessages( require( "Cairo"   , quietly=TRUE ) )
suppressPackageStartupMessages( require( "yaml"    , quietly=TRUE ) )
suppressPackageStartupMessages( require( "ggplot2" , quietly=TRUE ) )

my.cnf = yaml.load_file( '~/.my.yaml' )
database = my.cnf$clients$itap
quote       <- "'"
newline     <- "\n"

steps_sql <- "
SELECT 
    steps steps ,
    YEAR( datestamp ) year,
    WEEK( datestamp ) week ,
    IF(
        WEEKDAY( datestamp ) > 5 ,
        1 ,
        2 + WEEKDAY( datestamp ) 
        ) wday ,
    DATE( datestamp ) date 
FROM fitbit_daily 
GROUP BY DATE(datestamp)
ORDER BY DATE(datestamp)
    "
digits_week  <- c( 1, 2, 3, 4, 5, 6, 7 ) 
days_of_week <- c( "S","M","T","W","T","F","S" ) 

con <- dbConnect(
    MySQL(),
    user=database$user ,
    password=database$password,
    dbname=database$database,
    host=database$host
    )

steps.data  <- dbGetQuery( con , steps_sql )

# print steps.data

CairoPNG(
    filename    = "/home/jacoby/www/fitbit_heatmap.png" ,
    width       = 800  ,
    height      = 600  ,
    pointsize   = 12
    )
ggplot(
    steps.data, 
    aes( week, wday, fill = steps )
    ) +
geom_tile(colour = "#191412") +
ggtitle( "Dave Jacoby's FitBit Steps" ) +
xlab( 'Week of the Year' ) +
ylab( 'Day of the Week' ) +
scale_y_continuous( breaks=digits_week , labels=days_of_week ) +
scale_fill_gradientn(
    colours = c(
        "#ffffff",
        "#999999",
        "#a68ffd",
        "#3d0afa",
        "#ff5060"
        )
    ) +
facet_wrap(~ year, ncol = 1) 

