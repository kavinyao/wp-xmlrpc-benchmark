# wp-xmlrpc-benchmark

This is a home-built tool for benchmarking WordPress XML-RPC and analyzing results.

## Usage

1. Make a benchmark configuration. You can refer to sample-config.py as a skeleton.
1. Run benchmark with `python benchmark-xmlrpc.py config-file.py concurrent_requests total_requests`.
    * Example: `python benchmark-xmlrpc.py site-1-config.py 100 5000`
    * A log file in the format `log[con_req]-[total_req]-[month]-[day]-[hour]:[minute]:[second]` will be generated.
1. Analyze log with `python analyze-log.py log_file`.

## Dependency

The code depends on [Twisted](http://twistedmatrix.com/) and the dependency is specified in `requirements.txt`. You can use `pip install -r requirements.txt` to install packages required.

Use `virtualenv` and `pip` is highly recommended.
