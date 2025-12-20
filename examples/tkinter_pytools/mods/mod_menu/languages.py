from .theme import ACTIVE_WINDOWS

TRANSLATIONS = {
    "English (Default)": {},
    "Japanese": {
        # Titles
        "Text Analyzer": "文字数アナライザー",
        "Hash Gen": "ハッシュ生成機",
        "Epoch Converter": "Unix時間変換",
        "UUID Gen": "UUID発行",
        # Buttons
        "Analyze": "解析実行",
        "Clear": "クリア",
        "Generate Hashes": "ハッシュ計算",
        "Epoch To Datetime": "Unix時間 → 日時",
        "Datetime To Epoch": "日時 → Unix時間",
        "Generate UUID": "UUIDを生成",
        "Close": "閉じる",
        # Labels & Messages
        "Characters: 0 | Words: 0 | Lines: 0": "文字数: 0 | 単語数: 0 | 行数: 0",
        "MD5: -": "MD5: (未計算)",
        "SHA256: -": "SHA256: (未計算)",
        "Epoch Seconds:": "Unixタイムスタンプ (秒):",
        "Datetime (UTC, YYYY-MM-DD HH:MM:SS):": "日時 (UTC):",
        "Awaiting conversion...": "変換待機中...",
        "Press the button to get a UUID v4.\nIt will be copied to the clipboard.": "ボタンを押すとUUID v4を生成し、\nクリップボードにコピーします。",
        "Nothing generated yet.": "まだ生成されていません。",
        "Input Text:": "テキストを入力:",
        # Modded Messages
        "Copy Hash": "コピー",
        "Copied!": "コピー完了!",
        "No hash to copy.": "空欄です",
    },
    "German": {
        # Titles
        "Text Analyzer": "Textanalyse",
        "Hash Gen": "Hash-Generator",
        "Epoch Converter": "Unix-Zeitkonverter",
        "UUID Gen": "UUID-Erstellung",
        # Buttons
        "Analyze": "Analysieren",
        "Clear": "Löschen",
        "Generate Hashes": "Hashes Generieren",
        "Epoch To Datetime": "Unix → Datum",
        "Datetime To Epoch": "Datum → Unix",
        "Generate UUID": "UUID Generieren",
        "Close": "Schließen",
        # Labels
        "Characters: 0 | Words: 0 | Lines: 0": "Zeichen: 0 | Wörter: 0 | Zeilen: 0",
        "MD5: -": "MD5: (Ausstehend)",
        "SHA256: -": "SHA256: (Ausstehend)",
        "Epoch Seconds:": "Unix-Zeitstempel (Sek):",
        "Datetime (UTC, YYYY-MM-DD HH:MM:SS):": "Datum (UTC):",
        "Awaiting conversion...": "Warte auf Konvertierung...",
        "Press the button to get a UUID v4.\nIt will be copied to the clipboard.": "Drücken Sie die Taste für UUID v4.\nIn die Zwischenablage kopiert.",
        "Nothing generated yet.": "Noch nichts generiert.",
        "Input Text:": "Texteingabe:",
        # Modded Messages
        "Copy Hash": "Kopieren",
        "Copied!": "Kopiert!",
        "No hash to copy.": "Kein Hash.",
    },
}

CURRENT_LANGUAGE = "English (Default)"


def switch_global_language(lang_name):
    global CURRENT_LANGUAGE
    if lang_name not in TRANSLATIONS:
        return

    CURRENT_LANGUAGE = lang_name
    print(f"[Mod] Global language switch: {lang_name}")

    for win in list(ACTIVE_WINDOWS):
        try:
            if win.winfo_exists():
                retranslate_recursive(win, lang_name)
        except Exception:
            pass


def retranslate_recursive(widget, lang_name):
    try:
        if not hasattr(widget, "_uml_original_text"):
            try:
                original = widget.cget("text")
                widget._uml_original_text = original
            except Exception:
                widget._uml_original_text = None

        original_text = widget._uml_original_text
        if original_text:
            trans_dict = TRANSLATIONS[lang_name]
            if original_text in trans_dict:
                widget.configure(text=trans_dict[original_text])
            else:
                widget.configure(text=original_text)

    except Exception:
        pass

    for child in widget.winfo_children():
        retranslate_recursive(child, lang_name)
