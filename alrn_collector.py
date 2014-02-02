#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (©) 2014 Marcel Ribeiro Dantas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import re
import tempfile

# This number is a specific id in the ALRN website. 60 means
# the 60th month since they started tracking the spending of
# local politicians.
month_id = 60 # December, 2013

# page 'verbas' in ALRN
verbas = tempfile.NamedTemporaryFile(delete=False)
os.system(("wget http://www.al.rn.gov.br/portal/verbas -O %s") % (verbas.name))
# HTML code in verbas page
html = open(verbas.name, 'r')

# Getting deputies section in the HTML
for line_number, line_content in enumerate(html):
    # Known lines to have names/months, respectively.
    if (line_number == 23):
        # it checks if the lines didnt change
        if (line_content.find("<option value=") != -1):
            deputies = line_content
html.close()
verbas.close()
os.unlink(verbas.name)

# Getting IDs from within the section
ids = re.compile('\"(.*?)\"').findall(deputies)
for id in ids:
# Downloading PDFs
    os.system(("curl --data \"deputado_id=%s&mes_id=%s\" http://www.al.rn.gov.br/portal/verbas > %s.pdf") %(id, month_id, id))
# Extracting and printing on the screen
    os.system(("pdftotext %s.pdf %s") %(id, id))
    pdf_file = open (id, 'r')
    done = False

    for line in pdf_file:
        nome = line.find("Deputado(a):")
        gastoTotal = line.find("Total:")
        if (nome != -1):
            if (done == False):
                print line[nome:-1]
                done = True
        if (gastoTotal != -1):
            print line[gastoTotal:-1]
    pdf_file.close()
