from mindlab_clients import data_client, query_client

EXPERIMENT_ID= None

def test_data_client():

    data_client.purge({"confirmation": "not_safe"})
    
    experiment_json = {
        "name":
            "tom_test",
        "elements": [{
            "name": "number_1",
            "component": "whatever",
            "configuration": {
                "aribtrary": "object"
            }
        }]
    }

    experiment = data_client.deserialise(experiment_json)
    global EXPERIMENT_ID
    EXPERIMENT_ID = experiment['id']

    populated_experiment = data_client.getPopulatedExperiment({
        'experiment_id': EXPERIMENT_ID
    })

    assert populated_experiment

    current_id = populated_experiment['elements'][0]['id']

    start_dict = {
        "current_id": current_id,
        "status": "started",
        "valid": True,
        "current_instruction": {},
        "participant_id": "tom",
        "context": {}
    }

    session = data_client.startExperiment({
        "experiment_id": EXPERIMENT_ID,
        **start_dict
    })
    session = data_client.submitParticipantData({
        "session_id": session['id'],
        "meta": {"result_id": session["current_result_id"]}
    })
    session = data_client.updateParticipantPosition({
        'session_id': session['id'],
        'status': 'complete',
        'context': {},
        'current_instruction': None,
        'current_id': None
    })


def test_query_client():

    project_id = data_client.createAnalysisProject({
        "name": "toms_project",
        "created_by": "tom",
        "version": 1
    })['id']

    query_client.syncExperimentState({"project_id": project_id, "experiment_id": EXPERIMENT_ID})

    res = query_client.executeQuery({
        "project_id": project_id,
        "query": {
            "_$experiment_sessions": {
                "experiment_id": EXPERIMENT_ID
            }
        }
        })
    assert res['value_count'] == 1
