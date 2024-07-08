#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#j
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import pypdf 
import mtbp3
import os

class pdfSummary:
    def __init__(self, path = None):
        
        if not isinstance(path, str) or len(path) == 0:
            self.pdf_path = mtbp3.get_data('attention.pdf')
            self.demo = True
        else:
            self.pdf_path = path
            self.demo = False

        try:
            file = open(self.pdf_path, 'rb')
            self.pp = pypdf.PdfReader(file)
        except FileNotFoundError:
            raise ValueError("File not found")

        self.n_page = self.pp.get_num_pages()
        self.file_size = os.path.getsize(self.pdf_path)
        self.n_image_in_page = [len(self.pp.pages[i].images) for i in range(self.n_page)]
        self.n_image = sum(self.n_image_in_page)
        self.meta = self.pp.metadata

if __name__ == "__main__":

    pdf_obj = pdfSummary("/Users/yh2020/dt2/proj/mtbp3/mtbp3/data/attention.pdf")
    print(pdf_obj.meta.creation_date)

