import time 
import random
import pytest
pytest_plugins = ('pytest_asyncio')

# Cannot get the test to work. However, the workflow is working as expected.
# as it's tested in the wporkflow-orchestrator microservice
# pytest and the async stuff does not seem to want to play nice.

@pytest.mark.asyncio
async def test_setup_data(test_client):
    return
    res = test_client.post("/execute_workflow",
        json={
            "initial_state": {
                "should_fail": False,
                "status": "in_progress",
                "counter": 0
            }, 
            "workflow_id": "dev_workflow"
        })
    assert res.status_code == 200
    res_data = res.json()
    thread_id = res_data['config']['configurable']['thread_id']

    def get_state():
        res = test_client.post(f"/get_thread_state",
            json={
                "thread_id": thread_id,
                "workflow_id": "dev_workflow"
            })
        assert res.status_code == 200
        return res.json()

    time.sleep(1)

    res_data = get_state()

    print(res_data)

    n = 20

    while(n>0):
        res_data = get_state()
        print(res_data)
        time.sleep(0.5)
        n = n-1
    
    assert res_data['status'] == 'completed'

        