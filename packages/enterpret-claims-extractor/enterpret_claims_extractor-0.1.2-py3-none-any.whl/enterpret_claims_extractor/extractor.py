import json
import logging
from typing import Dict, List
from openai import OpenAI
from .config import get_openai_api_key
from .exceptions import ClaimsExtractorError
from .utils import split_content_based_on_type
from .prompts import SYSTEM_PROMPT, USER_PROMPT


class ClaimsExtractor:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or get_openai_api_key())
        self.tokenized_inputs = {}
        self.extracted_claims = {}

    def get_claim_indices(self, record: str, record_id: str) -> Dict[str, List[int]]:
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

            claims_dict = json.loads(claims_json)

            claim_indices = list(map(int, claims_dict.get("CLAIMS", {}).keys()))

            self.extracted_claims[record_id] = {idx: claims_dict["CLAIMS"][str(idx)] for idx in claim_indices}
            return {"claim_indices": claim_indices}

        except Exception as e:
            raise ClaimsExtractorError(f"Error extracting claims: {str(e)}")

    def _process_record(self, record: Dict) -> Dict:
        if not all([record.get(key) for key in ["id", "url", "type", "source", "timestamp", "content"]]):
            raise ClaimsExtractorError("All record fields must be provided")
        
        tokenized_content = split_content_based_on_type(record["content"], record["type"])
        self.tokenized_inputs[record["id"]] = tokenized_content  # Store tokenized content with record_id as key

        # Make a GPT call to identify claims and their indices
        claims = self.get_claim_indices(json.dumps(self.tokenized_inputs[record["id"]]), record["id"])

        output = {"record_id": record["id"], "claim_indices": claims["claim_indices"]}

        return output

    def extract_claims(self, records: List[Dict]) -> List[Dict]:
        results = []
        for record in records:
            if record['type'] == 'RecordTypeAudioRecording':
                logging.warning(f"Skipping audio record {record.get('id', 'unknown')}")
                continue
            try:
                result = self._process_record(record)
                results.append(result)
            except ClaimsExtractorError as e:
                logging.error(f"Error processing record {record.get('id', 'unknown')}: {str(e)}")
        return results


    def view_claim_source(self, record_id: str) -> Dict[int, str]:
        if record_id not in self.tokenized_inputs:
            raise ClaimsExtractorError(
                f"No tokenized input available for record_id: {record_id}. Process input first."
            )

        if record_id not in self.extracted_claims:
            raise ClaimsExtractorError(f"No claims found for record_id: {record_id}")

        tokenized_content = self.tokenized_inputs[record_id]
        claim_indices = self.extracted_claims[record_id].keys()

        return {
            idx: tokenized_content.get(idx, "")
            for idx in claim_indices
        }


    def view_extracted_claims(self, record_id: str) -> Dict[int, str]:
        if record_id not in self.extracted_claims:
            raise ClaimsExtractorError(f"No claims found for record_id: {record_id}")

        return self.extracted_claims[record_id]