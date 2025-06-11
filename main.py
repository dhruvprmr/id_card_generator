import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

TEMPLATE="ute_id_template.png"
CSV_FILE="employee.csv"
PROFILE_PICTURE="profile_images"
OUTPUT_PDF="employee_id.pdf"

ID_WIDTH, ID_HEIGHT = 325, 204
PHOTO_SIZE = (110, 110)
PHOTO_POSITION = (180, 25)
NAME_POSITION = (20, 170)

TITLE_POSITION = 20
TITLE_FONT_SIZE = 12
TITLE_POSITION_OFFSET_Y = 20
FONT_SIZE = 14
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TEXT_COLOR = "white"

#Reading the data from csv
employees = pd.read_csv(CSV_FILE).to_dict(orient='records')

#Initializing PDF creation
pdf = FPDF(unit='pt', format=[ID_WIDTH, ID_HEIGHT])

for i in range(len(employees)):
    name = employees[i]['name']
    title = employees[i]['title']
    profile_path = os.path.join(PROFILE_PICTURE, employees[i]['profile'])

    id_template = Image.open(TEMPLATE)

    try:
        photo = Image.open(profile_path).resize(PHOTO_SIZE)
        id_template.paste(photo, PHOTO_POSITION)
    except FileNotFoundError:
        continue

    #Drawing the data on template
    draw = ImageDraw.Draw(id_template)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    title_font = ImageFont.truetype(FONT_PATH, TITLE_FONT_SIZE)

    draw.text(NAME_POSITION, name, fill=TEXT_COLOR, font=font)

    title_position = (ID_WIDTH - 150, NAME_POSITION[1])
    draw.text(title_position, title, fill=TEXT_COLOR, font=title_font)
    
    temp_image_path = f"temp_{i}.png"
    id_template.save(temp_image_path)

    pdf.add_page()
    pdf.image(temp_image_path, x=0, y=0, w=ID_WIDTH, h=ID_HEIGHT)

    os.remove(temp_image_path)

pdf.output(OUTPUT_PDF)