#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
 Adapted from https://github.com/holman/spark

Module to create Sparklines

usage:
    import spark
    spark.spark( 1 , 2 , 3 , 4 , 5 )

'''

def spark( array = [] ):
    ticks = [ '▁' , '▂' , '▃' , '▄' , '▅' , '▆' , '▇' , '█' ]
    mymax = max( array )
    mymin = min( array )
    numer = (int( mymax ) - int( mymin ) ) << 8
    denom =  -1 + len(ticks)
    f = numer / denom
    output = []
    for a in array:
        n = int( a ) - int( mymin ) << 8
        t = n / f
        output.append( ticks[t] )
    return ('').join(output)

