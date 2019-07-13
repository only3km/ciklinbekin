# 將 DFD 轉換成一行一條的 denormalised 的 CSV

from jinja2 import Template

from dfd.models.entry import EntryType
from dfd.parser import process_dfd_characters, process_dfd_radicals

DFDCharacters = open("../DFDCharacters.txt", "r", encoding='utf8').readlines()

entries = process_dfd_characters(DFDCharacters)

# DFDCharacters.csv
import csv
with open('../build/DFDCharacters.csv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, dialect='excel', lineterminator='\n')
    writer.writerow(["字頭#","漢字","IDS替代字","羅馬字","羅馬字（轉寫）","頁碼","列","行","部首#","註釋"])
    for i in range(0, len(entries)):
        if (entries[i].type == EntryType.NORMAL_CHARACTER):
            this_entry = entries[i]
            for c in this_entry.characters:
                if c.is_deleted:
                    continue
                for r in this_entry.r10n:
                    if r.is_deleted:
                        continue
                    writer.writerow([
                        i+1,
                        c.get_corrected().char if c.get_corrected().ids is None else c.get_corrected().ids, 
                        c.get_corrected().char if c.get_corrected().ids is not None else '', 
                        r.get_buc_corrected(),
                        r.get_r10n_corrected(),
                        this_entry.page_no,
                        this_entry.col_no,
                        this_entry.row_no,
                        this_entry.stroke_no,
                        "原書有誤，已更正" if c.has_correction() or r.has_correction() else ''
                        ])
