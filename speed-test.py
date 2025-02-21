import speedtest


st = speedtest.Speedtest()

#Get the best test server and set it
def server():
    best = st.get_best_server()
    return best

#Ping Speedtest
def ping():
    ping_ms = st.results.ping
    return ping_ms

#Download Speedtest
def download_test():
    download_speed = st.download()
    download_speed = download_speed / 1000000 #convert the bits into megabits
    return download_speed

#Upload Speedtest
def upload_test():
    upload_speed = st.upload()
    upload_speed = upload_speed / 1000000 #convert the bits into megabits
    return upload_speed

#Makes it so it can run separately
if __name__ == '__main__':

    print('Beginning Speedtest')
    print('-----' * 14, '\n')

    print('Scanning for best server...')
    print(f"Found:{server()['host']} located in {server()['country']}")

    print('\nStarting Speedtest...')
    print(f'\u001b[48;5;35m\u001b[38;5;255mPing: {ping()} ms\u001b[0m')
    print(f'\u001b[48;5;32m\u001b[38;5;255mDownload Speeds: {download_test():.2f} Mb/s\u001b[0m')
    print(f'\u001b[48;5;93m\u001b[38;5;255mUpload Speeds: {upload_test():.2f} Mb/s\u001b[0m')

    print('\nSpeed test done.')
    input('Press Enter to exit:')