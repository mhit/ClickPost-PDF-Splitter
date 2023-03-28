# ClickPost-PDF-Splitter
Shipping labels created through Click Post are generated as a single PDF page in A6 size. This allows for easy printing with label printers.

クリックポストで作成される送り状は、A6サイズの単一のPDFページとして生成されます。これにより、ラベル印刷機で簡単に印刷できます。
起動引数にPDFを複数渡せばまとめて処理します.

```
PDFをA6サイズ4分割するスクリプト

positional arguments:
  input_files           入力ファイルのパス

options:
  -h, --help            show this help message and exit
  --output-file-prefix OUTPUT_FILE_PREFIX
                        出力ファイル名の接頭辞
  --dpi DPI             DPI
```
