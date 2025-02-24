import pytest
import asyncio

from mindlab_clients import data_client, query_client

PROJECT_ID = None
EXPERIMENT_ID = None
ELEMENT_ID = None
DATA = None

"""
This is not a proper test, I'm just using it to mess around and try and scope out
the work flow between data-server, query-server and agent-server.
Might rework this into a proper test later but for now it's not going to run properly.
"""
# Uncomment to run test
@pytest.mark.skip
def test_setup_data():

    experiments = data_client.getExperiments({})
    
    for exp in experiments:
        if exp['name'] == "uganda_waragi":
            global EXPERIMENT_ID
            EXPERIMENT_ID = exp['id']
    
    description = data_client.describeExperiment({"experiment_id": EXPERIMENT_ID})
    
    for element in description['elements'].values():
        if element['name'] == "demo_age":
            global ELEMENT_ID
            ELEMENT_ID = element['id']
    
    # If project doesn't exist yet  run this
    #global PROJECT_ID
    #PROJECT_ID = data_client.createAnalysisProject({
    #    "name": "toms_project",
    #    "created_by": "tom",
    #    "version": 1
    #})['id']

    projects = data_client.getAnalysisProjects({})
    for project in projects:
        if project['name'] == "toms_project":
            global PROJECT_ID
            PROJECT_ID = project['id']

    query_client.syncExperimentState({"project_id": PROJECT_ID, "experiment_id": EXPERIMENT_ID})

    res = query_client.executeQuery({
        "project_id": PROJECT_ID,
        "query": {
            "_$apply_stats": {
                "indexes": [
                    {"_$data_rows_for_sessions": {
                        "session_index": {"_$experiment_sessions": {"experiment_id": EXPERIMENT_ID}},
                        "element_id": ELEMENT_ID,
                        "table_name": "data_integerinput"
                    }}
                ],
                "stats": {
                    "response": ["prop_table"]
                }
            }
        }
    })
    global DATA
    DATA = res[0]['response']['prop_table']
    assert True

#@pytest.mark.asyncio
@pytest.mark.skip
async def test_get_insights_from_data(test_client):

    res = test_client.post("/execute_workflow", json={"data": DATA, "workflow": "proportion_agent"})
    thread_id = res.json()['config']['configurable']['thread_id']

    res = test_client.post("/get_workflow", json={"thread_id": thread_id}).json()
    assert "result" not in res

    await asyncio.sleep(5)
    res = test_client.post("/get_workflow", json={"thread_id": thread_id}).json()
    assert "result" in res
