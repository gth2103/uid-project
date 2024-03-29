from app import db
from app.models import *
from sqlalchemy import asc
import  pytz


def add_event(event):
	db.session.add(event)
	db.session.commit()

def add_user_event(event, current_user):
	user_event = UserEvent(user_id=current_user.id, event_id=event.id, accepted=True)
	db.session.add(user_event)
	db.session.commit()

def get_recent_events(user_id):
	eastern = pytz.timezone('US/Eastern')
	today = datetime.now()
	local = eastern.localize(today)
	events = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.user_id == user_id, UserEvent.accepted == 1, Event.date >= local).order_by(asc(Event.date), asc(Event.start_time)).all()
	return events

def get_pending_events(user_id):
	eastern = pytz.timezone('US/Eastern')
	today = datetime.now()
	local = eastern.localize(today)
	events = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.user_id == user_id, UserEvent.accepted == 0, Event.date >= local).order_by(asc(Event.date), asc(Event.start_time)).all()
	return events

def get_event(event_id):
	event = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.event_id == event_id).first()
	return event

def remove_event(event_id):
	event = Event.query.filter_by(id=event_id).first()
	db.session.delete(event)
	db.session.commit()

def update_db_event(event_id, date, start_time, end_time, notes):
	event = Event.query.filter_by(id=event_id).first()
	event.date =  date
	event.start_time = start_time
	event.end_time = end_time 
	event.notes  = notes
	db.session.commit()


def send_invite(event, current_user, user):
	sender = UserEvent(user_id=current_user.id, event_id=event.id, accepted=True)
	receiver = UserEvent(user_id=user.id, event_id=event.id)
	db.session.add(sender)
	db.session.add(receiver)
	event_invitation = EventInvitation(sender_id=current_user.id, receiver_id=user.id, event_id=event.id)
	db.session.add(event_invitation)
	db.session.commit()

def get_user_event(event_id, user_id):
	event = db.session.query(UserEvent).filter(UserEvent.event_id == event_id, UserEvent.user_id == user_id).first()
	return event

def accept_user_event(event_id, user_id):
	event = db.session.query(UserEvent).filter(UserEvent.event_id == event_id, UserEvent.user_id == user_id).first()
	event.accepted  = 1;
	db.session.commit()

def delete_user_event(event_id, user_id):
	event = db.session.query(UserEvent).filter(UserEvent.event_id == event_id, UserEvent.user_id == user_id).first()
	print(event)
	db.session.delete(event)
	db.session.commit()



