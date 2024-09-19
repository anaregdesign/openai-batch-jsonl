import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd


# {"custom_id": "Bjcg03WnAQ0", "response": {"body": {"choices": [{"content_filter_results": {"hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": false, "severity": "safe"}, "sexual": {"filtered": false, "severity": "safe"}, "violence": {"filtered": false, "severity": "safe"}}, "finish_reason": "stop", "index": 0, "logprobs": null, "message": {"content": "The person in the image is wearing a floral gown from @fifth_store along with a white camisole.", "role": "assistant"}}], "created": 1726677619, "id": "chatcmpl-A8s0xEsR5FXdyMsVF61vupd75M5Wj", "model": "gpt-4o-2024-05-13", "object": "chat.completion", "prompt_filter_results": [{"prompt_index": 0, "content_filter_result": {"jailbreak": {"filtered": false, "detected": false}, "custom_blocklists": {"filtered": false, "details": []}}}, {"prompt_index": 1, "content_filter_result": {"sexual": {"filtered": false, "severity": "safe"}, "violence": {"filtered": false, "severity": "safe"}, "hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": false, "severity": "safe"}, "custom_blocklists": {"filtered": false, "details": []}}}], "system_fingerprint": "fp_80a1bad4c7", "usage": {"completion_tokens": 22, "prompt_tokens": 814, "total_tokens": 836}}, "request_id": "1dfa42c2-0769-474f-9ce9-f819be76cbaa", "status_code": 200}, "error": null}
# {"custom_id": "CET7KTgFwNC", "response": {"body": {"choices": [{"content_filter_results": {"hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": false, "severity": "safe"}, "sexual": {"filtered": false, "severity": "safe"}, "violence": {"filtered": false, "severity": "safe"}}, "finish_reason": "stop", "index": 0, "logprobs": null, "message": {"content": "It looks like you had a lovely time at the beach! The clear water and serene surroundings suggest a peaceful and relaxing setting. ありがとうございます for sharing this moment.", "role": "assistant"}}], "created": 1726677619, "id": "chatcmpl-A8s0xd9m86SVArqEtEwwwDNlgWoCy", "model": "gpt-4o-2024-05-13", "object": "chat.completion", "prompt_filter_results": [{"prompt_index": 0, "content_filter_result": {"jailbreak": {"filtered": false, "detected": false}, "custom_blocklists": {"filtered": false, "details": []}}}, {"prompt_index": 1, "content_filter_result": {"sexual": {"filtered": false, "severity": "low"}, "violence": {"filtered": false, "severity": "safe"}, "hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": false, "severity": "safe"}, "custom_blocklists": {"filtered": false, "details": []}}}], "system_fingerprint": "fp_80a1bad4c7", "usage": {"completion_tokens": 32, "prompt_tokens": 824, "total_tokens": 856}}, "request_id": "eb3b0bd2-0ba7-4c0a-8db8-976129552c22", "status_code": 200}, "error": null}
# {"custom_id": "BtBIumLHdd5", "response": {"body": {"choices": [{"content_filter_results": {"hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": false, "severity": "safe"}, "sexual": {"filtered": false, "severity": "safe"}, "violence": {"filtered": false, "severity": "safe"}}, "finish_reason": "stop", "index": 0, "logprobs": null, "message": {"content": "This looks like a charming and serene setting for a tea or coffee break. The table is elegantly set with a teapot, a floral teacup, a dessert in a glass dish, and some pastries. The marble table and well-arranged furniture create a sophisticated and cozy atmosphere. Enjoy your time with Luna!", "role": "assistant"}}], "created": 1726677619, "id": "chatcmpl-A8s0xMEHNpHFQ2CaCCLSfl90B631U", "model": "gpt-4o-2024-05-13", "object": "chat.completion", "prompt_filter_results": [{"prompt_index": 0, "content_filter_result": {"jailbreak": {"filtered": false, "detected": false}, "custom_blocklists": {"filtered": false, "details": []}}}, {"prompt_index": 1, "content_filter_result": {"sexual": {"filtered": false, "severity": "safe"}, "violence": {"filtered": false, "severity": "safe"}, "hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": false, "severity": "safe"}, "custom_blocklists": {"filtered": false, "details": []}}}], "system_fingerprint": "fp_80a1bad4c7", "usage": {"completion_tokens": 63, "prompt_tokens": 796, "total_tokens": 859}}, "request_id": "be92356c-4e65-48cb-b0fc-fe6b4a81c9b5", "status_code": 200}, "error": null}


@dataclass(frozen=True)
class Result:
    custom_id: str
    result: str
    created: datetime.time
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


@dataclass(frozen=True)
class BatchOutput:
    results: List[Result]

    @staticmethod
    def load(file_path: str):
        with open(file_path, 'r') as file:
            results = []
            for line in file:
                d = json.loads(line)
                result = Result(
                    custom_id=d['custom_id'],
                    result=d['response'],
                    created=datetime.fromtimestamp(d['response']['body']['created']),
                    completion_tokens=d['response']['body']['usage']['completion_tokens'],
                    prompt_tokens=d['response']['body']['usage']['prompt_tokens'],
                    total_tokens=d['response']['body']['usage']['total_tokens']
                )
                results.append(result)

        return BatchOutput(results)

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self.results)
