# wp-xmlrpc-benchmark

This is a home-built tool for benchmarking WordPress XML-RPC and analyzing results.

## Usage

1. Make a benchmark configuration. You can refer to `sample-config.py` as a skeleton.
1. Run benchmark with `python benchmark-xmlrpc.py config-file.py concurrent_requests total_requests [log_file]`.
    * Example: `python benchmark-xmlrpc.py site-1-config.py 100 5000`
    * Request data are written to log files. If the file name is not specified, a log file in the format `log[con_req]-[total_req]-[month]-[day]-[hour]:[minute]:[second]` will be generated
    * Errors will be logged to a file with name `{log_file}-error`
1. Analyze log with `python analyze-log.py log_file`.

The analysis report is like:

    [.........Summary]
           start time: 2012-07-25 09:57:32.371788
             end time: 2012-07-25 10:02:56.258678
         success rate: 99.060% [9906/10000]
       total duration: 323.886890s
     average duration: 3.177937s
           throughput: 1835.085082 req/min

    [....Method Stats]
    wp.getPostFormats: 1.473392s [  769reqs]
           wp.getPost: 1.540098s [ 1447reqs]
    wp.getPostStatusL: 1.553953s [  769reqs]
       wp.getPostType: 1.866592s [  769reqs]
          wp.getTerms: 2.137198s [  769reqs]
       wp.getTaxonomy: 2.175794s [  769reqs]
          wp.getPosts: 2.317214s [ 1538reqs]
     wp.getTaxonomies: 2.514145s [  769reqs]
           wp.newPost: 7.227887s [ 2307reqs]

    [....Requests/30s]
    01[1707]: ******************************************************
    02[1360]: *******************************************
    03[ 452]: **************
    04[ 428]: *************
    05[ 435]: *************
    06[ 377]: ************
    07[ 371]: ***********
    08[ 951]: ******************************
    09[1865]: ************************************************************
    10[1257]: ****************************************
    11[ 703]: **********************

## Dependency

The code depends on [Twisted](http://twistedmatrix.com/) and the dependency is specified in `requirements.txt`. You can use `pip install -r requirements.txt` to install packages required.

Use `virtualenv` and `pip` is highly recommended.
