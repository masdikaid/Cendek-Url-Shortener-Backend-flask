from firebase_admin import initialize_app, auth, firestore, exceptions

initialize_app()
db = firestore.client()