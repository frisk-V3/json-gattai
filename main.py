import json
import glob
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class JsonMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON行分割マージツール")
        self.root.geometry("600x450")

        self.label = tk.Label(root, text="JSONフォルダを選択して「改行区切り」で結合します", pady=10)
        self.label.pack()

        self.select_btn = tk.Button(root, text="フォルダを選択", command=self.select_folder)
        self.select_btn.pack(pady=5)

        self.run_btn = tk.Button(root, text="改行区切りで結合開始！", command=self.merge_json_to_lines, bg="#0078D7", fg="white", state="disabled")
        self.run_btn.pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(root, height=15, width=70)
        self.log_area.pack(padx=10, pady=10)

        self.selected_dir = ""

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def select_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_dir = directory
            self.log(f"【選択】: {directory}")
            self.run_btn.config(state="normal")

    def merge_json_to_lines(self):
        output_file_name = "combined_lines.json" # 区別のためファイル名変更
        output_path = os.path.join(self.selected_dir, output_file_name)
        
        search_path = os.path.join(self.selected_dir, "*.json")
        files = [f for f in glob.glob(search_path) if os.path.basename(f) != output_file_name]
        
        if not files:
            messagebox.showwarning("警告", "JSONファイルがありません。")
            return

        self.log("--- 処理開始 ---")
        count = 0

        try:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for file_path in files:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        try:
                            data = json.load(infile)
                            
                            # リストの場合は中身を1つずつ取り出して書き込む
                            if isinstance(data, list):
                                for item in data:
                                    json.dump(item, outfile, ensure_ascii=False)
                                    outfile.write('\n') # ここで改行を入れる
                                    count += 1
                            # 辞書（単体データ）の場合はそのまま書き込む
                            else:
                                json.dump(data, outfile, ensure_ascii=False)
                                outfile.write('\n') # ここで改行を入れる
                                count += 1
                            
                            self.log(f"読み込み成功: {os.path.basename(file_path)}")
                        except Exception as e:
                            self.log(f"読み込み失敗: {os.path.basename(file_path)} ({e})")

            self.log(f"\n完了！ 合計 {count} 件のデータを改行区切りで保存しました。")
            self.log(f"保存先: {output_path}")
            messagebox.showinfo("成功", f"{count} 件のデータを結合しました。")

        except Exception as e:
            messagebox.showerror("エラー", f"ファイル保存中にエラーが発生しました: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonMergerApp(root)
    root.mainloop()
