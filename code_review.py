#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:19:34 2020

@author: hassanpasha
"""

def combine_availabilities(avails):
    #sorting the given list by thex tuple 
    sorted_by_start_ts = sorted(avails, key=lambda x: x[0])

    ranges = []
    earliest_start, latest_end = None, None
    
    for (start, end) in sorted_by_start_ts:
        
        print(start,end)
        
        if earliest_start is None or latest_end is None:
            earliest_start, latest_end = (start, end)
            continue
        #Question : Why put an assert mid code, wouldn't a  try and except work better
        assert earliest_start <= start

        # Interval looks like (       )   [    ] - no overlap
        if latest_end < start:
            ranges.append((earliest_start, latest_end))
            earliest_start, latest_end = (start, end)
            continue

        # Interval looks like (       [   )    ] - has overlap
        elif latest_end >= start:
            latest_end = max(latest_end, end)
            continue
    # this handles end of list statment 
    if (earliest_start, latest_end) != (None, None):
        ranges.append((earliest_start, latest_end))
    # return list 
    return ranges


if __name__ == "__main__":
    print(combine_availabilities( avails = [(1, 7), (0, 5), (10, 15)]  )   )
