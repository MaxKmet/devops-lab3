from flask import Flask, request, render_template
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = ""
QUEUE_NAME = ""

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('main_page.html')


@app.route('/receive_messages', methods=['POST'])
def receive_messages():
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    
    msg_list = []
    
    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                msg_list.append(str(msg))
                receiver.complete_message(msg)
            
    return render_template('message_list.html', msg_list=msg_list)



if __name__ == '__main__':
   app.run()
