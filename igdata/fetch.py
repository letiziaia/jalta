import json
import re
import emoji
from datetime import datetime
from langdetect import detect

record = open("igdata.tsv", "w+", encoding="utf-8")
record.writelines(
    "Timestamp\tLanguage\tHashtags\tMentioned\tEmojies\tContent\n")

for f in range(16):
    with open(str(f)+".json") as json_file:
        data = json.load(json_file)
        edges1 = data["data"]["location"]["edge_location_to_media"]["edges"]
        edges2 = data["data"]["location"]["edge_location_to_top_posts"]["edges"]
        edges = edges1 + edges2
        for edge in edges:
            content = ""
            hashtags = set()
            emojis = set()
            language = "fi"
            mentioned = set()
            timestamp = "NA"
            try:
                # Content analysis
                content = edge["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                emojis = set([c for c in content if c in emoji.UNICODE_EMOJI])
                language = detect(content)
                hashtags = set([x.strip()
                                for x in re.findall(r"#(\w+)", content)])
                mentioned = set([x.strip()
                                 for x in re.findall(r"@(\w+)", content)])
            except Exception:
                pass
            try:
                timestamp = edge["node"]["taken_at_timestamp"]
                timestamp = datetime.utcfromtimestamp(
                    timestamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass

            line = [timestamp, language, " ".join(hashtags), " ".join(
                mentioned), " ".join(emojis), " ".join(content.split())]
            record.writelines("\t".join(line)+"\n")
