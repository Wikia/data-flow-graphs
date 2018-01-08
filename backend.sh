#!/bin/bash
# @see https://gist.github.com/macbre/0e176d667f79ab1124b85e3a389c7df8
query_digest --last-24h --data-flow --table events_local_users
#query_digest --last-24h --data-flow --table multilookup
#query_digest --last-24h --data-flow --table phalanx_stats
query_digest --last-24h --data-flow --database stats
