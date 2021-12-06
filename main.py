from flask import Flask, request, send_file, render_template, redirect, url_for
import requests
from PIL import Image, ImageDraw, ImageFont
import time
import barcode
from barcode.writer import ImageWriter

from forms import BarcodeForm
from models import db, Barcode

app = Flask(__name__)
app.config['SECRET_KEY']='73870e7f-634d-433b-946a-8d20132bafac'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/main.db'

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    form =  BarcodeForm()
    return render_template('index.html', form=form)

@app.route('/', methods=['POST'])
def index_post():
    form = BarcodeForm()
    if request.method == 'POST':
        brand = form.brand.data
        article = form.article.data
        size = form.size.data
        weigth = form.weigth.data
        barcode_name = form.barcode.data
        barcode_db = Barcode(brand=brand, article=article, size=size, weigth=weigth, barcode=barcode_name)
        db.session.add(barcode_db)
        db.session.commit()

        ean = barcode.get(barcode_name, str(article), writer=ImageWriter())
        filename = ean.save('base_img/ean13')

        img_base = Image.new('RGB', (1976, 1292), color=('#FFFFFF'))
        font = ImageFont.truetype('timesnewromanpsmt.ttf', size=70)
        img_base.save("base_img/base_img.jpg")

        img1 = Image.new('RGB', (700, 300), color=('#FFFFFF'))
        draw_text = ImageDraw.Draw(img1)
        draw_text.text((100, 5),text=f'Размер:{size}', font=font, fill=('#1C0606'), align='center')
        draw_text.text((100, 75), text=f'Бренд:{brand}', font=font, fill=('#1C0606'), align='center')
        draw_text.text((100, 145), text=f'Вес:{weigth}', font=font, fill=('#1C0606'), align='center')

        img2=Image.open('base_img/ean13.png')
        img2 = img2.resize((1400, 900), resample=0, box=None)

        img_base.paste(img1, (638, 1000))
        img_base.paste(img2,(288, 100))
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        img_base.save(f'barcodes/{brand}-{article}.jpg')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
