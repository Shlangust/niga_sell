from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os


from flask import Flask, request,render_template, redirect

engine = create_engine('sqlite:///news.db')
Base = declarative_base()

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  content = Column(Text)
  image_data = Column(Text)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

''''''

engine1 = create_engine('sqlite:///back_con.db')
Base1 = declarative_base()

class Post1(Base1):
  __tablename__ = 'pred'

  id = Column(Integer, primary_key=True)
  cont = Column(String)


Base1.metadata.create_all(engine1)

Session = sessionmaker(bind=engine1)
session1 = Session()


app = Flask(__name__)

'''
вывод новости на главной
print(session.query(Post).all()[0].title)
'''
@app.route("/")
def index():
    try:
        new1 = session.query(Post).all()[0]
        new2 = session.query(Post).all()[1]
        return render_template("index.html",new1=new1,new2=new2)
    except:
        return render_template("index.html",new1='Нету',new2='Нету')
@app.route("/news")
def news():
    posts = session.query(Post).all()
    return render_template("news.html", posts=posts)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        # return render_template()
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        image_data = 'static/' + image.filename
        # print(image_data)
        image.save(os.path.join(app.root_path, 'static', image.filename))
        post = Post(title = title, content = content,image_data=image_data)
        session.add(post)
        session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/back_con',methods=['POST'])
def back_con():
    if request.method == 'POST':

       cont = request.form['cont']

       post1 = Post1(cont=cont)
       session1.add(post1)
       session1.commit()
       return redirect('/')
    return render_template('help.html')


@app.route('/help',methods=['GET'])
def hlp():
    return render_template('help.html')

@app.route('/delete/<int:id>')
def delete(id):
   post = session.query(Post).filter_by(id=id).first()
   session.delete(post)
   session.commit()
   return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)