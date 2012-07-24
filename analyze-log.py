#!/bin/env python

import datetime
from collections import defaultdict

def date_from_string(date_repr):
    """
    date_repr should be repr(datetime.datetime)
    return a datetime.datetime object represented by date_repr
    """
    return datetime.datetime.strptime(date_repr, '%Y-%m-%d %H:%M:%S.%f')

def parse_log(log_file):
    """
    log_file should be the output of benchmark-xmlrpc.py
    return an unordered list like this:
    [(req_num, (start_time, end_time)), ...]
    """
    req_method_map = {}
    req_time_map = defaultdict(dict)
    for line in log_file:
        # since the delimiter is '/', can't use split direclty
        line = line.strip()
        date_repr, req_id, method, event = line.split('/')
        req_method_map[req_id] = method
        req_time_map[req_id][event] = date_from_string(date_repr)

    bad_reqs = [req_id for req_id in req_time_map.iterkeys() if len(req_time_map[req_id]) == 1]
    results = [(req_id, (req_method_map[req_id], d['start'], d['end'])) for req_id, d in req_time_map.iteritems() if req_id not in bad_reqs]
    return results, bad_reqs

def _seconds(start, end):
    """
    Calculate seconds from start to end with precision of microsecond.
    """
    delta = end - start
    return delta.seconds + delta.microseconds/1000000.0

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as log_file:
        results, bad_reqs = parse_log(log_file)

    start_time = results[0][1][1]
    end_time = results[0][1][2]
    durations = [] # measured in seconds
    method_durations = defaultdict(list)
    for req, info_tuple in results:
        method, start, end = info_tuple
        # find the earlist and latest time
        start_time = start_time if start_time < start else start
        end_time = end_time if end_time > end else end
        # calculate duration
        seconds = _seconds(start, end)
        durations.append(seconds)
        method_durations[method].append(seconds)

    print '[.........Summary]'
    print '       start time: %s' % start_time
    print '         end time: %s' % end_time

    num_requests = len(durations)
    print '    good requests: %d' % num_requests
    print '     bad requests: %d' % len(bad_reqs)

    total_duration = _seconds(start_time, end_time)
    print '   total duration: %.6fs' % total_duration

    avg_duration = sum(durations) / num_requests
    print ' average duration: %.6fs' % avg_duration

    minutes = total_duration / 60
    throughput = num_requests / minutes
    print '       throughput: %.6f req/min' % throughput

    # method statistics
    method_averages = [(method, sum(durations)/len(durations)) for method, durations in method_durations.iteritems()]
    method_averages.sort(key=lambda x: x[1])
    print '\n[....Method Stats]'
    for method, average in method_averages:
        # trim method name for display
        print '%17s: %.6fs' % (method[:17], average)

    # plot finished requests per 30 seconds
    req_stats = defaultdict(list)
    for req, time_pairs in results:
        time_offset = _seconds(start_time, time_pairs[1])
        index = int(time_offset) / 30
        req_stats[index].append(req)
    length = max(req_stats.keys()) + 1
    reqs_per_30s = [0] * length
    for index, reqs in req_stats.iteritems():
        reqs_per_30s[index] = len(reqs)
    max_number = max(reqs_per_30s)

    print '\n[....Requests/30s]'
    i = 1
    for req_number in reqs_per_30s:
        stars = '*' * (req_number*60 / max_number)
        print '%02d[%3d]: %s' % (i, req_number, stars)
        i += 1
