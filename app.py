from flask import Flask, render_template, request
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            youtube_video = request.form['youtube_video']
            video_id = youtube_video.split("=")[1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            result = ""
            for i in transcript:
                result += ' ' + i['text']
            
            summarizer = pipeline('summarization')
            
            num_iters = int(len(result) / 1000)
            summarized_text = []
            for i in range(num_iters + 1):
                start = i * 1000
                end = (i + 1) * 1000
                input_text = result[start:end]
                out = summarizer(input_text)
                out = out[0]
                out = out['summary_text']
                summarized_text.append(out)
            
            summarized_text = ' '.join(summarized_text)
            
            return render_template('result.html', summarized_text=summarized_text)
        
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
