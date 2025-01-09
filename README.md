# DilutionMate

# 基本仕様
- プログラミング言語: Python
- GUIライブラリ: Tkinter
- openAI（無課金なので使えません）

# 使用方法
1. 溶液情報の入力:
-溶液名（Solution Name）
-原液濃度（Stock Concentration in mol/L）
-目的濃度（Target Concentration in mol/L）
-原液量（Stock Volume in mL）
-目的溶液量（Target Volume in mL）

1.希釈計算:
-片方の値からもう片方を計算する機能があり、例えば：原液量と目的濃度から目的溶液量を計算,目的溶液量と目的濃度から原液量を計算

1.注意点の取得:
-OpenAI APIを使用して、溶液に関する注意点を自動的に取得します。これは、溶液調製時の安全性に関する情報を提供します。

1.結果の表示:
-計算結果と安全性情報を表示し、結果を保存することができます。

1.結果の保存:
-計算結果をテキストファイルに保存する機能も含まれています.
