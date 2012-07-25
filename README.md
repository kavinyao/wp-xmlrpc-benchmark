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
           start time: 2012-07-24 02:40:03.969915
             end time: 2012-07-24 02:41:01.760889
        good requests: 3000
         bad requests: 0
       total duration: 57.790974s
     average duration: 1.906461s
           throughput: 3114.673236 req/min

    [....Method Stats]
    wp.getPostStatusL: 1.211825s [  230reqs]
       wp.getTaxonomy: 1.214590s [  230reqs]
     wp.getTaxonomies: 1.244669s [  230reqs]
          wp.getTerms: 1.257016s [  230reqs]
    wp.getPostFormats: 1.280260s [  230reqs]
          wp.getPosts: 1.690162s [  461reqs]
       wp.getPostType: 1.762043s [  230reqs]
           wp.getPost: 1.763301s [  467reqs]
           wp.newPost: 3.299949s [  692reqs]

    [....Requests/30s]
    01[1418]: *****************************************************
    02[1582]: ************************************************************

## Dependency

The code depends on [Twisted](http://twistedmatrix.com/) and the dependency is specified in `requirements.txt`. You can use `pip install -r requirements.txt` to install packages required.

Use `virtualenv` and `pip` is highly recommended.
