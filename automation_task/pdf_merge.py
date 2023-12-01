import PyPDF2
import sys
import os

merge = PyPDF2.PdfFileMerger()

for file in os.listdir(os.curdir):
    if file.endswith('.pdf'):
        merger.append(file)
    merger.write('combinedPDF')