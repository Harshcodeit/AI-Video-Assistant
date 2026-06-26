import yt_dlp
import tempfile
from pydub import AudioSegment # pydub an audio manipulation library
import os

# DOWNLOAD_DIR = 'downloads'
# os.makedirs(DOWNLOAD_DIR,exist_ok = True)

DOWNLOAD_DIR = tempfile.mkdtemp()

# yt_dlp(download audio from youtube) -> YouTube URL -> WAV file
# FFmpegExtractAudio converts it to WAV format

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s") #yt_dlp placeholders
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


# convert any format to WAV, make it mono channel, set sampling rate to 16khz
# AudioSegment is pydub class that loads,edits,splits,converts and exports audio files
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path


# split an x- minute audio into chunks
'''
Whisper can become slow and memory-intensive on long audio files.
I split the audio into smaller chunks and transcribe them separately,
which improves scalability and reliability.
'''
def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

# to download a youtube audio in wav format or convert other format to wav
def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks


def process_uploaded_file(uploaded_file) -> list:
    # save streamlit upload object  to a temp file

    suffix = os.path.splitext(uploaded_file.name)[-1]
    with tempfile.NamedTemporaryFile(delete=False,suffix=suffix,dir=DOWNLOAD_DIR) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path=tmp.name

    print(f"Saved upload to {tmp_path}, converting to wav")
    wav_path = convert_to_wav(tmp_path)

    print("CHunking Audio...")
    chunks = chunk_audio(wav_path)

    print(f"Audio Ready - {len(chunks)} chunk(s) created.")

    return chunks


