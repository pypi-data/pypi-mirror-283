from .base_processor import FabricTextProcessor
import os
import subprocess
from typing import List, Callable
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

class FabricTextProcessor:
    def __init__(self, model: str = "gpt-4-turbo", max_tokens_per_chunk: int = 1000):
        self.model = model
        self.max_tokens_per_chunk = max_tokens_per_chunk
        self.encoding = tiktoken.encoding_for_model(model)

    def preprocess_text(self, text: str) -> str:
        paragraphs = text.split('\n\n')
        processed_paragraphs = []
        
        for paragraph in paragraphs:
            lines = paragraph.split('\n')
            processed_lines = []
            for i, line in enumerate(lines):
                if i == 0 or line.strip() == '' or line.strip().startswith('----'):
                    processed_lines.append(line)
                elif not line[0].isupper() and not line[0].isdigit() and not lines[i-1].strip()[-1] in '.!?:;':
                    processed_lines[-1] += ' ' + line.strip()
                else:
                    processed_lines.append(line)
            processed_paragraphs.append('\n'.join(processed_lines))
        
        return '\n\n'.join(processed_paragraphs)

    def split_text(self, text: str) -> List[str]:
        preprocessed_text = self.preprocess_text(text)
        chars_per_token = len(preprocessed_text) / len(self.encoding.encode(preprocessed_text))
        max_chars = int(self.max_tokens_per_chunk * chars_per_token)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chars,
            chunk_overlap=50,
            length_function=lambda t: len(self.encoding.encode(t)),
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", ".", "!", "?", ";", ",", " ", ""]
        )
        chunks = text_splitter.split_text(preprocessed_text)
        
        final_chunks = []
        for chunk in chunks:
            chunk_tokens = self.encoding.encode(chunk)
            if len(chunk_tokens) > self.max_tokens_per_chunk:
                sub_chunks = self._split_chunk(chunk)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)
        
        return final_chunks

    def _split_chunk(self, chunk: str) -> List[str]:
        import re
        sentences = re.split(r'(?<=[。！？.!?])\s*', chunk)
        sub_chunks = []
        current_sub_chunk = []
        current_token_count = 0

        for sentence in sentences:
            sentence_token_count = len(self.encoding.encode(sentence))
            if current_token_count + sentence_token_count > self.max_tokens_per_chunk:
                if current_sub_chunk:
                    sub_chunks.append(" ".join(current_sub_chunk))
                    current_sub_chunk = []
                    current_token_count = 0
            
            current_sub_chunk.append(sentence)
            current_token_count += sentence_token_count

        if current_sub_chunk:
            sub_chunks.append(" ".join(current_sub_chunk))

        return sub_chunks

    def run_fabric(self, subprompt: str, model: str, input_text: str) -> str:
        process = subprocess.Popen(
            ["fabric", "-sp", subprompt, "-m", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        output = []
        error = []

        process.stdin.write(input_text)
        process.stdin.close()

        for line in process.stdout:
            print(line, end='', flush=True)
            output.append(line)

        for line in process.stderr:
            print(line, end='', file=sys.stderr, flush=True)
            error.append(line)

        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args, ''.join(error))

        return ''.join(output)

    def process_chunks(self, chunks: List[str], pipeline: List[Callable]) -> List[str]:
        results = []
        for i, chunk in enumerate(chunks, 1):
            print(f"\nProcessing chunk {i}/{len(chunks)}:")
            result = self.process_single_chunk(chunk, pipeline)
            results.append(result)
        return results

    def process_single_chunk(self, chunk: str, pipeline: List[Callable]) -> str:
        for step in pipeline:
            chunk = step(self, chunk)
        return chunk


