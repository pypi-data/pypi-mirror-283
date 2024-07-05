import re
from typing import Dict
from nltk.tokenize import sent_tokenize
import datetime

def split_content_based_on_type(content: str, content_type: str) -> Dict[int, str]:
    if content_type == "RecordTypeAudioRecording":
        return {1: "<AUDIO_CONTENT>"}

    elif isinstance(content, str) and content is not None:
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