import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

MODEL_NAME = os.getenv("MODEL_NAME", "t5-small")

_tokenizer = None
_summarizer = None

def load_model():
    global _tokenizer, _summarizer
    if _summarizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        _summarizer = pipeline(
            "summarization",
            model=model,
            tokenizer=_tokenizer,
            device=-1,
        )
    return _summarizer, _tokenizer

def summarize_text(text: str, max_length: int = 80, min_length: int = 10,
                   num_beams: int = 4, length_penalty: float = 1.0):
    summarizer, tokenizer = load_model()
    prompt = "summarize: " + text[:4000]
    result = summarizer(
        prompt,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        length_penalty=length_penalty,
        do_sample=False,
    )
    summary = result[0]["summary_text"]
    return summary, len(tokenizer.encode(text, truncation=True)), len(tokenizer.encode(summary))
