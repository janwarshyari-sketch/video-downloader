from flask import Flask, request, jsonify, render_template
import yt_dlp
import os
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    url = data.get('url') if data else None
    if not url:
        return jsonify({"error": "Link nahi mila"}), 400
    try:
        ydl_opts = {'quiet': True, 'no_playlist': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', [])[::-1]:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                    formats.append({"quality": f.get('format_note') or f"{f.get('height')}p", "ext": "mp4", "url": f.get('url')})
                if len(formats) >= 4:
                    break
            if not formats:
                formats.append({"quality": "Best", "ext": "mp4", "url": info.get('url')})
            return jsonify({"title": info.get('title'), "thumbnail": info.get('thumbnail'), "downloads": formats})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
