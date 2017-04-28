from azure.storage.queue import QueueService
import settings
import requests
import subprocess


def init_queue_service():
    queue_service = QueueService(connection_string=settings.QUEUE_CONNECTION)
    queue_service.create_queue(settings.QUEUE_NAME)
    return queue_service


def init_queue_consumer():
    queue_service = init_queue_service()
    return queue_service.peek_messages(settings.QUEUE_NAME)


def main_context():
    try:
        app()
    except:
        main_context()


def app():
    queue_service = init_queue_service()
    while True:
        messages = queue_service.get_messages(settings.QUEUE_NAME)
        for message in messages:
            message_content = message.message_text
            if proof1(message_content):
                if proof2():
                    start_sh_script()
            queue_service.delete_message(settings.QUEUE_NAME, message.message_id, message.pop_receipt)


def proof1(content):
    return proof1_check_message_content(content=content)


def proof1_check_message_content(content):
    if content in settings.PROOF1_CONTENT_MESSAGE:
        return True
    else:
        return False


def proof2():
    state = proof2_get_state_from_url()
    print(state)
    if settings.PROOF2_ENVIRONMENT in state['Env']:
        return False
    else:
        return True


def proof2_get_state_from_url():
    response = requests.get(settings.PROOF2_URL)
    return response.json()


def start_sh_script():
    script_list = [settings.SCRIPT_FILENAME]
    subprocess.call(script_list)


if __name__ == "__main__":
    print("Start consume...")
    main_context()
