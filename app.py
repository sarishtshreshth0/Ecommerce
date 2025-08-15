from flask import Flask , request, render_template_string ,render_template, send_file, session, flash, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from PIL import Image, ImageFont, ImageDraw
import os
import img2pdf
import datetime
from uuid import uuid4
from random import randint

uri = "mongodb+srv://sarishtshreshth:openforall@cluster0.sf3lhpf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db  = client['frontpage']
db_college = db['college']
db_blog = db['blog']

SALT = randint(1, 1000000)

app = Flask(__name__)
app.config['SECRET_KEY'] = str(SALT)

@app.route('/key')
def key():
    return f'{int(7478) ^ int(SALT)}'

admins = {
    'prince' : key(),
}

blog_posts = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in admins and admins[username] == password:
            session['admin'] = username
            flash("Logged in successfully.", "success")
            return redirect(url_for('admin_dashboard'))
        flash("Invalid credentials.", "danger")
    return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash("Title and content are required.", "danger")
            return redirect(url_for('admin_dashboard'))
        blog_posts.append({
            'id': str(uuid4()),
            'title': title,
            'content': content,
            'author': session['admin'],
            'media': request.files.get('media'),
            'date_posted': datetime.datetime.now()
        })
        db_blog.insert_one({
            'title': title,
            'content': content,
            'author': session['admin'],
            'date_posted': datetime.datetime.now()
        })
        flash("Blog post added.", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin.html', blogs=blog_posts)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route("/blogs")
def display_blogs():
    return render_template("blogs.html", blogs=db_blog.find())



@app.route("/search")
def search():
    query = request.args.get("q","").lower()
    collegelist = [p['college'] for p in db_college.find() if query in p['college'].lower()]
    collegelist = collegelist[0:5]
    return render_template("_result.html",collegelist = collegelist)

#(@app.route("/select/<college>")
#def select_college(college):
    # Yeh updated input plus preview trigger return karega
 #   html = f"""
  #<input type="text" id="college-input" name="college" placeholder="College Name" 
   #        value="{college}" 
    #       hx-get="/show" hx-target="#show" hx-trigger="keyup changed delay:0ms"
     #      hx-include="#user-form" autocomplete="off">
    
   # <div hx-get="/show" hx-trigger="load" hx-target="#show" hx-include="#user-form"></div>
    #"""# auto trigger once loaded
    #return html) 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/maker')
def maker():
    return render_template('show.html')

@app.route('/maker2')
def maker2():
    return render_template('show_2.html')

@app.route('/maker3')
def maker3():
    return render_template('show_3.html')

@app.route('/show')
def show():
    data = {
        'name': request.args.get('name', ''),
        'subject': request.args.get('subject', ''),
        'rollno': request.args.get('rollno', ''),
        'session': request.args.get('session', ''),
        'branch': request.args.get('branch', ''),
        'subjectcode': request.args.get('subjectcode', ''),
        'sem': request.args.get('sem', ''),
        'year': request.args.get('year', ''),
        'college': request.args.get('college', '')
    }

    if any(data.values()):
        return render_template_string("""
            {% if college %}<h2><p><strong></strong> {{ college }}</p><br></h2>{% endif %}                    
            {% if name %}<p><strong>Name:</strong> {{ name }}</p><br>{% endif %}
            {% if branch %}<p><strong>Branch:</strong> {{ branch }}</p><br>{% endif %}
            {% if year %}<p><strong>Year:</strong> {{ year }}</p><br>{% endif %}
            {% if sem %}<p><strong>Semester:</strong> {{ sem }}</p><br>{% endif %}
            {% if rollno %}<p><strong>Roll No:</strong> {{ rollno }}</p><br>{% endif %}
            {% if subject %}<p><strong>Subject:</strong> {{ subject }}</p><br>{% endif %}
            {% if subjectcode %}<p><strong>Subject-Code:</strong> {{ subjectcode }}</p><br>{% endif %}
            {% if session %}<p><strong>Session:</strong> {{ session }}</p><br>{% endif %}
        """, **data)
    return ""

@app.route('/show_3')
def show_3():
    data = {
        'name': request.args.get('name', ''),
        'department': request.args.get('department', ''),
        'supervisor': request.args.get('supervisor', ''),
        'supervisor_department': request.args.get('supervisor_department', ''),
        'title': request.args.get('title', ''),
        'subtitle': request.args.get('subjectcode', ''),
        'college': request.args.get('college', ''),
        'address': request.args.get('address', '')
    }

    if any(data.values()):
        return render_template_string("""
            {% if college %}<h2><p><strong></strong> {{ college }}</p><br></h2>{% endif %}                    
            {% if name %}<p><strong>Name:</strong> {{ name }}</p><br>{% endif %}
            {% if department %}<p><strong>Department:</strong> {{ department }}</p><br>{% endif %}
            {% if supervisor %}<p><strong>Year:</strong> {{ supervisor }}</p><br>{% endif %}
            {% if supervisor_department %}<p><strong>Supervisor's Department:</strong> {{ supervisor_department }}</p><br>{% endif %}
            {% if title %}<p><strong>Roll No:</strong> {{ title }}</p><br>{% endif %}
            {% if subtitle %}<p><strong>Subject:</strong> {{ subtitle }}</p><br>{% endif %}
            {% if address %}<p><strong>Subject-Code:</strong> {{ address }}</p><br>{% endif %}
        """, **data)
    return ""


@app.route('/show2')
def show2():
    data = {
        'doctor': request.args.get('doctor', ''),
        'designation': request.args.get('designation', ''),
        'contact': request.args.get('contact', ''),
        'hospital': request.args.get('hospital', ''),
        'address': request.args.get('address', '')

    }

    if any(data.values()):
        return render_template_string("""
            {% if hospital %}<h2><p><strong></strong> {{ hospital }}</p><br></h2>{% endif %}                    
            {% if doctor %}<p><strong>Doctor:</strong> {{ doctor }}</p><br>{% endif %}
            {% if designation %}<p><strong>Designation:</strong> {{ designation }}</p><br>{% endif %}
            {% if contact %}<p><strong>Contact:</strong> {{ contact }}</p><br>{% endif %}
            {% if address %}<p><strong>Address:</strong> {{ address }}</p><br>{% endif %}
        """, **data)
    return ""


@app.route("/select/<college>")
def select_college(college):
    # Yeh updated input plus preview trigger return karega
    html = f"""
    <input type="text" id="college" name="college" placeholder="College Name" 
           value="{college}" 
           hx-get="/show" hx-target="#results" hx-trigger="keyup changed delay:0ms"
           hx-include="#user-form" autocomplete="off">
    
    <div hx-get="/show" hx-trigger="load" hx-target="#results" hx-include="#user-form"></div>
    """# auto trigger once loaded
    return html

@app.route('/download')
def generate_certificate():
    college = request.args.get('college', '')
    name = request.args.get('name', '')
    stream = request.args.get('branch', '')
    year = request.args.get('year', '')
    sem = request.args.get('sem', '')
    roll = request.args.get('rollno', '')
    papername = request.args.get('subject', '')
    papercode = request.args.get('subjectcode', '')
    session = request.args.get('session', '')
    template_path = r"static/Cover.jpg"
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    font_path = r"static/DroidSans-Bold.ttf"
    # college_font = ImageFont.truetype(font_path, 130)
    name_font = ImageFont.truetype(font_path, 100)
    other_font = ImageFont.truetype(font_path, 80)
    # college_position = (100, 300)
    # name_position = (1100, 540)
    # stream_position = (1100, 850)
    # year_position = (1100, 1170)
    # sem_position = (1100, 1450)
    # roll_position = (1100, 1750)
    # papername_position = (1100, 2000)
    # papercode_position = (1100, 2350)
    # session_position = (1100, 2640)
    i = 0
    a = [(30, 540), (30, 850), (30, 1170), (30, 1450), (30, 1750), (30, 2000), (30, 2350), (30, 2640)]
    b =[(1100, 540), (1100, 850), (1100, 1170), (1100, 1450), (1100, 1750), (1100, 2000), (1100, 2350), (1100, 2640)]
    if college:
        college_position = (100, 300)
        college = college.upper()
        if len(college) <= 32:
            college_font = ImageFont.truetype(font_path, 130)
            draw.text(college_position, college, font=college_font, fill="black")
        elif len(college) > 32 and len(college) <= 60:
            college_font = ImageFont.truetype(font_path, 100)
            space = college.rfind(' ', 0, 32 + 1)
            if space == -1: 
                first = college[:32]
                second = college[32:]
            else:
                first = college[:space]
                second = college[space+1:]
            mid = 1275
            px_per_char = 60
            start = mid - (len(first) * px_per_char // 2)
            draw.text((start, college_position[1]), first, font=college_font, fill="black")
            draw.text((start, college_position[1] + 100), second, font=college_font, fill="black")
        else:
            college_font = ImageFont.truetype(font_path, 80)
            space = college.rfind(' ', 0, 45 + 1)
            if space == -1: 
                first = college[:45]
                second = college[45:]
            else:
                first = college[:space]
                second = college[space+1:]
            mid = 1275
            px_per_char = 51
            start = mid - (len(first) * px_per_char // 2)
            draw.text((start, college_position[1]), first, font=college_font, fill="black")
            draw.text((start, college_position[1] + 100), second, font=college_font, fill="black")
    
    if name:
        name_position = b[i]
        draw.text(a[i], "NAME:", font=name_font, fill="black")
        i += 1
        name = name.upper()
        if len(name) <= 30:
            draw.text(name_position, name, font=name_font, fill="black")
        else:
            space = name.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = name[:30]
                second = name[30:]
            else:
                first = name[:space]
                second = name[space+1:]
            draw.text(name_position, first, font=name_font, fill="black")
            draw.text((name_position[0], name_position[1] + 100), second, font=name_font, fill="black")
    
    if stream:
        stream = stream.upper()
        stream_position = b[i]
        draw.text(a[i], "STREAM:", font=other_font, fill="black")
        i += 1
        if len(stream) > 30:
            space = stream.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = stream[:30]
                second = stream[30:]
            else:
                first = stream[:space]
                second = stream[space+1:]
            draw.text(stream_position, first, font=other_font, fill="black")
            draw.text((stream_position[0], stream_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(stream_position, stream, font=other_font, fill="black")
    if year:
        year = year.upper()
        year_position = b[i]
        draw.text(a[i], "YEAR:", font=other_font, fill="black")
        i += 1
        if len(year) > 30:
            space = year.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = year[:30]
                second = year[30:]
            else:
                first = year[:space]
                second = year[space+1:]
            draw.text(year_position, first, font=other_font, fill="black")
            draw.text((year_position[0], year_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(year_position, year, font=other_font, fill="black")
    if sem:
        sem = sem.upper()
        sem_position = b[i]
        draw.text(a[i], "SEM:", font=other_font, fill="black")
        i += 1
        if len(sem) > 30:
            space = sem.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = sem[:30]
                second = sem[30:]
            else:
                first = sem[:space]
                second = sem[space+1:]
            draw.text(sem_position, first, font=other_font, fill="black")
            draw.text((sem_position[0], sem_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(sem_position, sem, font=other_font, fill="black")
    if roll:
        roll = roll.upper()
        roll_position = b[i]
        draw.text(a[i], "ROLL:", font=other_font, fill="black")
        i += 1
        if len(roll) > 30:
            space = roll.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = roll[:30]
                second = roll[30:]
            else:
                first = roll[:space]
                second = roll[space+1:]
            draw.text(roll_position, first, font=other_font, fill="black")
            draw.text((roll_position[0], roll_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(roll_position, roll, font=other_font, fill="black")
    
    if papername:
        papername = papername.upper()
        papername_position = b[i]
        draw.text(a[i], "PAPER NAME:", font=other_font, fill="black")
        i += 1
        if len(papername) > 30:
            space = papername.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = papername[:30]
                second = papername[30:]
            else:
                first = papername[:space]
                second = papername[space+1:]
            draw.text(papername_position, first, font=other_font, fill="black")
            draw.text((papername_position[0], papername_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(papername_position, papername, font=other_font, fill="black")

    if papercode:
        papercode = papercode.upper()
        papercode_position = b[i]
        draw.text(a[i], "PAPER CODE:", font=other_font, fill="black")
        i += 1
        if len(papercode) > 30:
            space = papercode.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = papercode[:30]
                second = papercode[30:]
            else:
                first = papercode[:space]
                second = papercode[space+1:]
            draw.text(papercode_position, first, font=other_font, fill="black")
            draw.text((papercode_position[0], papercode_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(papercode_position, papercode, font=other_font, fill="black")
    if session:
        session_position = b[i]
        draw.text(a[i], "SESSION:", font=other_font, fill="black")
        i += 1
        session = session.upper()
        if len(session) > 30:
            space = session.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = session[:30]
                second = session[30:]
            else:
                first = session[:space]
                second = session[space+1:]
            draw.text(session_position, first, font=other_font, fill="black")
            draw.text((session_position[0], session_position[1] + 100), second, font=other_font, fill="black")
        else:
            draw.text(session_position, session, font=other_font, fill="black")

    image.save(r'static/preview.jpg')
    print(f"Cover for {name}")
    img_path = r"static/preview.jpg"
    pdf_path = r"static/preview.pdf"
    image = Image.open(img_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    return send_file(pdf_path, as_attachment=True)
@app.route('/download_prescription')
def generate_prescription():
    template_path = r'static/prescription_2.jpeg'
    output_path = r'static/prescription.png'
    font_path = r'static/DroidSans-Bold.ttf'
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 30)
    name_position = (20, 10)
    designation_position = (20, 50)
    contact_position = (20, 90)
    hospital_position = (750, 10)
    address_position = (750, 50)
    # logo_position = (450, 10)
    name = request.args.get('doctor', '')
    designation = request.args.get('designation', '')
    contact = request.args.get('contact', '')
    hospital = request.args.get('hospital', '')
    address = request.args.get('address', '')
    # logo = Image.open(r'static/logo.png')
    draw.text(name_position, name, font=font, fill="black")
    draw.text(designation_position, designation, font=font, fill="black")
    draw.text(contact_position, contact, font=font, fill="black")
    draw.text(hospital_position, hospital, font=font, fill="black")
    draw.text(address_position, address, font=font, fill="black")
    # image.paste(logo, logo_position, logo)
    image.save(output_path)
    pdf_path = r"static/preview.pdf"
    image = Image.open(output_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    return send_file(pdf_path, as_attachment=True)

@app.route('/download_thesis')
def generate_thesis():
    template_path = r'static/Thesis_2.jpeg'
    output_path = r'static/Thesis.png'
    font_path = r'static/DroidSans-Bold.ttf'
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)
    # logo = Image.open(r'static/logo.png')
    font = ImageFont.truetype(font_path, 30)
    title_font = ImageFont.truetype(font_path, 60)
    subtitle_font = ImageFont.truetype(font_path, 40)
    # logo_position = (300, 810)

    name = request.args.get('name', ''),
    department = request.args.get('department', ''),
    supervisor = request.args.get('supervisor', ''),
    supervisor_department = request.args.get('supervisor_department', ''),
    title = request.args.get('title', ''),
    subtitle = request.args.get('subjectcode', ''),
    college = request.args.get('college', ''),
    address = request.args.get('address', '')

    if title:
        title_position = (350, 150)
        title = title.upper()
        if len(title) <= 30:
            draw.text(title_position, title, font=title_font, fill="black")
        else:
            space = title.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = title[:30]
                second = title[30:]
            else:
                first = title[:space]
                second = title[space+1:]
            draw.text(title_position, first, font=font, fill="black")
            draw.text((title_position[0], title_position[1] + 100), second, font=title_font, fill="black")
    
    if subtitle:
        subtitle_position = (350, 250)
        subtitle = subtitle.upper()
        if len(subtitle) <= 30:
            draw.text(subtitle_position, subtitle, font=subtitle_font, fill="black")
        else:
            space = subtitle.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = subtitle[:30]
                second = subtitle[30:]
            else:
                first = subtitle[:space]
                second = subtitle[space+1:]
            draw.text(subtitle_position, first, font=font, fill="black")
            draw.text((subtitle_position[0], subtitle_position[1] + 100), second, font=subtitle_font, fill="black")

    if department:
        department_position = (350, 520)
        department = department.upper()
        if len(department) <= 30:
            draw.text(department_position, department, font=font, fill="black")
        else:
            space = department.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = department[:30]
                second = department[30:]
            else:
                first = department[:space]
                second = department[space+1:]
            draw.text(department_position, first, font=font, fill="black")
            draw.text((department_position[0], department_position[1] + 100), second, font=font, fill="black")

    if supervisor:
        supervisor_position = (350, 650)
        supervisor = supervisor.upper()
        if len(supervisor) <= 30:
            draw.text(supervisor_position, supervisor, font=font, fill="black")
        else:
            space = supervisor.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = supervisor[:30]
                second = supervisor[30:]
            else:
                first = supervisor[:space]
                second = supervisor[space+1:]
            draw.text(supervisor_position, first, font=font, fill="black")
            draw.text((supervisor_position[0], supervisor_position[1] + 100), second, font=font, fill="black")

    if supervisor_department:
        supervisor_department_position = (350, 720)
        supervisor_department = supervisor_department.upper()
        if len(supervisor_department) <= 30:
            draw.text(supervisor_department_position, supervisor_department, font=font, fill="black")
        else:
            space = supervisor_department.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = supervisor_department[:30]
                second = supervisor_department[30:]
            else:
                first = supervisor_department[:space]
                second = supervisor_department[space+1:]
            draw.text(supervisor_department_position, first, font=font, fill="black")
            draw.text((supervisor_department_position[0], supervisor_department_position[1] + 100), second, font=font, fill="black")

    if address:
        address_position = (350, 1120)
        address = address.upper()
        if len(address) <= 30:
            draw.text(address_position, address, font=font, fill="black")
        else:
            space = address.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = address[:30]
                second = address[30:]
            else:
                first = address[:space]
                second = address[space+1:]
            draw.text(address_position, first, font=font, fill="black")
            draw.text((address_position[0], address_position[1] + 50), second, font=font, fill="black")
    

    if college:
        college_position = (350, 1050)
        college = college.upper()
        if len(college) <= 32:
            draw.text(college_position, college, font=font, fill="black")
        elif len(college) > 32 and len(college) <= 60:
            college_font = ImageFont.truetype(font_path, 30)
            space = college.rfind(' ', 0, 32 + 1)
            if space == -1: 
                first = college[:32]
                second = college[32:]
            else:
                first = college[:space]
                second = college[space+1:]
            mid = 1275
            px_per_char = 60
            start = mid - (len(first) * px_per_char // 2)
            draw.text((start, college_position[1]), first, font=college_font, fill="black")
            draw.text((start, college_position[1] + 100), second, font=college_font, fill="black")
        else:
            college_font = ImageFont.truetype(font_path, 25)
            space = college.rfind(' ', 0, 45 + 1)
            if space == -1: 
                first = college[:45]
                second = college[45:]
            else:
                first = college[:space]
                second = college[space+1:]
            mid = 1275
            px_per_char = 51
            start = mid - (len(first) * px_per_char // 2)
            draw.text((start, college_position[1]), first, font=college_font, fill="black")
            draw.text((start, college_position[1] + 100), second, font=college_font, fill="black")

    if name:
        name_position = (350, 450)
        name = name.upper()
        if len(name) <= 30:
            draw.text(name_position, name, font=font, fill="black")
        else:
            space = name.rfind(' ', 0, 30 + 1)
            if space == -1: 
                first = name[:30]
                second = name[30:]
            else:
                first = name[:space]
                second = name[space+1:]
            draw.text(name_position, first, font=font, fill="black")
            draw.text((name_position[0], name_position[1] + 100), second, font=font, fill="black")

    # logo = logo.resize((600, 150))
    # image.paste(logo, logo_position, logo)
    image.save(output_path)
    print(f"Cover for {name} saved at {output_path}")
    pdf_path = r"static/preview.pdf"
    image = Image.open(output_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
