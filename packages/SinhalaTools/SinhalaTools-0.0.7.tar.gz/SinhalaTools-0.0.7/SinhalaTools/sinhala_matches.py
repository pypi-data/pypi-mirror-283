import re

singlish_vowels = [
    ['අ', 'a'],
    ['ආ', 'aa'],
    ['ඇ', 'ae'],
    ['ඈ', 'ae, aee'],
    ['ඉ', 'i'],
    ['ඊ', 'ii'],
    ['උ', 'u'],
    ['ඌ', 'uu'],
    ['එ', 'e'],
    ['ඒ', 'ee'],
    ['ඔ', 'o'],
    ['ඕ', 'oo'],
    ['ඓ', 'ai'],  # sinhala only begin
    ['ඖ', 'ou'],
    ['ඍ', 'ru'],
    ['ඎ', 'ru, ruu'],
    # //['ඏ', 'li'], /** 2020-6-22 commented out some rare letters to prevent too many possibilites */
    # //['ඐ', 'li, lii'] // sinhala only end
]

singlish_specials = [
    ['ඞ්', 'n'],
    ['ං', 'n, m'],
    # //['ඃ', 'n, m'] // sinhala only
]

singlish_consonants = [
    ['ක', 'k'],
    ['ග', 'g'],
    ['ච', 'c, ch'],
    ['ජ', 'j'],
    ['ඤ', 'n, kn'],
    ['ට', 't'],
    ['ඩ', 'd'],
    ['ණ', 'n'],
    ['ත', 'th'],
    ['ද', 'd'],
    ['න', 'n'],
    ['ප', 'p'],
    ['බ', 'b'],
    ['ම', 'm'],
    ['ය', 'y'],
    ['ර', 'r'],
    ['ල', 'l'],
    ['ව', 'v, w'],
    ['ශ', 'sh'],
    ['ෂ', 'sh'],
    ['ස', 's'],
    ['හ', 'h'],
    ['ළ', 'l'],
    ['ෆ', 'f'],
    ['ඛ', 'kh, k'],
    ['ඨ', 't'],
    ['ඝ', 'gh'],
    ['ඟ', 'ng'],
    ['ඡ', 'ch'],
    ['ඣ', 'jh'],
    ['ඦ', 'nj'],
    ['ඪ', 'dh'],
    ['ඬ', 'nd'],
    ['ථ', 'th'],
    ['ධ', 'dh'],
    ['ඳ', 'nd'],
    ['ඵ', 'ph'],
    ['භ', 'bh'],
    ['ඹ', 'mb'],
    ['ඥ', 'gn']  # // sinhala only
]

singlish_combinations = [
    ['්', ''],  # //ක්
    ['', 'a'],  # //ක
    ['ා', 'a, aa'],  # //කා
    ['ැ', 'ae'],
    ['ෑ', 'ae, aee'],
    ['ි', 'i'],
    ['ී', 'i, ii'],
    ['ු', 'u'],
    ['ූ', 'u, uu'],
    ['ෙ', 'e'],
    ['ේ', 'e, ee'],
    ['ෛ', 'ei'],
    ['ො', 'o'],
    ['ෝ', 'o, oo'],
    ['්‍ර', 'ra'],  # //ක්‍ර
    ['්‍රා', 'ra, raa'],  # //ක්‍රා
    ['්‍රැ', 'rae'],
    ['්‍රෑ', 'rae, raee'],
    ['්‍රි', 'ri'],
    ['්‍රී', 'ri, rii'],
    ['්‍රෙ', 're'],
    ['්‍රේ', 're, ree'],
    ['්‍රෛ', 'rei'],
    ['්‍රො', 'ro'],
    ['්‍රෝ', 'ro, roo'],
    ['්‍ය', 'ya'],  # //ක්‍ය
    ['්‍යා', 'ya, yaa'],  # //ක්‍යා
    ['්‍යැ', 'yae'],
    ['්‍යෑ', 'yae, yaee'],
    ['්‍යි', 'yi'],
    ['්‍යී', 'yi, yii'],
    ['්‍යු', 'yu'],
    ['්‍යූ', 'yu, yuu'],
    ['්‍යෙ', 'ye'],
    ['්‍යේ', 'ye, yee'],
    ['්‍යෛ', 'yei'],
    ['්‍යො', 'yo'],
    ['්‍යෝ', 'yo, yoo'],
    ['ෘ', 'ru'],  # // sinhala only begin
    ['ෲ', 'ru, ruu'],
    ['ෞ', 'au'],
    # //['ෟ', 'li'],
    # //['ෳ', 'li, lii'] // sinhala only end
]


singlish_mapping = {}
max_singlish_key_len = 0


def add_to_singlish_mapping(values, p_sinh_str, p_roman_str):
    global max_singlish_key_len
    for pair in values:
        sinh = pair[0] + p_sinh_str

        romans = pair[1].split(',')
        p_romans = p_roman_str.split(',')

        for roman in romans:
            for p_roman in p_romans:
                map_index = roman.strip() + p_roman.strip()
                if map_index in singlish_mapping:
                    singlish_mapping[map_index].append(sinh)
                else:
                    singlish_mapping[map_index] = [sinh]
                    max_singlish_key_len = max(
                        len(map_index), max_singlish_key_len)


add_to_singlish_mapping(singlish_vowels, '', '')
add_to_singlish_mapping(singlish_specials, '', '')
for combi in singlish_combinations:
    add_to_singlish_mapping(singlish_consonants, combi[0], combi[1])


def possible_matches(input_str, max_input_length=20):

    if len(input_str) > max_input_length:
        return [input_str]

    matches = []
    for length in range(1, min(max_singlish_key_len, len(input_str)) + 1):
        prefix = input_str[:length]
        rest = input_str[length:]
        matches.extend(permute_matches(prefix, rest))

    # Remove 1) two consecutive hals 2) consecutive independent vowels 3) hal followed by an independent vowel
    # that do not occur in Sinhala - reduce the number of matches to prevent SQL query from exploding
    pattern = re.compile(r'[ක-ෆ]්[ක-ෆ]්|[්ං][අ-ඎ]|[අ-ඎ][අ-ඎ]')
    return [match for match in matches if not pattern.search(match)]


def permute_matches(prefix, rest):
    # If prefix is all Sinhala then pass through the prefix - this allows Sinhala and Singlish mixing and ending dot
    prefix_mappings = singlish_mapping.get(prefix) if is_singlish_query(
        prefix) else ([prefix] if len(prefix) == 1 else [])
    if not prefix_mappings:  # recursion ending condition
        return []
    if not rest:  # recursion ending condition
        return prefix_mappings

    rest_mappings = possible_matches(rest)
    full_mappings = [
        prefix_m + rest_m for rest_m in rest_mappings for prefix_m in prefix_mappings]
    return full_mappings


def is_singlish_query(query):
    return bool(re.search(r'[A-Za-z]', query))