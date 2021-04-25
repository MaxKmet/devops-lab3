from flask import Flask, request, render_template
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = ""
QUEUE_NAME = ""

app = Flask(__name__)

def send_single_message(sender, msg):
    message = ServiceBusMessage(msg)
    sender.send_messages(message)

@app.route("/")
def main_page():
    return render_template('main_page.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    
    msg = str(request.form['msg'])

    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            send_single_message(sender, msg)
            
    return render_template('main_page.html')



if __name__ == '__main__':
   app.run()
