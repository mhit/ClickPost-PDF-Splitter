import fitz
import os
import argparse

# 引数設定
parser = argparse.ArgumentParser(description='PDFをA6サイズ4分割するスクリプト')
parser.add_argument('input_files', type=str, nargs='+', help='入力ファイルのパス')
parser.add_argument('--output-file-prefix', type=str, default='a6', help='出力ファイル名の接頭辞')
parser.add_argument('--dpi', type=int, default=600, help='DPI')
args = parser.parse_args()

# 出力ファイル名の接頭辞
output_file_prefix = args.output_file_prefix

# 各入力ファイルについて処理を行う
for input_file_path in args.input_files:
    # 入力ファイルを開く
    doc = fitz.open(input_file_path)

    # ページ数を取得
    num_pages = len(doc)

    # 出力用の新しいPDFドキュメントを作成
    output_doc = fitz.open()

    # 切り出し範囲構造体
    a6_width = 270
    a6_height = 390
    clip_offset = 14
    clip_cutout_offset_w = 24
    clip_cutout_offset_h = 27
    page_rects = {
        1: fitz.Rect(clip_offset,
                     clip_offset,
                     a6_width + clip_offset,
                     a6_height + clip_offset
                     ),
        2: fitz.Rect(clip_offset + a6_width + clip_cutout_offset_w,
                     clip_offset,
                     (a6_width * 2) + clip_offset + clip_cutout_offset_w,
                     a6_height + clip_offset
                     ),
        3: fitz.Rect(clip_offset,
                     clip_offset + a6_height + clip_cutout_offset_h,
                     a6_width + clip_offset,
                     (a6_height * 2) + clip_offset + clip_cutout_offset_h
                     ),
        4: fitz.Rect(clip_offset + a6_width + clip_cutout_offset_w,
                     clip_offset + a6_height + clip_cutout_offset_h,
                     (a6_width * 2) + clip_offset + clip_cutout_offset_w,
                     (a6_height * 2) + clip_offset + clip_cutout_offset_h
                     )
    }

    # 各ページについて処理を行う
    for d in range(num_pages):
        page = doc[d]
        for p in range(1, 5):
            clip = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=page_rects[p], dpi=args.dpi)
            if clip.pixel(5, 5) == (255, 0, 0):
                new_page = output_doc.new_page(width=a6_width, height=a6_height)
                new_page.insert_image(fitz.Rect(0, 0, a6_width, a6_height), pixmap=clip)

    # 出力ファイル名を作成
    output_file_name = f"{output_file_prefix}_{os.path.splitext(os.path.basename(doc.name))[0]}.pdf"
    # 出力
    output_doc.save(output_file_name, garbage=4, deflate=True, clean=True)
    # ファイルをクローズ
    output_doc.close()
    doc.close()

    print(f"{input_file_path}の処理が完了しました。")
