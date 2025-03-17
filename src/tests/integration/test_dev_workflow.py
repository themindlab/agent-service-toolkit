
def test_setup_data(test_client):

    res = test_client.post("/execute_workflow",
        json={
            "initial_state": {}, 
            "workflow_id": "dev_workflow"
        })
    thread_id = res.json()['config']['configurable']['thread_id']

    print(thread_id)