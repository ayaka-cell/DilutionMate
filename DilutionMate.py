import tkinter as tk
from tkinter import messagebox, filedialog
import openai

# OpenAIのAPIキー（ユーザーのAPIキーを設定してください◎）
openai.api_key = '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'
solution_name = "溶液に関する注意点を教えてください。<mask>"

# OpenAI APIを使用して溶液に関する注意点を取得する関数
def get_solution_info(solution_name):
    try:
        # ChatCompletionエンドポイントを使用
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # モデル名
            messages=[
                {"role": "system", "content": "あなたは化学の専門家で、安全性のガイドラインを提供します。"},
                {"role": "user", "content": f"溶液名: {solution_name} の調製に関する注意点を教えてください。"}
            ],
            temperature=0.7,  # レスポンスのランダム性
        )
        # レスポンスから注意点を取得
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"OpenAIからの情報取得に失敗しました: {e}"


# GUIアプリケーション
class DilutionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("希釈計算ツール")
        
        # 入力フィールド
        self.label_solution_name = tk.Label(root, text="溶液名:")
        self.label_solution_name.grid(row=0, column=0)
        self.entry_solution_name = tk.Entry(root)
        self.entry_solution_name.grid(row=0, column=1)
        
        self.label_stock_concentration = tk.Label(root, text="原液濃度 (mol/L):")
        self.label_stock_concentration.grid(row=1, column=0)
        self.entry_stock_concentration = tk.Entry(root)
        self.entry_stock_concentration.grid(row=1, column=1)
        
        self.label_target_concentration = tk.Label(root, text="目的濃度 (mol/L):")
        self.label_target_concentration.grid(row=2, column=0)
        self.entry_target_concentration = tk.Entry(root)
        self.entry_target_concentration.grid(row=2, column=1)
        
        self.label_stock_volume = tk.Label(root, text="原液量 (mL):")
        self.label_stock_volume.grid(row=3, column=0)
        self.entry_stock_volume = tk.Entry(root)
        self.entry_stock_volume.grid(row=3, column=1)
        
        self.label_target_volume = tk.Label(root, text="目的溶液量 (mL):")
        self.label_target_volume.grid(row=4, column=0)
        self.entry_target_volume = tk.Entry(root)
        self.entry_target_volume.grid(row=4, column=1)
        
        # 計算ボタン
        self.calculate_button = tk.Button(root, text="計算", command=self.calculate)
        self.calculate_button.grid(row=5, column=0, columnspan=2)

        # 保存ボタン
        self.save_button = tk.Button(root, text="結果を保存", command=self.save_results)
        self.save_button.grid(row=6, column=0, columnspan=2)
        
        # 結果表示
        self.result_label = tk.Label(root, text="", justify="left")
        self.result_label.grid(row=7, column=0, columnspan=2)

        # 結果保存用変数
        self.results = ""

    def calculate(self):
        """希釈計算と注意点の取得を行う関数"""
        try:
            solution_name = self.entry_solution_name.get()
            stock_concentration = float(self.entry_stock_concentration.get())
            target_concentration = float(self.entry_target_concentration.get())
            stock_volume = self.entry_stock_volume.get()
            target_volume = self.entry_target_volume.get()

            # 必須フィールド確認
            if not solution_name or not stock_concentration or not target_concentration:
                messagebox.showerror("入力エラー", "溶液名、原液濃度、目的濃度は必須項目です。")
                return
            
            # 希釈計算
            if stock_volume and not target_volume:
                stock_volume = float(stock_volume)
                target_volume = (stock_volume * stock_concentration) / target_concentration
                calculation_result = f"必要な目的溶液量: {target_volume:.2f} mL"
            elif target_volume and not stock_volume:
                target_volume = float(target_volume)
                stock_volume = (target_volume * target_concentration) / stock_concentration
                calculation_result = f"必要な原液量: {stock_volume:.2f} mL"
            else:
                messagebox.showerror("入力エラー", "原液量または目的溶液量のどちらかを入力してください。")
                return

            # OpenAIから注意点取得
            safety_info = get_solution_info(solution_name)

            # 結果表示
            self.results = (
                f"溶液名: {solution_name}\n"
                f"原液濃度: {stock_concentration} mol/L\n"
                f"目的濃度: {target_concentration} mol/L\n"
                f"{calculation_result}\n"
                f"注意点: {safety_info}"
            )
            self.result_label.config(text=self.results)

        except ValueError:
            messagebox.showerror("入力エラー", "数値を正しく入力してください。")

    def save_results(self):
        """結果をテキストファイルに保存する関数"""
        if not self.results:
            messagebox.showerror("保存エラー", "保存する結果がありません。")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.results)
                messagebox.showinfo("保存成功", "結果を保存しました。")
            except Exception as e:
                messagebox.showerror("保存エラー", f"ファイルの保存に失敗しました: {e}")

# アプリケーション実行
if __name__ == "__main__":
    root = tk.Tk()
    app = DilutionTool(root)
    root.mainloop()
