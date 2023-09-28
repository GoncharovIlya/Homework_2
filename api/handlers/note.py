from api import app, multi_auth, request
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema
from utility.helpers import get_object_or_404


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
def get_note_by_id(note_id):
    # TODO: авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    return note_schema.dump(note), 200


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
def get_notes():
    # TODO: авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.all()
    note = NoteModel.query.filter(NoteModel.author_id)
    # note = NoteModel.query.get(id)
    # if user.id == note:
    if user.id == note:
    # if notes.author_id == multi_auth.current_user().id:
        return notes_schema.dump(notes), 200


@app.post("/notes")
@multi_auth.login_required
def create_note():
    user = multi_auth.current_user()
    note_data = request.json
    note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note_schema.dump(note), 201


@app.put("/notes/<int:note_id>")
@multi_auth.login_required
def edit_note(note_id):
    # +TODO: Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    note = get_object_or_404(NoteModel, note_id)
    note_data = request.json
    if note.author_id == multi_auth.current_user().id:
        note.text = note_data["text"]
        note.private = note_data.get("private") or note.private
        note.save()
        return note_schema.dump(note), 200
    # note.save()
    return {"Error": "You can not delete this note"}, 403 


@app.delete("/notes/<int:note_id>")
@multi_auth.login_required
def delete_note(note_id):
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == multi_auth.current_user().id:
        note.delete()
        return {'Info': f'Message with id = {note_id} was deleted'}, 200
    return {"Error": "You can not delete this note"}, 403
    # +TODO: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
