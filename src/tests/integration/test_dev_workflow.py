
def test_setup_data(test_client):

    res = test_client.post("/execute_workflow",
        json={
            "initial_state": {}, 
            "workflow_id": "dev_workflow"
        })
    assert res.status_code == 200
    res_data = res.json()
    print(res_data)
    thread_id = res_data['config']['configurable']['thread_id']

    print(thread_id)