from flask import Flask,render_template,url_for,redirect,request,flash,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import click
import os
app=Flask(__name__)
app.secret_key='secret string'
db=SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path,'message.db')


class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    name=db.Column(db.String(20))
    timestamp=db.Column(db.DateTime,default=datetime.now,index=True)


@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    if drop:
        click.confirm('This operation will delete the databse,do you want to continue?',abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')



@app.route('/index',methods = ['GET','POST'])
def index():
    #messages = Message.query.order_by(Message.timestamp.desc()).all()
    messages = Message.query.all()
    name=request.form.get('name')
    body=request.form.get('body')
    if name is None:
        print ('Name is none')
    else:
        print('name is not none')
    if name is not None and body is not None:
        print ('name is ' + name)
        print ('body is ' + body)
        message=Message(body=body,name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        print('done!----------------------')
        return redirect(url_for('index'))

    return render_template('index.html',messages=messages)

    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
