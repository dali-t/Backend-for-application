from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from repositories import image_repo, user_repo, comment_repo, reaction_repo
from repositories import reaction_repo
from datetime import datetime

load_dotenv()

app = Flask(__name__)

@app.get('/')
def index():
    all_images = image_repo.get_all_images_for_table()
    return render_template('index.html', images=all_images)

@app.get('/images/<int:image_id>')
def get_image(image_id):
    image = image_repo.get_image_by_id(image_id)
    if not image:
        return 'Image not found', 404
    
    # Fetch comments and reactions for the image
    comments = comment_repo.get_comments_for_image(image_id)
    reaction_counts = reaction_repo.get_reaction_counts(image_id)
    # print(reactions)
    return render_template('image.html', image=image, comments=comments, reaction_counts=reaction_counts)

@app.get('/images/new')
def new_image():
    users = user_repo.get_all_users()
    return render_template('new_image.html', users=users)

@app.post('/images')
def create_image():
    caption = request.form.get('caption')
    image_link = request.form.get('image_link')
    author_email = request.form.get('author_email')

    if not caption or not image_link or not author_email:
        return 'Bad Request - Missing Form Data', 400

    try:
        # Attempt to create the image, which may raise a ValueError
        image_id = image_repo.create_image(caption, image_link, author_email)
        return redirect(f'/images/{image_id}')
    
    except ValueError as e:
        # Return error message with link to index page
        return f'Error: {e}. <a href="/">Return to view all Images</a>', 400

    except Exception as e:
        return 'Internal Server Error', 500

@app.post('/images/<int:image_id>/comments')
def create_comment(image_id):
    user_id = 1  # Assuming user_id is retrieved from session or authentication
    comment_text = request.form.get('comment_text')

    if not comment_text:
        return 'Bad Request - Missing Comment Text', 400

    try:
        comment_repo.create_comment(image_id, user_id, comment_text)
        return redirect(url_for('get_image', image_id=image_id))
    
    except Exception as e:
        return f'Error creating comment: {e}', 500
    
# This feature doesnt work properly, was trying to learn how to do it but it's kinda hard. Just here for aesthetics
@app.post('/images/<int:image_id>/reactions')
def react_to_image(image_id):
    reaction_types = request.form.getlist('reaction_types[]')

    if not reaction_types:
        return 'Bad Request - No Reaction Selected', 400

    for reaction_type in reaction_types:
        try:
            reaction_repo.create_reaction(image_id, user_id, reaction_type)  # Assuming user_id is obtained from session or authentication
        except Exception as e:
            return f'Error reacting to image: {e}', 500

    return redirect(url_for('get_image', image_id=image_id))


if __name__ == '__main__':
    app.run(debug=True)