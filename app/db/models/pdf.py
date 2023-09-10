from ...extensions import db

class PDF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) # this could be the key/path
    s3_url = db.Column(db.String(500), nullable=False) # direct URL to the file S3
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)