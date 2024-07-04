import re

ro_specials = [
    # /* VOWELS */
    ['ඓ', 'ai'],  # // sinhala only begin - only kai and ai occurs in reality
    ['ඖ', 'au'],  # // ambiguous conversions e.g. k+au = ka+u = kau, a+u = au but only kau and au occurs in reality
    ['ඍ', 'ṛ'],
    ['ඎ', 'ṝ'],
    # //['ඏ', 'ḷ'], // removed because conflicting with ළ් and very rare
    ['ඐ', 'ḹ'],  # // sinhala only end

    ['අ', 'a'],
    ['ආ', 'ā'],
    ['ඇ', 'æ'], ['ඇ', 'Æ', 1],
    ['ඈ', 'ǣ'],
    ['ඉ', 'i'],
    ['ඊ', 'ī'],
    ['උ', 'u'],
    ['ඌ', 'ū'],
    ['එ', 'e'],
    ['ඒ', 'ē'],
    ['ඔ', 'o'],
    ['ඕ', 'ō'],

    # /* SPECIALS */
    ['ඞ්', 'ṅ'],  # // not used in combi
    ['ං', 'ṃ'], ['ං', 'ṁ', 1],  # // IAST, use both
    ['ඃ', 'ḥ'], ['ඃ', 'Ḥ', 1]  # // sinhala only
]

ro_consonants = [
    ['ඛ', 'kh'],
    ['ඨ', 'ṭh'],
    ['ඝ', 'gh'],
    ['ඡ', 'ch'],
    ['ඣ', 'jh'],
    ['ඦ', 'ñj'],  # //ඤ්ජ
    ['ඪ', 'ḍh'],
    ['ඬ', 'ṇḍ'], ['ඬ', 'dh', 1],  # //ණ්ඩ
    ['ථ', 'th'],
    ['ධ', 'dh'],
    ['ඵ', 'ph'],
    ['භ', 'bh'],
    ['ඹ', 'mb'],  # // non pali
    ['ඳ', 'ṉd'], ['ඳ', 'd', 1],  # // non pali
    ['ඟ', 'ṉg'], ['ඟ', 'g', 1],  # // non pali
    ['ඥ', 'gn'],  # // non pali

    ['ක', 'k'],
    ['ග', 'g'],
    ['ච', 'c'],
    ['ජ', 'j'],
    ['ඤ', 'ñ'],
    ['ට', 'ṭ'],
    ['ඩ', 'ḍ'],
    ['ණ', 'ṇ'],
    ['ත', 't'],
    ['ද', 'd'],
    ['න', 'n'],
    ['ප', 'p'],
    ['බ', 'b'],
    ['ම', 'm'],
    ['ය', 'y'],
    ['ර', 'r'],
    ['ල', 'l'],
    ['ව', 'v'], ['ව', 'w', 1],
    ['ශ', 'ś'],
    ['ෂ', 'ş'], ['ෂ', 'Ṣ', 1], ['ෂ', 'ṣ', 1],
    ['ස', 's'],
    ['හ', 'h'],
    ['ළ', 'ḷ'],
    ['ෆ', 'f']
]

# sinh before, sinh after, roman after
ro_combinations = [
    ['', '', '්'],  # //ක්
    ['', 'a', ''],  # //ක
    ['', 'ā', 'ා'],  # //කා
    ['', 'æ', 'ැ'],  # // non pali
    ['', 'ǣ', 'ෑ'],  # // non pali
    ['', 'i', 'ි'],
    ['', 'ī', 'ී'],
    ['', 'u', 'ු'],
    ['', 'ū', 'ූ'],
    ['', 'e', 'ෙ'],
    ['', 'ē', 'ේ'],  # // non pali
    ['', 'ai', 'ෛ'],  # // non pali
    ['', 'o', 'ො'],
    ['', 'ō', 'ෝ'],  # // non pali

    ['', 'ṛ', 'ෘ'],  # // sinhala only begin
    ['', 'ṝ', 'ෲ'],
    ['', 'au', 'ෞ'],
    # //['', 'ḷ', 'ෟ'], // conflicting with ළ් - might cause bugs - removed bcs very rare
    ['', 'ḹ', 'ෳ']  # // sinhala only end
]


def create_conso_combi(combinations, consonants):
    conso_combi = []
    for combi in combinations:
        for conso in consonants:
            cc = [conso[0] + combi[2], combi[0] + conso[1] + combi[1]]
            if len(conso) > 2:  # add one-way direction if any
                cc.append(conso[2])
            conso_combi.append(cc)
    return conso_combi


ro_conso_combi = create_conso_combi(ro_combinations, ro_consonants)


def roman_to_sinhala(text):
    text = generic_convert(text, 1)
    # add zwj for yansa and rakaransa
    text = replace_re(text, '්ර', '්‍ර')  # rakar
    return replace_re(text, '්ය', '්‍ය')  # yansa


def sinhala_to_roman(text):
    # remove zwj since it does not occur in roman
    text = replace_re(text, '\u200D', '')
    return generic_convert(text, 0)


def replace_re(text, f, r):
    return re.sub(f, r, text, flags=re.IGNORECASE)


def generic_convert(text, dir):
    ro_conso_combi.sort(key=lambda x: len(x[dir]), reverse=True)
    for cc in ro_conso_combi:
        if len(cc) < 3 or cc[2] == dir:
            text = replace_re(text, cc[dir], cc[1 - dir])

    ro_specials.sort(key=lambda x: len(x[dir]), reverse=True)
    for v in ro_specials:
        if len(v) < 3 or v[2] == dir:
            text = replace_re(text, v[dir], v[1 - dir])
    return text


def gen_test_pattern():
    test_sinh = ''
    for cc in ro_conso_combi:
        if len(cc) < 3 or cc[2] == 0:
            test_sinh += cc[0] + ' '

    for v in ro_specials:
        if len(v) < 3 or v[2] == 0:
            test_sinh += v[0] + ' '
    return test_sinh





# # Example text conversion
# text = "kælēka ataraman vuna yakaḍa yakek"
# converted_text = roman_to_sinhala_convert(text)
# print(converted_text)

# text = "කැලේක අතරමන් වුන යකඩ යකෙක්"
# converted_text = sinhala_to_roman_convert(text)
# print(converted_text)

# Example inputTools
# text = "කැලේක අතරමන් වුන යකඩ යකෙක්"
# response = inputTools(text)
# print(response)
# print(response[1][0][1][0])

