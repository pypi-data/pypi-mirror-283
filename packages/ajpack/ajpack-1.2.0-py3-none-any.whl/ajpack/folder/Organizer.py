import os, shutil, ajpack # type:ignore

def get_files() -> list[str]:
    script_name: str = os.path.basename(__file__)
    return [f for f in os.listdir() if os.path.isfile(f) and f != script_name and f != "Organizer.exe"]

def sort(files: list[str]) -> None:
    # Create a dictionary that holds the file extensions
    file_extensions: dict[str, str] = {
        # Documents
        "pdf": "PDFs",
        "doc": "Word-Documents",
        "docx": "Word-Documents",
        "xlsx": "Excel-Spreadsheets",
        "csv": "Excel-Spreadsheets",
        "ppt": "PowerPoint-Presentations",
        "pptx": "PowerPoint-Presentations",
        "odt": "OpenDocument-Text",
        "ods": "OpenDocument-Spreadsheets",
        "odp": "OpenDocument-Presentations",
        "rtf": "Rich-Text-Files",
        "md": "Markdown-Files",
        "epub": "eBooks",
        "mobi": "eBooks",
        "tex": "LaTeX-Documents",
        "xps": "XML-Paper-Specification",
        "abw": "AbiWord-Documents",
        "djvu": "DjVu-Documents",
        "fb2": "FictionBook",
        "chm": "Compiled-HTML-Help",
        "ibooks": "iBooks",
        "lit": "Microsoft-Reader",
        "azw": "Amazon-Kindle-eBook",
        "azw3": "Amazon-Kindle-eBook",
        "docm": "Word-Macro-Enabled-Documents",
        "xlsm": "Excel-Macro-Enabled-Spreadsheets",

        # Images
        "jpg": "Images",
        "jpeg": "Images",
        "png": "Images",
        "gif": "Images",
        "bmp": "Images",
        "tiff": "Images",
        "svg": "Vector-Images",
        "webp": "Images",
        "heic": "High-Efficiency-Images",
        "psd": "Photoshop-Documents",
        "ai": "Adobe-Illustrator-Files",
        "raw": "Raw-Image-Files",
        "dng": "Digital-Negative-Images",
        "cr2": "Canon-Raw-Images",
        "nef": "Nikon-Raw-Images",
        "arw": "Sony-Raw-Images",
        "orf": "Olympus-Raw-Images",
        "rw2": "Panasonic-Raw-Images",
        "3fr": "Hasselblad-Raw-Images",
        "pef": "Pentax-Raw-Images",
        "sr2": "Sony-Raw-Images",
        "x3f": "Sigma-Raw-Images",
        "raf": "Fuji-Raw-Images",

        # Icons
        "ico": "Icons",
        "icns": "Icons",
        "svg": "Vector-Images",
        "cur": "Cursor-Files",

        # Music
        "mp3": "Music",
        "wav": "Music",
        "flac": "Music",
        "aac": "Music",
        "ogg": "Music",
        "m4a": "Music",
        "wma": "Windows-Media-Audio",
        "aiff": "Audio-Interchange-File-Format",
        "alac": "Apple-Lossless-Audio",
        "mid": "MIDI-Files",
        "midi": "MIDI-Files",
        "mod": "Module-Files",
        "xm": "Extended-Module-Files",
        "it": "Impulse-Tracker-Files",
        "s3m": "Scream-Tracker-Files",

        # Videos
        "mp4": "Videos",
        "avi": "Videos",
        "mov": "Videos",
        "flv": "Videos",
        "wmv": "Videos",
        "mkv": "Videos",
        "webm": "Videos",
        "m4v": "Videos",
        "3gp": "Mobile-Video-Files",
        "mts": "AVCHD-Video-Files",
        "m2ts": "Blu-ray-Video-Files",
        "vob": "DVD-Video-Objects",
        "rm": "RealMedia",
        "rmvb": "RealMedia-Variable-Bitrate",
        "ogv": "Ogg-Video",
        "asf": "Advanced-Systems-Format",
        "f4v": "Flash-Video",
        "swf": "Shockwave-Flash",
        "mxf": "Material-Exchange-Format",

        # Archives
        "zip": "Compressed-Files",
        "rar": "Compressed-Files",
        "7z": "Compressed-Files",
        "tar": "Compressed-Files",
        "gz": "Compressed-Files",
        "bz2": "Compressed-Files",
        "xz": "Compressed-Files",
        "iso": "ISO-Files",
        "dmg": "Disk-Image-Files",
        "tgz": "Compressed-Files",
        "lz": "Compressed-Files",
        "lzma": "Compressed-Files",
        "cab": "Windows-Cabinet-Files",
        "z": "Unix-Compressed-Files",
        "cpio": "Unix-Cpio-Archive",
        "ar": "Unix-Archive",
        "rpm": "Red-Hat-Package-Manager-Files",
        "deb": "Debian-Package-Files",
        "pkg": "MacOS-Package",
        "xar": "XAR-Archive",

        # Scripts
        "exe": "Executables",
        "sh": "Shell-Scripts",
        "bat": "Batch-Files",
        "cmd": "Command-Files",
        "ps1": "PowerShell-Scripts",
        "txt": "Text-Files",
        "md": "Markdown-Files",
        "rtf": "Rich-Text-Files",
        "py": "Python-Scripts",
        "java": "Java-Files",
        "class": "Java-Class-Files",
        "jar": "Java-Archive-Files",
        "cpp": "C++-Files",
        "c": "C-Files",
        "cs": "C#-Files",
        "js": "JavaScript-Files",
        "ts": "TypeScript-Files",
        "html": "HTML-Files",
        "htm": "HTML-Files",
        "css": "CSS-Files",
        "json": "JSON-Files",
        "xml": "XML-Files",
        "yaml": "YAML-Files",
        "yml": "YAML-Files",
        "php": "PHP-Files",
        "rb": "Ruby-Files",
        "pl": "Perl-Files",
        "swift": "Swift-Files",
        "go": "Go-Files",
        "rs": "Rust-Files",
        "r": "R-Scripts",
        "m": "MATLAB-Files",
        "vbs": "VBScript-Files",
        "lua": "Lua-Files",
        "as": "ActionScript-Files",
        "jsp": "JavaServer-Pages",
        "asp": "Active-Server-Pages",
        "scm": "Scheme-Scripts",
        "clj": "Clojure-Scripts",
        "fs": "F#-Files",
        "erl": "Erlang-Files",
        "hs": "Haskell-Files",
        "jl": "Julia-Files",
        "tsx": "TypeScript-React-Files",
        "jsx": "JavaScript-React-Files",
        "scala": "Scala-Files",
        "groovy": "Groovy-Scripts",
        "kt": "Kotlin-Files",
        "mjs": "JavaScript-Module-Files",
        "coffee": "CoffeeScript-Files",
        "litcoffee": "Literate-CoffeeScript-Files",
        "rsx": "Rust-React-Files",

        # Fonts
        "ttf": "Fonts",
        "otf": "Fonts",
        "woff": "Web-Fonts",
        "woff2": "Web-Fonts",
        "eot": "Embedded-OpenType-Fonts",
        "fon": "Bitmap-Fonts",
        "fnt": "Font-Files",
        "pfa": "Printer-Font-ASCII",
        "pfb": "Printer-Font-Binary",
        "pfm": "Printer-Font-Metrics",
        "afm": "Adobe-Font-Metrics",

        # Miscellaneous
        "log": "Log-Files",
        "dat": "Data-Files",
        "db": "Database-Files",
        "sql": "SQL-Files",
        "sqlite": "SQLite-Database-Files",
        "accdb": "Access-Database-Files",
        "mdb": "Access-Database-Files",
        "bak": "Backup-Files",
        "tmp": "Temporary-Files",
        "torrent": "Torrent-Files",
        "ics": "Calendar-Files",
        "msg": "Outlook-Mail-Files",
        "eml": "Email-Files",
        "vcf": "vCard-Files",
        "ics": "iCalendar-Files",
        "key": "Keynote-Presentations",
        "numbers": "Numbers-Spreadsheets",
        "pages": "Pages-Documents",
        "opml": "Outline-Processor-Markup-Language",
        "srt": "SubRip-Subtitle-Files",
        "sub": "Subtitle-Files",
        "vtt": "WebVTT-Files",
        "sbv": "YouTube-Subtitle-Files",
        "ass": "Aegisub-Advanced-Substation",
        "ssa": "Substation-Alpha",
        "jsonl": "JSON-Lines",
        "parquet": "Parquet-Files",
        "avro": "Avro-Files",
        "orc": "Optimized-Row-Columnar",
        "har": "HTTP-Archive",
        "pcap": "Packet-Capture-Files",
        "cap": "Packet-Capture-Files",
        "dmp": "Memory-Dump-Files",
        "dump": "Dump-Files",
        "url": "Links",
        "lnk": "Links",
        "apk": "Android_APKs",
        "xcf": "Gimp"
    }

    def del_if_exist(file: str, folder: str) -> bool:
        if os.path.exists(os.path.join(file, folder)): os.remove(file); return True
        else: return False

    for file in files:
        try:
            print(ajpack.colored_text(f"Sorting file {os.path.basename(file)}...", "green"))

            if os.path.splitext(file)[1][1::].lower() in file_extensions.keys():
                folder: str = file_extensions[os.path.splitext(file)[1][1::].lower()]

                if del_if_exist(file, folder): continue

                if not os.path.exists(folder): os.makedirs(folder)

                shutil.move(file, folder)
            else:
                folder= "Unknown_Filetypes"

                if del_if_exist(file, folder): continue

                if not os.path.exists(folder): os.makedirs(folder)
                    
                shutil.move(file, folder)
        except Exception as e: print(ajpack.colored_text(f"There was an error while sorting the file {os.path.basename(file)} --> {e}", "red"))

def main() -> None:
    files = get_files()
    sort(files)

if __name__ == "__main__":
    main()