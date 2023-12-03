from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base
from os import environ
import datetime
import socket
from flask import Flask, make_response, request


# create database table classes
class count_table_object(declarative_base()):
    __tablename__ = environ['COUNT_TABLE']
    id = Column(Integer, primary_key=True)
    counter = Column(Integer)


class log_table_object(declarative_base()):
    __tablename__ = environ['LOG_TABLE']
    id = Column(Integer, primary_key=True)
    client_ip = Column(String)
    internal_ip = Column(String)
    timestamp = Column(TIMESTAMP)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def addCountCreateCookieData2DBBandShowIP():
    # Initialize database connection
    engine = create_engine(f"mysql://{environ['USER_NAME']}:{environ['USER_PASSWORD']}@DB/{environ['DB_NAME']}")
    session = sessionmaker(bind=engine)()

    # get the session ip
    client_ip = request.headers.get('X-Forwarded-For')

    # getting internal ip
    internal_ip_address = socket.gethostbyname(socket.gethostname())

    # create cookie
    cookie=make_response()
    cookie_timer = datetime.datetime.now() + datetime.timedelta(minutes=5)
    cookie.set_cookie('whist_app_cookie',value=internal_ip_address,expires=cookie_timer)

    # add 1 to counter
    counter = session.query(count_table_object).one_or_none()
    counter.counter +=1
    session.commit()
    session.close()

    log_item = log_table_object()
    log_item.client_ip=client_ip
    log_item.internal_ip=internal_ip_address
    log_item.timestamp=datetime.datetime.now()
    session.add(log_item)
    session.commit()
    session.close()

    return internal_ip_address


@app.route('/showcount', methods=['GET', 'POST'])
def showCount():
    engine = create_engine(f"mysql://{environ['USER_NAME']}:{environ['USER_PASSWORD']}@DB/{environ['DB_NAME']}")
    db_session = sessionmaker(bind=engine)
    session = db_session()

    counter = session.query(count_table_object).one()

    return str(counter.counter)


# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,)

