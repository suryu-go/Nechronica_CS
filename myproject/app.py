from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# トップページ表示
@app.route('/')
def index():
    return render_template('index.html')

# キャラクター保管所からのデータ取得API
@app.route('/api/import', methods=['POST'])
def import_vampire_blood():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URLを入力してください'}), 400
        
    # URLの末尾を調整してJSON用URLを作る
    if not url.endswith('.json'):
        json_url = f"{url.rstrip('/')}.json"
    else:
        json_url = url

    try:
        # キャラクター保管所からデータを取得（ヘッダーを指定してエラーを防止）
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(json_url, headers=headers, timeout=5)
        response.raise_for_status()
        char_data = response.json()
        
        return jsonify({
            'status': 'success',
            'data': char_data
        })
        
    except Exception as e:
        return jsonify({'error': f'データの取得に失敗しました: {str(e)}'}), 500

if __name__ == '__main__':
    # 開発用サーバーを起動
    app.run(debug=True)