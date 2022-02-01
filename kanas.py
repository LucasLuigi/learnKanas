# -*-coding:utf-8 -*

ALPHABETS = ['Hiragana', 'Katakana', 'Kanji']

# The order must match with the input of selectKanasSubset
KANAS_SUBSETS = ["simple Kanas", "Dakuon",
                 "Handakuon", "combo Kanas", "Kanas"]

SIMPLE_KANAS_ROMA = {
    "": ["a", "i", "u", "e", "o"],
    "K": ["ka", "ki", "ku", "ke", "ko"],
    "S": ["sa", "shi", "su", "se", "so"],
    "T": ["ta", "chi", "tsu", "te", "to"],
    "N": ["na", "ni", "nu", "ne", "no"],
    "H": ["ha", "hi", "fu", "he", "ho"],
    "M": ["ma", "mi", "mu", "me", "mo"],
    "Y": ["ya", "yu", "yo"],
    "R": ["ra", "ri", "ru", "re", "ro"],
    "W": ["wa", "wo"],
    "n": ["n"]
}

SIMPLE_KANAS_HIRA = {
    "": ["あ", "い", "う", "え", "お"],
    "K": ["か", "き", "く", "け", "こ"],
    "S": ["さ", "し", "す", "せ", "そ"],
    "T": ["た", "ち", "つ", "て", "と"],
    "N": ["な", "に", "ぬ", "ね", "の"],
    "H": ["は", "ひ", "ふ", "へ", "ほ"],
    "M": ["ま", "み", "む", "め", "も"],
    "Y": ["や", "ゆ", "よ"],
    "R": ["ら", "り", "る", "れ", "ろ"],
    "W": ["わ", "を"],
    "n": ["ん"]
}

DAKUON_ROMA = {
    "G": ["ga", "gi", "gu", "ge", "go"],
    "Z": ["za", "z_ji", "zu", "ze", "zo"],
    "D": ["da", "d_ji", "d_ju", "de", "do"],
    "B": ["ba", "bi", "bu", "be", "bo"]
}

DAKUON_HIRA = {
    "G": ["が", "ぎ", "ぐ", "げ", "ご"],
    "Z": ["ざ", "じ", "ず", "ぜ", "ぞ"],
    "D": ["だ", "ぢ", "づ", "で", "ど"],
    "B": ["ば", "び", "ぶ", "べ", "ぼ"]
}

HANDAKUON_ROMA = {
    "P": ["pa", "pi", "pu", "pe", "po"]
}

HANDAKUON_HIRA = {
    "P": ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]
}

COMBOS_KANAS_ROMA = {
    "K": ["kya", "kyu", "kyo"],
    "G": ["gya", "gyu", "gyo"],
    "S": ["sha", "shu", "sho"],
    "J": ["ja", "ju", "jo"],
    "C": ["cha", "chu", "cho"],
    "N": ["nya", "nyu", "nyo"],
    "H": ["hya", "hyu", "hyo"],
    "B": ["bya", "byu", "byo"],
    "P": ["pya", "pyu", "pyo"],
    "M": ["mya", "myu", "myo"],
    "R": ["rya", "ryu", "ryo"]
}

COMBOS_KANAS_HIRA = {
    "K": ["きゃ", "きゅ", "きょ"],
    "G": ["ぎゃ", "ぎゅ", "ぎょ"],
    "S": ["しゃ", "しゅ", "しょ"],
    "J": ["じゃ", "じゅ", "じょ"],
    "C": ["ちゃ", "ちゅ", "ちょ"],
    "N": ["にゃ", "にゅ", "にょ"],
    "H": ["ひゃ", "ひゅ", "ひょ"],
    "B": ["びゃ", "びゅ", "びょ"],
    "P": ["ぴゃ", "ぴゅ", "ぴょ"],
    "M": ["みゃ", "みゅ", "みょ"],
    "R": ["りゃ", "りゅ", "りょ"]
}

rootKanasRoma = []
rootKanasHira = []
rootKanasKata = []


# Flattening each multi-level constant kanas lists
def initFlattenedKanas():
    global rootKanasRoma
    global rootKanasHira
    global rootKanasKata

    # global simpleKanasRoma
    # global simpleKanasHira
    # global dakuonRoma
    # global dakuonHira
    # global handakuonRoma
    # global handakuonHira
    # global combosKanasRoma
    # global combosKanasHira
    # global everyKanasRoma
    # global everyKanasHira

    simpleKanasRoma = []
    simpleKanasHira = []
    simpleKanasKata = []
    dakuonRoma = []
    dakuonHira = []
    dakuonKata = []
    handakuonRoma = []
    handakuonHira = []
    handakuonKata = []
    combosKanasRoma = []
    combosKanasHira = []
    combosKanasKata = []
    everyKanasRoma = []
    everyKanasHira = []
    everyKanasKata = []

    # Simple Kanas
    for line in SIMPLE_KANAS_ROMA:
        for kana in SIMPLE_KANAS_ROMA[line]:
            simpleKanasRoma.append(kana)

    for line in SIMPLE_KANAS_HIRA:
        for kana in SIMPLE_KANAS_HIRA[line]:
            simpleKanasHira.append(kana)

    # Dakuon ゛

    for line in DAKUON_ROMA:
        for kana in DAKUON_ROMA[line]:
            dakuonRoma.append(kana)

    for line in DAKUON_HIRA:
        for kana in DAKUON_HIRA[line]:
            dakuonHira.append(kana)

    # Handakuon ゜

    for line in HANDAKUON_ROMA:
        for kana in HANDAKUON_ROMA[line]:
            handakuonRoma.append(kana)

    for line in HANDAKUON_HIRA:
        for kana in HANDAKUON_HIRA[line]:
            handakuonHira.append(kana)

    # Combos Kanas

    for line in COMBOS_KANAS_ROMA:
        for kana in COMBOS_KANAS_ROMA[line]:
            combosKanasRoma.append(kana)

    for line in COMBOS_KANAS_HIRA:
        for kana in COMBOS_KANAS_HIRA[line]:
            combosKanasHira.append(kana)

    # Every Kanas (combining every previous ones)
    everyKanasRoma = simpleKanasRoma + dakuonRoma + handakuonRoma + combosKanasRoma
    everyKanasHira = simpleKanasHira + dakuonHira + handakuonHira + combosKanasHira
    everyKanasKata = simpleKanasKata + dakuonKata + handakuonKata + combosKanasKata

    # List of lists
    rootKanasRoma = [simpleKanasRoma, dakuonRoma,
                     handakuonRoma, combosKanasRoma, everyKanasRoma]
    rootKanasHira = [simpleKanasHira, dakuonHira,
                     handakuonHira, combosKanasHira, everyKanasHira]
    rootKanasKata = [simpleKanasKata, dakuonKata,
                     handakuonKata, combosKanasKata, everyKanasKata]
