import json
import logging
from typing import Dict, List
from openai import OpenAI
from .utils import split_content_based_on_type
from .prompts import SYSTEM_PROMPT, USER_PROMPT
from .config import get_openai_api_key
from .exceptions import ClaimsExtractorError


class ClaimsExtractor:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or get_openai_api_key())
        self.tokenized_inputs = {}
        self.extracted_claims = {}

    def extract_claims(self, record: str, record_id: str) -> Dict[str, List[int]]:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                temperature=0.01,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT},
                    {"role": "assistant", "content": record},
                ],
            )
            claims_json = completion.choices[0].message.content.strip()

            # print('For debuggingd:', claims_json)
            claims_dict = json.loads(claims_json)

            claim_indices = list(map(int, claims_dict.get("CLAIMS", {}).keys()))
            self.extracted_claims[record_id] = {
                idx: claims_dict["CLAIMS"][str(idx)] for idx in claim_indices
            }
            return {"claim_indices": claim_indices}

        except Exception as e:
            raise ClaimsExtractorError(f"Error extracting claims: {str(e)}")

    def _process_record(self, record: Dict, verbose: bool = False) -> Dict:
        if not all([record.get(key) for key in ["id", "url", "type", "source", "timestamp", "content"]]):
            raise ClaimsExtractorError("All record fields must be provided")

        record_id = record["id"]
        self.tokenized_inputs[record_id] = split_content_based_on_type(record["content"], record["type"])
        
        if verbose:
            logging.info(f"Tokenized input for record {record_id}:")

        for idx, token in self.tokenized_inputs[record_id].items():
            print(f"  {idx}: {token}")

        # For conversation type, we'll send the whole content to GPT
        if record["type"] == "RecordTypeConversation":
            claims = self.extract_claims(record["content"], record_id)
        else:
            claims = self.extract_claims(json.dumps(self.tokenized_inputs[record_id]), record_id)

        output = {"record_id": record_id, "claim_indices": claims["claim_indices"]}

        return output

    def process_records(self, records: List[Dict]) -> List[Dict]:
        results = []
        for record in records:
            try:
                result = self._process_record(record)
                results.append(result)
            except ClaimsExtractorError as e:
                print(
                    f"Error processing record {record.get('id', 'unknown')}: {str(e)}"
                )
        return results

    def view_claim_source(self, record_id: str, claim_indices: List[int]) -> Dict[int, str]:
        if record_id not in self.tokenized_inputs:
            raise ClaimsExtractorError(
                f"No tokenized input available for record {record_id}. Process input first."
            )

        tokenized_input = self.tokenized_inputs[record_id]
        return {
            idx: tokenized_input.get(idx, f"Claim {idx} (spanning multiple sentences)")
            for idx in claim_indices
        }

    def view_extracted_claims(self, record_id: str) -> Dict[int, str]:
        if not self.extracted_claims:
            raise ClaimsExtractorError(
                "No claims have been extracted. Process input first."
            )

        if record_id in self.extracted_claims:
            return self.extracted_claims[record_id]
        else:
            raise ClaimsExtractorError(f"No claims found for record_id: {record_id}")
