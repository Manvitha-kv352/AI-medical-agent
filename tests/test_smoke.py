import sys
from pathlib import Path

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
