import threading


class MetricsStore:
    def __init__(self):
        self._lock = threading.Lock()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_response_time = 0.0
        self.total_pubmed_retrieval_time = 0.0
        self.total_reranking_time = 0.0
        self.total_llm_generation_time = 0.0
        self.total_evaluation_time = 0.0

    def record_request(self, response_time, pubmed_time=0.0, reranking_time=0.0, llm_time=0.0, evaluation_time=0.0, success=True):
        with self._lock:
            self.total_requests += 1
            self.total_response_time += response_time
            self.total_pubmed_retrieval_time += pubmed_time
            self.total_reranking_time += reranking_time
            self.total_llm_generation_time += llm_time
            self.total_evaluation_time += evaluation_time
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

    def record_timing(self, stage, elapsed):
        with self._lock:
            if stage == "pubmed_retrieval":
                self.total_pubmed_retrieval_time += elapsed
            elif stage == "reranking":
                self.total_reranking_time += elapsed
            elif stage == "llm_generation":
                self.total_llm_generation_time += elapsed
            elif stage == "evaluation":
                self.total_evaluation_time += elapsed

    def snapshot(self):
        with self._lock:
            total_requests = self.total_requests or 1
            return {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "average_response_time": round(self.total_response_time / total_requests, 4),
                "pubmed_retrieval_time": round(self.total_pubmed_retrieval_time / total_requests, 4),
                "reranking_time": round(self.total_reranking_time / total_requests, 4),
                "llm_generation_time": round(self.total_llm_generation_time / total_requests, 4),
                "evaluation_time": round(self.total_evaluation_time / total_requests, 4),
            }


metrics_store = MetricsStore()
