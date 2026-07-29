import os
import time
from graph.workflow import run_agent

start = time.time()
result = run_agent('Find papers about AI in neuroscience')
elapsed = time.time() - start
print('elapsed', round(elapsed, 2))
print('answer_keys', sorted(result['answer'].keys()))
print('paper_count', len(result['answer'].get('papers', [])))
print('eval_exists', os.path.exists('evaluation/results/evaluations.jsonl'))
print('log_exists', os.path.exists('evaluation/results/evaluation.log'))
