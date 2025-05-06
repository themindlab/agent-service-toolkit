import time
THREAD_ID = None

def test_list_workflows(test_client):
    res = test_client.post("/list_workflows", json={})
    assert res.status_code == 200
    res_data = res.json()
    assert len(res_data) > 0

    workflows = []
    for workflow in res_data:
        workflows.append(workflow['key'])
    assert "dev_workflow" in workflows

def test_execute_workflow(test_client):
    res = test_client.post("/execute_workflow",
        json={
            "initial_state": {
                "should_fail": False,
                "counter": 0
            }, 
            "workflow_id": "dev_workflow"
        })
    assert res.status_code == 200
    res_data = res.json()
    assert res_data['config']['configurable']['thread_id'] is not None
    global THREAD_ID
    THREAD_ID = res_data['config']['configurable']['thread_id']

def test_get_thread_state(test_client):
    res = test_client.post("/get_thread_state",
        json={
            "thread_id": THREAD_ID,
            "workflow_id": "dev_workflow"
        })
    assert res.status_code == 200
    res_data = res.json()
    print(res_data)
    assert "messages" in res_data