from kombu import Connection, Exchange, Queue


conn = Connection('amqp://test:test@192.168.161.56:5672//')
media_exchange = Exchange('media', 'direct', durable=True)

def process_media(body, message):
    print body
    message.ack()

# Consume from several queues on the same channel:
video_queue = Queue('video', exchange=media_exchange, key='video')
image_queue = Queue('image', exchange=media_exchange, key='image')

with conn.Consumer([video_queue, image_queue],
                         callbacks=[process_media]) as consumer:
    while True:
        conn.drain_events()
