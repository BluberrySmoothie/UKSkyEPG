import csv
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from xml.dom import minidom  # Import minidom for pretty-printing XML

def fetch_epg_data(channel_number, date):
    url = f"https://awk.epgsky.com/hawk/linear/schedule/{date}/{channel_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {channel_number} on {date}")
        return None

def create_xmltv(channels, epg_data):
    tv = ET.Element("tv")
    for channel in channels:
        channel_elem = ET.SubElement(tv, "channel", id=channel["tvg-id"])
        ET.SubElement(channel_elem, "display-name").text = channel["tvg-id"]
    
    for channel_id, programmes in epg_data.items():
        for prog in programmes:
            if "st" not in prog:
                print(f"Skipping programme due to missing 'st' key: {prog}")
                continue
            
            # Use timezone-aware datetime objects (UTC)
            start_time = datetime.fromtimestamp(prog["st"], tz=timezone.utc).strftime('%Y%m%d%H%M%S')
            stop_time = datetime.fromtimestamp(prog["st"] + prog.get("d", 0), tz=timezone.utc).strftime('%Y%m%d%H%M%S')
            
            prog_elem = ET.SubElement(tv, "programme", {
                "start": start_time,
                "stop": stop_time,
                "channel": channel_id
            })
            
            # Ensure all elements are strings when added to XML
            ET.SubElement(prog_elem, "title").text = str(prog.get("t", "Unknown Title"))
            ET.SubElement(prog_elem, "desc").text = str(prog.get("sy", ""))
            ET.SubElement(prog_elem, "category").text = str(prog.get("eg", ""))
            ET.SubElement(prog_elem, "rating").text = str(prog.get("r", ""))
            
            if "seasonnumber" in prog and "episodenumber" in prog:
                season = int(prog["seasonnumber"]) - 1
                episode = int(prog["episodenumber"]) - 1
                episode_elem = ET.SubElement(prog_elem, "episode-num", system="xmltv_ns")
                episode_elem.text = str(f"{season}.{episode}.0")
    
    # Create ElementTree from the XML structure
    tree = ET.ElementTree(tv)
    
    # Use minidom to pretty-print the XML
    xml_str = minidom.parseString(ET.tostring(tv)).toprettyxml(indent="  ")
    
    # Write the formatted XML to a file
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

def main():
    csv_file = "SkyChannels.csv"  # Update with actual file name
    channels = []
    
    # Read channel data from CSV
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            channels.append({"channel": row[0], "tvg-id": row[1]})
    
    epg_data = {}
    for i in range(9):  # Today + 8 days
        date = (datetime.now() + timedelta(days=i)).strftime('%Y%m%d')
        for channel in channels:
            print(f"Fetching data for Channel: {channel['channel']}, TVG-ID: {channel['tvg-id']}, Date: {date}")
            json_data = fetch_epg_data(channel["channel"], date)
            if json_data:
                schedule = json_data.get("schedule", [])
                if not schedule or not schedule[0].get("events"):
                    print(f"No programme data available for Channel: {channel['channel']}, Date: {date}")
                    continue
                for prog in schedule[0].get("events", []):
                    if "st" not in prog:
                        print(f"Missing 'st' key in programme data for Channel: {channel['channel']}, Date: {date}, Programme: {prog}")
                        continue
                    epg_data.setdefault(channel["tvg-id"], []).append({
                        "st": prog["st"],
                        "d": prog.get("d", 0),
                        "t": prog.get("t", "Unknown Title"),
                        "sy": prog.get("sy", ""),
                        "eg": prog.get("eg", ""),
                        "r": prog.get("r", ""),
                        "seasonnumber": prog.get("seasonnumber", 0),
                        "episodenumber": prog.get("episodenumber", 0)
                    })
    
    # Create XMLTV file
    create_xmltv(channels, epg_data)
    print("EPG XML file generated: epg.xml")

if __name__ == "__main__":
    main()
