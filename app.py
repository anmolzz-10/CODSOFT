from flask import Flask, request, render_template
import pickle
import pandas as pd
from surprise import Dataset, Reader

app = Flask(__name__)

# Load book data
books_df = pd.read_csv('D:/codsoft projects/book_project/data/books.csv')

def get_top_n_recommendations(predictions, n=10):
    top_n = {}
    for uid, iid, true_r, est, _ in predictions:
        if not top_n.get(uid):
            top_n[uid] = []
        top_n[uid].append((iid, est))
    
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    
    return top_n

def get_book_info(book_ids):
    book_info = books_df[books_df['book_id'].isin(book_ids)][['book_id', 'title', 'authors', 'average_rating', 'original_publication_year', 'small_image_url']]
    return book_info.set_index('book_id').to_dict(orient='index')

def load_data():
    ratings_df = pd.read_csv('ratings.csv')
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'book_id', 'rating']], reader)
    return data

# Load the pre-trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = int(request.form['user_id'])
    
    # Generate predictions using the existing model
    predictions = model.test([(user_id, book_id, 4) for book_id in range(1, 10001)])
    top_n = get_top_n_recommendations(predictions)
    
    # Get top recommended books for the user
    top_books = top_n.get(user_id, [])
    top_books_ids = [book_id for book_id, _ in top_books]
    
    # Get book details
    book_details = get_book_info(top_books_ids)
    
    # Format the data for rendering
    recommendations = []
    for book_id, rating in top_books:
        book = book_details.get(book_id, {})
        recommendations.append({
            'book_id': book_id,
            'title': book.get('title', 'Unknown'),
            'authors': book.get('authors', 'Unknown'),
            'average_rating': book.get('average_rating', 'N/A'),
            'original_publication_year': book.get('original_publication_year', 'N/A'),
            'small_image_url': book.get('small_image_url', ''),
            'rating': rating
        })
    
    return render_template('recommendations.html', recommendations=recommendations, user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
