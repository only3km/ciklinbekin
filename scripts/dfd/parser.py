from .models.entry import DFDCharacterEntry, DFDRadicalEntry

def _process_dfd(lines, entry_cls):
    page = 1
    col = 1
    stroke = 1
    row = 1
    output = []
    for line in lines:
        line = line.strip()
        # remove comment
        percent_sign = line.find('%')
        if percent_sign != -1:
            line = line[:percent_sign].strip()
        if len(line) == 0:
            continue
        if line.startswith('+'):
            # control
            if line.startswith('+Page'):
                if line.startswith('+Page='):
                    page = int(line[len('+Page='):])
                    col=1
                    row=1
                else:
                    page += 1
                    col=1
                    row=1
            elif line.startswith('+Column'):
                if line.startswith('+Column='):
                    col = int(line[len('+Column='):])
                    row = 1
                else:
                    col+=1
                    row=1
            elif line.startswith('+Stroke'):
                if line.startswith('+Stroke='):
                    stroke = int(line[len('+Stroke='):])
            else:
                print('Unknown command', line)
        else:
            success, entry = entry_cls.parse_line(line,page, col, row, stroke)
            if success:
                output.append(entry)
                row+=1
            else:
                print('parse line failed: ', line)
    return output

def process_dfd_characters(lines):
    """Parse DFDCharacters.txt
    """
    return _process_dfd(lines,DFDCharacterEntry)

def process_dfd_radicals(lines):
    """Parse DFDRadicals.txt
    """
    return _process_dfd(lines,DFDRadicalEntry)