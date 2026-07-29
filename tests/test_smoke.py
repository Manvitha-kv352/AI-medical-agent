import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api import app as fastapi_app
from prompts.prompt_loader import render_prompt
from graph.workflow import run_agent
from evaluation.ragas_backend import evaluate_and_store


def test_health_endpoint():
    client = TestClient(fastapi_app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_prompt_loader():
    rendered = render_prompt('answer_generation', version='v1', question='Test', context_text='ctx')
    assert 'Test' in rendered
    assert 'Context:' in rendered


def test_workflow_and_eval_smoke():
    result = run_agent('Find papers about AI in neuroscience')
    assert isinstance(result, dict)
    assert 'answer' in result

    eval_record = evaluate_and_store(
        query='Find papers about AI in neuroscience',
        answer=result.get('answer', {}),
        retrieved_docs=result.get('retrieved_docs', []),
        prompt_versions={'answer': 'v1', 'citation': 'v1', 'evaluation': 'v1', 'query': 'v1'},
    )
    assert 'faithfulness_score' in eval_record


def test_research_endpoint_returns_structured_payload():
    client = TestClient(fastapi_app)
    response = client.post('/research', json={'question': 'Find papers about AI in neuroscience'})
    assert response.status_code == 200
    payload = response.json()
    assert 'query' in payload
    assert 'answer' in payload
    assert 'topic' in payload['answer']
    assert 'papers' in payload['answer']
    assert isinstance(payload['answer']['papers'], list)


def test_research_endpoint_handles_internal_errors():
    client = TestClient(fastapi_app)
    with patch('api.agent_app.invoke', side_effect=RuntimeError('boom')):
        response = client.post('/research', json={'question': 'Find papers about AI in neuroscience'})

    assert response.status_code == 500
    payload = response.json()
    assert 'error' in payload
    assert payload['error']['type'] == 'workflow_error'


def test_research_endpoint_rejects_empty_question():
    client = TestClient(fastapi_app)
    response = client.post('/research', json={'question': ''})
    assert response.status_code == 400
