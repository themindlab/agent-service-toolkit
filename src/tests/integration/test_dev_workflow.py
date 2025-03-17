
def test_setup_data(test_client):

    res = test_client.post("/execute_workflow",
        json={
            "initial_state": {}, 
            "workflow_id": "dev_workflow"
        })
    assert res.status_code == 200
    res_data = res.json()
    thread_id = res_data['config']['configurable']['thread_id']

    while(res_data['status'] == 'running'):
        res = test_client.post("/get_thread_state",
            json={
                "thread_id": thread_id,
                "workflow_id": "dev_workflow"
            })
        assert res.status_code == 200
        res_data = res.json()