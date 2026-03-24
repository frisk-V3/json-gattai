import json
import glob
import os

def merge_json_files(output_file="combined.json"):
    # カレントディレクトリ内の全jsonファイルを取得（output_file自体は除外）
    files = [f for f in glob.glob("*.json") if f != output_file]
    combined_data = []

    print(f"発見されたファイル: {files}")

    for file_name in files:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 中身がリストなら中身を追加、辞書ならそのまま追加
                if isinstance(data, list):
                    combined_data.extend(data)
                else:
                    combined_data.append(data)
            print(f"成功: {file_name}")
        except Exception as e:
            print(f"失敗: {file_name} - {e}")

    # 結果を保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"がっちゃんこ完了！ 合計 {len(combined_data)} 件を {output_file} に保存しました。")

if __name__ == "__main__":
    merge_json_files()
