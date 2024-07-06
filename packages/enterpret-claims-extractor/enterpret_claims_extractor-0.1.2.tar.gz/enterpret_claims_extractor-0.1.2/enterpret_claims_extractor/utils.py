import re
from typing import Dict, List
from nltk.tokenize import sent_tokenize
import csv

def read_records_from_csv(file_path: str, row_ids: List[str]=None):
    records = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row_ids is None or row["ID"] in row_ids:
                records.append({
                    "id": row["ID"],
                    "url": row["URL"],
                    "type": row["Type"],
                    "source": row["Source"],
                    "timestamp": row["CreatedAt"],
                    "content": row["Content"]
                })
    return records

def split_content_based_on_type(content: str, content_type: str) -> Dict[int, str]:
    
    if isinstance(content, str) and content is not None:
        if content_type == "RecordTypeConversation":
            dialogues = re.split(r"(?=User:|Agent:)", content)
            dialogues = [dialogue.strip() for dialogue in dialogues if dialogue != '']
            sentence_dict = {}
            sentence_index = 1
            for dialogue in dialogues:
                sentences = sent_tokenize(dialogue)
                for sentence in sentences:
                    sentence_dict[sentence_index] = sentence
                    sentence_index += 1
            return sentence_dict

        elif content_type == "RecordTypeSurvey":
            sentences = sent_tokenize(content)
            return {index+1: sentence for index, sentence in enumerate(sentences)}
    else:
        return {}