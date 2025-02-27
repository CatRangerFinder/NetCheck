from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Gauge, generate_latest
import speed_test
import time

##System config##
server_name = str('server-a')


app = Flask(__name__)
download_speed = speed_test.download_test()
upload_speed = speed_test.upload_test()

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


#Download speed metric label
current_download_rate_locally = Gauge(
    'current_download_rate_locally',
    'The current rated download speeds, its a gauge.',
    ['server_name']
)

#Upload speed metric label
current_upload_rate_locally = Gauge(
    'current_upload_rate_locally',
    'The current rated upload speeds, its a gauge.',
    ['server_name']
)


#Location for prometheus to scrape the metrics
@app.route('/metrics', methods=['GET'])
def metrics_page():
    start_pull_time = time.time()

    #Network data for prometheus
    start_speed_time = time.time()
    speed_test.best_server()
    current_download_rate_locally.labels(server_name).set(round(download_speed, 3))
    print(f'METRICS_LOG: download_speed= {download_speed} Mb/s')
    current_upload_rate_locally.labels(server_name).set(round(upload_speed, 3))
    print(f'METRICS_LOG: upload_speed= {upload_speed} Mb/s')
    end_speed_time = time.time()


    #Logs section uncomment out this section and all "start_*_time" parts to enable logs in the console
    time_spent_speed = (end_speed_time - start_speed_time)
    print(f'TIME_LOG: Time to process speedtest: {time_spent_speed:.3f} seconds')

    #Final time logger for the request
    end_pull_time = time.time()
    time_spent_pull = (end_pull_time - start_pull_time)
    print(f'TIME_LOG: Time to process metric pull: {time_spent_pull:.3f} seconds')

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


#Home page just case its needed later
@app.route('/')
def home_page():
    response = jsonify(testing='prometheus_metrics add: /metrics')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)