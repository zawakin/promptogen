import os

# プロジェクトのルートディレクトリを取得
root_dir = os.path.dirname(os.path.abspath(__file__))

# 出力ディレクトリを設定
output_dir = os.path.join(root_dir, 'output')

# 出力ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)


def make_json_path(path: str):
    return os.path.join(output_dir, path)
