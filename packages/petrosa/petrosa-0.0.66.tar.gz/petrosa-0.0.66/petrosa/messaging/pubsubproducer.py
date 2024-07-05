from google.cloud import pubsub_v1


def send_msg(data: str, project_id: str, topic_id: str):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
        
    return publish_future
