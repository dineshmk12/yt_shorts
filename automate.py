import csv
from datetime import datetime
from gtts import gTTS
from moviepy.editor import TextClip, ColorClip, AudioFileClip, CompositeVideoClip
import os

PROMPT_FILE = "prompts.csv"

def get_next_prompt():
    with open(PROMPT_FILE, "r") as f:
        reader = csv.DictReader(f)
        prompts = list(reader)
    
    for row in prompts:
        if row["status"].strip().lower() == "pending":
            return row["prompt"], prompts
    return None, prompts

def mark_prompt_done(prompts, used_prompt):
    for row in prompts:
        if row["prompt"] == used_prompt:
            row["status"] = "done"
    with open(PROMPT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["prompt", "status"])
        writer.writeheader()
        writer.writerows(prompts)

def generate_script(prompt):
    return f"Here's something interesting: {prompt}"

def generate_audio(script_text):
    tts = gTTS(script_text)
    tts.save("audio.mp3")

def generate_video(prompt):
    txt_clip = TextClip(prompt, fontsize=50, color='white', size=(700, None), method='caption')
    txt_clip = txt_clip.set_duration(10).set_position('center')
    audio = AudioFileClip("audio.mp3")
    background = ColorClip(size=(720,1280), color=(0,0,0), duration=10)
    video = CompositeVideoClip([background, txt_clip.set_position('center')]).set_audio(audio)
    video.write_videofile("short.mp4", fps=24)

def main():
    prompt, prompts = get_next_prompt()
    if not prompt:
        print("No prompts left.")
        return

    print(f"Using prompt: {prompt}")
    script = generate_script(prompt)
    generate_audio(script)
    generate_video(prompt)
    mark_prompt_done(prompts, prompt)

    # YouTube upload (not included here — can be added with credentials)
    print("Video created. Upload step goes here.")

if __name__ == "__main__":
    main()
