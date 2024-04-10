print('start')
import os
import sqlite3
import xml.etree.ElementTree as ET
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
print(current_directory)
# Function to extract speaker information
def get_speaker_info(speaker):
    name = speaker.get("naam")
    party = speaker.get("partij")
    return name, party

# Creating SQLite database
db_file = "speeches.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Creating table in the database
cursor.execute('''CREATE TABLE IF NOT EXISTS speeches
                  (file_name TEXT,date TEXT, speaker_name TEXT, party TEXT, category TEXT, title TEXT, speech TEXT)''')

conn.commit()

def process_files(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml'):
                    print(file)
                    file_path = os.path.join(root, file)
                    tree = ET.parse(file_path)
                    root_elem = tree.getroot()
                    # Extracting date
                    try:
                        date_element = root_elem.find(".//meta[@name='OVERHEIDop.datumVergadering']")
                        date = date_element.get("content") if date_element is not None else ""
                    except Exception as e:
                        print(f"Error extracting date from XML file {file_path}: {str(e)}")
                        date = ""

                    # Extracting category
                    try:
                        category_element = root_elem.find(".//meta[@name='OVERHEID.category']")
                        category = category_element.get("content") if category_element is not None else ""
                    except Exception as e:
                        print(f"Error extracting category from XML file {file_path}: {str(e)}")
                        category = ""
                    
                    # Extracting title
                    try:
                        title_element = root_elem.find(".//meta[@name='DC.title']")
                        title = title_element.get("content") if title_element is not None else ""
                    except Exception as e:
                        print(f"Error extracting title from XML file {file_path}: {str(e)}")
                        title = ""
                    # Get file name
                    file_name = file
                    speeches = root_elem.findall(".//spreekbeurt")
                    for speech in speeches:
                         speaker_name, party = get_speaker_info(speech)
                         if not speaker_name:
                            try:
                                speaker_name=speech.find("spreker/naam/achternaam").text.strip() #if speech_content_element is not None else ""  
                            except:
                                speaker_name=speech.find("spreker").text.strip() #if speech_content_element is not None else ""  
                         speech_content_element = speech.find("tekst/al")
                         speech_content = speech_content_element.text.strip() if speech_content_element is not None else ""
                         if not speech_content:
                            tekst_elements = speech.findall("tekst")
                            
                            speech_content_elements = []
                            for tekst_element in tekst_elements:
                                speech_content_groep_elements = tekst_element.findall("al-groep")
                                for speech_content_groep_element in speech_content_groep_elements:
                                    al_elements = speech_content_groep_element.findall("al")
                                    for al_element in al_elements:
                                        speech_content_elements.append(al_element.text.strip() if al_element.text is not None else "")
                                    # for al_element in al_elements:
                                    #     text = al_element.text.strip() if al_element.text is not None else ""
                                    #     tail = al_element.tail.strip() if al_element.tail is not None else ""
                                    #     speech_content_elements.append(text + tail)
                            speech_content = " ".join(speech_content_elements)
                            





                         if not speech_content:
                             speech_content_element = speech.find("tekst/motie/al")
                             speech_content = speech_content_element.text.strip() if speech_content_element is not None else ""



                             
                             
                         cursor.execute("INSERT INTO speeches (file_name,date, speaker_name, party, category, title, speech) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                        (file_name,date, speaker_name, party, category, title, speech_content))
                         conn.commit()



# Path to the root folder with XML files
data_folder = 'xml_data'
# Call the function to process the files
process_files(data_folder)

# Close the database connection
conn.close()
