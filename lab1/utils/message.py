import json


def prepare_message_to_read(data):
    data = data.decode("utf-8")
    return json.loads(data)


def show_message(data):
    print(
        "________________________________________________________________\n"
        f"# id: {data['id']}\n"
        f"# nick: {data['nick']}\n"
        f"# message:\n{data['content']}\n"
        "________________________________________________________________\n"
    )
