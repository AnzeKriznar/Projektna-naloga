import download
import podatki
import os
def main(redownload=True, reparse=True):

    
    for i in range(20):
        filename = f"podjetja{i}.html"
        pot_html = os.path.join(podatki.podjetja_directory, filename)
        if redownload or not os.path.exists(pot_html):

            download.save_frontpage(download.url(i), download.podjetja_directory, download.name(i))
    csv_mapa = "obdelani_podatki"
    pot_csv = os.path.join(csv_mapa, podatki.csv_filename)

    if reparse or not os.path.exists(pot_csv):

        for i in range(0,20):
            if i == 0:
                vsi_slovarji = []
            vsi_slovarji += podatki.ads_from_file(podatki.name(i), podatki.podjetja_directory)
            podatki.write_podjetja_ads_to_csv(vsi_slovarji, "obdelani_podatki", podatki.csv_filename)
    else:
        print(f"Datoteka {pot_csv} že obstaja")