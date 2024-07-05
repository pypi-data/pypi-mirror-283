from google.cloud import pubsub_v1


def get_producer(project_id: str, topic_id: str):
    producer = pubsub_v1.PublisherClient()
    topic_path = producer.topic_path(project_id, topic_id)

    return producer, topic_path


def send_msg(data: str, publisher, topic_path: str):

    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
        
    return publish_future
