import datetime
import json
import socket
import time
import urllib.request

CARBON_SERVER = '10.1.7.45'  # grafana/graphite/carbon server
CARBON_PORT = 2003
carbon_db = ''

serverList = ['http://127.0.0.1:8080']

# function: read today's collected count
def readMetricTodayCount(serverMetricsUrl1,todayHuman1):
    fullMetricsUrl = serverMetricsUrl1 + "?tag=day:" + todayHuman1
    try:
        collectedCount = json.loads(urllib.request.urlopen(fullMetricsUrl, None, 30).read())
        logNum = collectedCount['measurements'][0]['value']
        return logNum
    except:
        return 0

# main function
sock = socket.socket()
sock.connect((CARBON_SERVER, CARBON_PORT))
metrics_ary = []

for server in serverList:
    serverMetricsUrl = ''
    # format to http-127-0-0-1-8080
    graphiteServerMetricsUrl = server.replace('://', '-').replace(':', '-')
    if server.endswith('/'):
        serverMetricsUrl = server + 'monitor/metrics'
        graphiteServerMetricsUrl = graphiteServerMetricsUrl.replace('.', '-').replace('/', '')
    else:
        serverMetricsUrl = server + '/monitor/metrics'
        graphiteServerMetricsUrl = graphiteServerMetricsUrl.replace('.', '-')
    todayHuman = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d')
    hellWorldCallCountMetricsReqUrl = serverMetricsUrl + "/test"
    hellWorldCallSuccessCount = readMetricTodayCount(hellWorldCallCountMetricsReqUrl,todayHuman)
    print(hellWorldCallCountMetricsReqUrl)
    print(hellWorldCallSuccessCount)
    graphiteKeyPullOpmTaskRunSuccessCountToday = carbon_db + "helloworld.success.count." + graphiteServerMetricsUrl + ".today"
    graphiteKeyPullOpmTaskRunSuccessCountDay = carbon_db + "helloworld.success.count." + graphiteServerMetricsUrl + "." + todayHuman
    ts = int(round(time.time()))
    metrics_ary.append('%s %s %d' % (graphiteKeyPullOpmTaskRunSuccessCountToday, hellWorldCallSuccessCount, ts))
    metrics_ary.append('%s %s %d' % (graphiteKeyPullOpmTaskRunSuccessCountDay, hellWorldCallSuccessCount, ts))
msg = '\n'.join(metrics_ary) + '\n'
#print(msg)
sock.sendall(msg.encode())
sock.close()