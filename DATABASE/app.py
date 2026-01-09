from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devops:pass@localhost/lingvo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    teacher = db.Column(db.String(100))
    level = db.Column(db.String(20))
    totallength = db.Column(db.Integer)
    weeklength = db.Column(db.Integer)
    coursefeeperhour = db.Column(db.Float)
    startdates = db.Column(db.ARRAY(db.String))

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    languagelevel = db.Column(db.String(20))
    languagesoffered = db.Column(db.ARRAY(db.String))
    languagesspoken = db.Column(db.ARRAY(db.String))
    workexperience = db.Column(db.Integer)
    priceperhour = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer)
    tutorid = db.Column(db.Integer)
    datestart = db.Column(db.String)
    timestart = db.Column(db.String)
    duration = db.Column(db.Integer)
    persons = db.Column(db.Integer)
    price = db.Column(db.Float)
    earlyregistration = db.Column(db.Boolean, default=False)
    groupenrollment = db.Column(db.Boolean, default=False)
    intensivecourse = db.Column(db.Boolean, default=False)
    supplementary = db.Column(db.Boolean, default=False)
    personalized = db.Column(db.Boolean, default=False)
    excursions = db.Column(db.Boolean, default=False)
    assessment = db.Column(db.Boolean, default=False)
    interactive = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/courses', methods=['GET', 'OPTIONS'])
def get_courses():
    if request.method == 'OPTIONS': return '', 200
    courses = Course.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'teacher': c.teacher,
        'level': c.level,
        'totallength': c.totallength,
        'weeklength': c.weeklength,
        'coursefeeperhour': c.coursefeeperhour,
        'startdates': c.startdates or []
    } for c in courses])

@app.route('/api/courses/<int:id>', methods=['GET', 'OPTIONS'])
def get_course(id):
    if request.method == 'OPTIONS': return '', 200
    course = Course.query.get_or_404(id)
    return jsonify({
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'teacher': course.teacher,
        'level': course.level,
        'totallength': course.totallength,
        'weeklength': course.weeklength,
        'coursefeeperhour': course.coursefeeperhour,
        'startdates': course.startdates or []
    })

@app.route('/api/tutors', methods=['GET', 'OPTIONS'])
def get_tutors():
    if request.method == 'OPTIONS': return '', 200
    tutors = Tutor.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'languagelevel': t.languagelevel,
        'languagesoffered': t.languagesoffered or [],
        'languagesspoken': t.languagesspoken or [],
        'workexperience': t.workexperience,
        'priceperhour': t.priceperhour
    } for t in tutors])

@app.route('/api/tutors/<int:id>', methods=['GET', 'OPTIONS'])
def get_tutor(id):
    if request.method == 'OPTIONS': return '', 200
    tutor = Tutor.query.get_or_404(id)
    return jsonify({
        'id': tutor.id,
        'name': tutor.name,
        'languagelevel': tutor.languagelevel,
        'languagesoffered': tutor.languagesoffered or [],
        'languagesspoken': tutor.languagesspoken or [],
        'workexperience': tutor.workexperience,
        'priceperhour': tutor.priceperhour
    })

@app.route('/api/orders', methods=['GET', 'POST', 'OPTIONS'])
def orders():
    if request.method == 'OPTIONS': return '', 200
    if request.method == 'POST':
        data = request.json
        order = Order(
            courseid=data.get('courseid'),
            tutorid=data.get('tutorid'),
            datestart=data.get('datestart'),
            timestart=data.get('timestart'),
            duration=data.get('duration'),
            persons=data.get('persons'),
            price=data.get('price'),
            earlyregistration=data.get('earlyregistration', False),
            groupenrollment=data.get('groupenrollment', False),
            intensivecourse=data.get('intensivecourse', False),
            supplementary=data.get('supplementary', False),
            personalized=data.get('personalized', False),
            excursions=data.get('excursions', False),
            assessment=data.get('assessment', False),
            interactive=data.get('interactive', False)
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'id': order.id}), 201
    orders_list = Order.query.all()
    return jsonify([{
        'id': o.id,
        'courseid': o.courseid,
        'tutorid': o.tutorid,
        'datestart': o.datestart,
        'timestart': o.timestart,
        'duration': o.duration,
        'persons': o.persons,
        'price': o.price,
        'earlyregistration': o.earlyregistration,
        'groupenrollment': o.groupenrollment,
        'intensivecourse': o.intensivecourse,
        'supplementary': o.supplementary,
        'personalized': o.personalized,
        'excursions': o.excursions,
        'assessment': o.assessment,
        'interactive': o.interactive
    } for o in orders_list])

@app.route('/api/orders/<int:id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
def order_detail(id):
    if request.method == 'OPTIONS': return '', 200
    order = Order.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': order.id,
            'courseid': order.courseid,
            'tutorid': order.tutorid,
            'datestart': order.datestart,
            'timestart': order.timestart,
            'duration': order.duration,
            'persons': order.persons,
            'price': order.price,
            'earlyregistration': order.earlyregistration,
            'groupenrollment': order.groupenrollment,
            'intensivecourse': order.intensivecourse,
            'supplementary': order.supplementary,
            'personalized': order.personalized,
            'excursions': order.excursions,
            'assessment': order.assessment,
            'interactive': order.interactive
        })
    elif request.method == 'PUT':
        data = request.json
        order.datestart = data.get('datestart', order.datestart)
        order.timestart = data.get('timestart', order.timestart)
        order.persons = data.get('persons', order.persons)
        order.price = data.get('price', order.price)
        order.supplementary = data.get('supplementary', order.supplementary)
        order.personalized = data.get('personalized', order.personalized)
        order.excursions = data.get('excursions', order.excursions)
        order.assessment = data.get('assessment', order.assessment)
        order.interactive = data.get('interactive', order.interactive)
        db.session.commit()
        return jsonify({'id': order.id}), 200
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
