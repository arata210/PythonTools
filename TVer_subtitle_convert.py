import html2text


def Sub_Color(c_fgc):
    """
    将c.fgc-x中十进制数x转为3位二进制数, 0/1分别对应00/ff
    :return: Hex Color Code
    """
    c_fgc = int(c_fgc)
    HexColorCode = str()
    for code in bin(c_fgc)[2:].zfill(3):
        if code == '1':
            HexColorCode = HexColorCode + 'ff'
        elif code == '0':
            HexColorCode = HexColorCode + '00'
        else:
            HexColorCode = 'FFFFFF'
            break

    return HexColorCode


def Sub_text(vtt_text):
    """
    处理字幕内容, ass格式标准化输出
    :return: ass_sub
    """
    old_text = vtt_text.split("</c>")
    ass_text = str()
    for new_text in old_text:
        if new_text == '':
            break
        else:
            color = Sub_Color(new_text[7])
            ass_text = ass_text + '{\c&' + color + '&}' + new_text.split(">")[1]

    return ass_text


def Sub_line(line_attr, line_text):
    # print(num)
    time_start = line_attr.split()[0][1:-1]
    # print(time_start)
    time_end = line_attr.split()[2][1:-1]
    # print(time_end)
    length = int(float(line_attr.split()[4][9:-1]) * 19.2)
    # 字体大小默认100, 如果需要更改请同步更改此处的+100
    width = int(float(line_attr.split()[3][5:-1]) * 10.8 + 100)
    pos = '\pos(' + str(length) + ',' + str(width) + ')'
    ass_sub = "Dialogue: 0," + time_start + ',' + time_end + ',Default,,0,0,0,,' + '{' + pos + '}' + Sub_text(line_text)

    return ass_sub.strip('\n')


def main(vtt_file):
    File = open(vtt_file, 'r', encoding='utf-8')
    File_out = open(vtt_file[:-4] + '.ass', 'a', encoding='utf-8')
    File_out.write("""[Script Info]
;
;
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Meiryo,100,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,1,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")

    word_list = list()
    for line in File:
        if line == '' or line == '\n':
            continue
        else:
            word = line.strip()
            word_list.append(word)

    for num in range(1, len(word_list), 2):
        File_out.write(Sub_line(word_list[num], word_list[num + 1]))
        File_out.write('\n')

    File_out.close()
    File.close()


vttFile = input()
main(vttFile)
