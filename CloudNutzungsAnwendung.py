import requests

def get_dataset():
    url = "http://container1:8080/v1/dataset"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch dataset. Status code: {response.status_code}")
        return None


def calculate_consumption(events):
    return_dict = {"result": []}
    sorted_data = {"customer_id": {}}

    for event in events:
        customer_id = event['customerId']
        workload_id = event['workloadId']
        timestamp = event['timestamp']
        event_type = event['eventType']

        if customer_id not in sorted_data["customer_id"]:
            sorted_data["customer_id"][customer_id] = {}
        if workload_id not in sorted_data["customer_id"][customer_id]:
            sorted_data["customer_id"][customer_id][workload_id] = 0
        sorted_data["customer_id"][customer_id][workload_id] += -timestamp if event_type== 'start' else timestamp

    for customer in sorted_data["customer_id"]:
        consumption= 0
        for workload in sorted_data["customer_id"][customer]:
            consumption += sorted_data["customer_id"][customer][workload]
        return_dict["result"].append({"customerId": customer, "consumption": consumption})

    return return_dict

def post_data(consumption_data):
    response = requests.post("http://container1:8080/v1/result", json=consumption_data)
    print(str(response.status_code) + ", " + response.text)


if __name__ == "__main__":
    dataset = get_dataset()

    if dataset is not None:
        events = dataset["events"]
        consumption_data = calculate_consumption(events)
        post_data(consumption_data)
