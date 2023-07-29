import re
import os
import csv
csv_filename = 'podjetja.csv'
frontpage_filename = 'glavna.html'
def name(index):
    return 'podjetja{}'.format(index)

def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
def page_to_ads(page_content):
    vzorec = '<a href="/company/.+?</div></li>'
    return re.findall(vzorec, page_content, flags=re.DOTALL)
podjetja_directory = 'podatki'

print(os.listdir())
def get_dict_from_ad_block(block):
    vzorec_ime = 'hreflang="(en|und)">(.+?)</a></h2></div><div'
    vzorec_sedez = 'Headquarters:.+?hreflang="(en|und)">(.+?)</a></strong></div><div'
    vzorec_svetovni_rang = 'World Rank \(Dec-25-2025\): </span><strong class="field-content">(.+?)</strong></div><div'
    vzorec_Market_cap_Dec_2022 = 'Market Cap Dec-25-2022: </span><strong class="field-content">(.+?)</strong></div><div'
    vzorec_World_Rank_Jan_2022 = 'World Rank \(Jan-07-2022\): </span><strong class="field-content">(.+?)</strong></div><div'
    vzorec_Market_Value_Jan_2022 = 'Market Value \(Jan-07-2022\): </span><strong class="field-content">(.+?)</strong></div><div'
    vzorec_kategorija_podjetja = 'Company Category:.+?hreflang="(en|und)">(.+?)</a>'
    vzorec_stevilo_zaposlenih = 'Employee Count: </span><strong class="field-content">(.+?)</strong></div><div'
    vzorec_Letni_dohodek = 'Annual Revenue in USD: </span><strong class="field-content">(.+?)</strong></div><div'
    vzorec_Letni_Neto_dohodek = 'Annual Net Income in USD: </span><strong class="field-content">(.+?)</strong></div><div'

    try:
        ime = re.search(vzorec_ime, block).group(2)
        svetovni_rang_2025 = re.search(vzorec_svetovni_rang, block).group(1)
        
    except AttributeError:
        print(f"Nepopolni vzorci pri (čudnem?) oglasu\n{block}")
        raise
    try:
        sedez = re.search(vzorec_sedez, block, flags=re.DOTALL).group(2)
    except AttributeError:
        sedez = 'None'
    try:
        Market_cap_Dec_2022 = re.search(vzorec_Market_cap_Dec_2022, block, flags=re.DOTALL).group(1)
    except AttributeError:
        Market_cap_Dec_2022 = 'None'
    try:
        World_Rank_Jan_2022 = re.search(vzorec_World_Rank_Jan_2022, block).group(1)
    except AttributeError:
        World_Rank_Jan_2022 = 'None'
    try:
        World_Market_Value_Jan_2022 = re.search(vzorec_Market_Value_Jan_2022, block).group(1)
    except AttributeError:
        World_Market_Value_Jan_2022 = 'None'
    try:
        Kategorija = re.search(vzorec_kategorija_podjetja, block).group(2)
    except AttributeError:
        Kategorija = 'None'
    try:
        zaposleni = re.search(vzorec_stevilo_zaposlenih, block).group(1)
    except AttributeError:
        zaposleni = 'None'
    try:
        letni_dohodek = re.search(vzorec_Letni_dohodek, block).group(1)
    except AttributeError:
        letni_dohodek = 'None'
    try:
        Neto_dohodek = re.search(vzorec_Letni_Neto_dohodek, block).group(1)
    except AttributeError:
        Neto_dohodek = 'None'
    
    return {"ime": ime, "Sedež": sedez, "Svetovni rang 2025": svetovni_rang_2025, 'Tržna kapitalzicija Dec-25-2022': Market_cap_Dec_2022, 'Svetovni rang Jan 2022': World_Rank_Jan_2022, 'Tržna vrednost Jan 2022': World_Market_Value_Jan_2022, 'Kategorija': Kategorija, 'Število zaposlenih': zaposleni, 'Letni dohodek':
            letni_dohodek, 'Neto dohodek': Neto_dohodek}
for i in range(0,20):
    vsebina = read_file_to_string(podjetja_directory, name(i))
    podjetja = page_to_ads(vsebina)
 

def ads_from_file(filename, directory):
    vsebina = read_file_to_string(directory, filename)
    podjetja = page_to_ads(vsebina)
    slovarji = []
    for podjetje in podjetja:
        slovarji.append(get_dict_from_ad_block(podjetje))
        print(slovarji)
    return slovarji
def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    # ko odpremo datoteko, podamo neobevzni argument newline in ga nastavimo na prazen niz,
    # sicer bomo na windowsih imeli grd csv, kjer bo vsaki dejanski vrstici sledila prazna
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return
def write_podjetja_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
    slovarjev parametra ads enaki in je seznam ads neprazen."""
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugače pa sproži napako
    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
    # produkcijskem okolju
    assert ads and (all(slovar.keys() == ads[0].keys() for slovar in ads))
    write_csv(ads[0], ads, directory, filename)

for i in range(0,20):
    if i == 0:
        vsi_slovarji = []
    vsi_slovarji += ads_from_file(name(i), podjetja_directory)
write_podjetja_ads_to_csv(vsi_slovarji, "obdelani_podatki", csv_filename)