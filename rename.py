import os

# 対象ディレクトリ
directory = 'songs'

# ディレクトリ内のファイルを取得し、.htmlファイルのみを対象とする
files = [f for f in os.listdir(directory) if f.endswith('.html')]
files.sort()  # ファイル名のソート

# ファイルを連番にリネーム
for i, filename in enumerate(files):
    new_filename = '{}.html'.format(i)
    old_path = os.path.join(directory, filename)
    new_path = os.path.join(directory, new_filename)
    os.rename(old_path, new_path)

print('ファイルのリネームが完了しました。')