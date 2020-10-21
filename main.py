import requests
import parsel
import json
import pathlib

def scrape_site(makerspace_data_text):
  top_selector = parsel.Selector(makerspace_data_text)

  columns = top_selector.xpath("//div[@class='row']/div[@class='col-11 col-md-6 col-lg border']")



  output_list = []

  for column in columns:
    output_dict = {}
    datum = column.xpath(".//h6/text()").get()
    
    output_dict['datum'] = datum

    rows_data = column.xpath(".//div/a/span/text()").getall()
    row_dicts = []


    index = 0
    anzahl = ""
    uhrzeit = ""
    for row in rows_data: 
      index = index + 1 
      if index % 2 == 0:
        anzahl = row

      if index % 2 != 0:
        uhrzeit = row

      if uhrzeit != "" and anzahl != "":
        row_dict = {}
        row_dict['anzahl'] = anzahl
        anzahl = ""
        row_dict['uhrzeit'] = uhrzeit
        uhrzeit = ""
        row_dicts.append(row_dict)
    
    
    output_dict['rows'] = row_dicts
    output_list.append(output_dict)
    output_dict = {}

  return output_list


output = []
for i in range(20):
  print(i)
  makerspace_data = requests.get(f"https://makerspace.experimenta.science/anmeldung/?offset=-{i}").text

  output.append(scrape_site(makerspace_data))


json_data = json.dumps(output)
output_path = pathlib.Path('./test.json')
output_path.write_text(json_data)