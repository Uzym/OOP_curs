import os
from filter_overlay import FilterOverlay
import s3_handler
import json

import pika
import logging

amqp_url = os.environ["AMQP_URL"]
conn_params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel2 = connection.channel()

channel.queue_declare(queue='first')
channel.queue_declare(queue='second')

def get_request(chat_id, outp_path):
    return {
        "chat_id": chat_id,
        "outp_path": outp_path
    }

filterOverlay = FilterOverlay()
s3handler = s3_handler.s3Handler()
input_path = 'input/'
output_s3_path = 'output/'

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def json_deserializer(m):
    return json.loads(m.decode('utf-8'))

def callback(ch, method, properties, body):
    input = json_deserializer(body)
    logging.info(input)
    s3handler.download(input_path + input['name'] + '.jpg')
    outp_path = filterOverlay.get_path(input['name'], input['filter'])
    s3handler.upload(outp_path)
    req = get_request(input['chat_id'], output_s3_path +  outp_path.split('/')[-1])
    logging.info(req)
    req = json_serializer(req)
    channel2.basic_publish(exchange='', routing_key='second', body=req)       
    os.remove(outp_path)
    os.remove(input_path + input['name'] + '.jpg')

def main():
    channel.basic_consume(queue='first', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()
    
