import io
import json
import os
import tempfile
import time
from typing import Any, Dict, Optional, Tuple

import requests
import scipy.io.wavfile
import torch
import torchaudio
import whisper
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, VitsModel, AutoTokenizer

def transcribe_audio(audio_data: bytes) -> str:
    """
    Transcribe audio data to text using KBLab/kb-whisper-large model.

    Args:
        audio_data: Audio data in bytes format

    Returns:
        Transcribed text or error message
    """
    temp_audio_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        # STT: KB-Whisper Large
        # https://huggingface.co/KBLab/kb-whisper-large
        # 也可以考虑使用large版本，但生成时间显著变长
        # model_id = "KBLab/kb-whisper-large"
        model_id = "KBLab/kb-whisper-small"

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            use_safetensors=True,
            cache_dir="cache"
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_id, cache_dir="cache")

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )

        generate_kwargs = {"task": "transcribe", "language": "sv"}
        res = pipe(temp_audio_path, generate_kwargs=generate_kwargs)

        return res["text"]

    except Exception as e:
        return f"Transcription error with KB-Whisper: {str(e)}"

    finally:
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)


def generate_response(prompt: str, model_name: str) -> Tuple[str, Dict[str, float]]:
    timing_log = {}
    total_start_time = time.time()

    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            return "Error: GEMINI_API_KEY environment variable not set. Please set it to your Gemini API key.", {"total_time": 0.0}

        gemini_api_key = gemini_api_key.strip('"')

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_api_key}"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        # --- LLM API Call Timing ---
        api_call_start_time = time.time()
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        api_call_end_time = time.time()
        timing_log["api_call_time"] = api_call_end_time - api_call_start_time

        response.raise_for_status()

        # --- JSON Parsing Timing ---
        json_parse_start_time = time.time()
        result = response.json()
        json_parse_end_time = time.time()
        timing_log["json_parse_time"] = json_parse_end_time - json_parse_start_time

        response_text = "No valid response generated from Gemini."
        if result and result.get("candidates"):
            first_candidate = result["candidates"][0]
            if first_candidate.get("content") and first_candidate["content"].get("parts"):
                response_text = first_candidate["content"]["parts"][0].get("text", "No text content in response.")

        total_end_time = time.time()
        timing_log["total_llm_time"] = total_end_time - total_start_time
        return response_text, timing_log

    except requests.exceptions.RequestException as e:
        total_end_time = time.time()
        timing_log["total_llm_time"] = total_end_time - total_start_time
        return f"Error communicating with Gemini API: {str(e)}", timing_log
    except json.JSONDecodeError:
        total_end_time = time.time()
        timing_log["total_llm_time"] = total_end_time - total_start_time
        return "Error decoding JSON response from Gemini API.", timing_log
    except Exception as e:
        total_end_time = time.time()
        timing_log["total_llm_time"] = total_end_time - total_start_time
        return f"Error generating response: {str(e)}", timing_log


def generate_audio(text: str, voice: str) -> Tuple[Optional[bytes], Dict[str, float]]:
    timing_log = {}
    total_start_time = time.time()

    try:
        model_id = "facebook/mms-tts-swe"

        # --- Model Load Timing ---
        model_load_start_time = time.time()
        model = VitsModel.from_pretrained(model_id, cache_dir="cache")
        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="cache")
        model_load_end_time = time.time()
        timing_log["model_load_time"] = model_load_end_time - model_load_start_time

        # --- Tokenization Timing ---
        tokenization_start_time = time.time()
        inputs = tokenizer(text, return_tensors="pt")
        tokenization_end_time = time.time()
        timing_log["tokenization_time"] = tokenization_end_time - tokenization_start_time

        # --- Waveform Generation Timing ---
        waveform_gen_start_time = time.time()
        with torch.no_grad():
            waveform = model(**inputs).waveform
        waveform_gen_end_time = time.time()
        timing_log["waveform_gen_time"] = waveform_gen_end_time - waveform_gen_start_time

        # --- Audio Save Timing ---
        save_audio_start_time = time.time()
        buffer = io.BytesIO()
        scipy.io.wavfile.write(buffer, rate=model.config.sampling_rate, data=waveform.squeeze().cpu().numpy())
        buffer.seek(0)
        audio_data = buffer.read()
        save_audio_end_time = time.time()
        timing_log["save_audio_time"] = save_audio_end_time - save_audio_start_time

        total_end_time = time.time()
        timing_log["total_tts_time"] = total_end_time - total_start_time
        return audio_data, timing_log

    except Exception as e:
        print(f"Error generating audio with MMS-TTS: {str(e)}")
        total_end_time = time.time()
        timing_log["total_tts_time"] = total_end_time - total_start_time
        return None, timing_log

