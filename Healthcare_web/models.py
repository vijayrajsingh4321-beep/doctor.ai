#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    


# In[ ]:




