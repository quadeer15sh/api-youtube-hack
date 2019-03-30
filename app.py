from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/api/data_by_categories', methods = ['GET'])
def data_by_categories():
    data = pd.read_csv('data_by_categories.csv')
    categories = data['Categories'].tolist()
    views = data['Views'].tolist()
    likes = data['Likes'].tolist()
    dislikes = data['Dislikes'].tolist()
    comments = data['Comments'].tolist()

    return jsonify({"Categories":categories, "Views":views, "Likes":likes, "Dislikes":dislikes, "Comments":comments})

@app.route('/api/videostats', methods=['GET'])
def videoStats():
    max_likes = int(df.likes.max())
    min_likes = int(df.likes.min())
    upper_likes = int(df.likes[df.likes >= df.likes.mean()].count())
    lower_likes = int(df.likes[df.likes < df.likes.mean()].count())

    max_views = int(df.views.max())
    min_views = int(df.views.min())
    upper_views = int(df.views[df.views >= df.views.mean()].count())
    lower_views = int(df.views[df.views < df.views.mean()].count())

    max_comments = int(df.comment_count.max())
    min_comments = int(df.comment_count.min())
    upper_comments = int(df.comment_count[df.comment_count >= df.comment_count.mean()].count())
    lower_comments = int(df.comment_count[df.comment_count < df.comment_count.mean()].count())

    stats = {
    'Likes':{'maximum':max_likes, 'minimum':min_likes, 'more than avg':upper_likes, 'less than avg':lower_likes},
    'Views':{'maximum': max_views, 'minimum':min_views, 'more than avg':upper_views, 'less than avg':lower_views},
    'Comments':{'maximum': max_comments, 'minimum':min_comments, 'more than avg':upper_comments, 'less than avg':lower_comments}
             }

    return jsonify(stats)

@app.route('/api/best_publish_time', methods = ['GET'])
def bestPublishTime():
    new_df = df.drop_duplicates()
    category_list = new_df.categories.unique().tolist()
    category_list.pop(12)
    best_upload_time = {}
    for i in category_list:
        best_upload_time[i] = new_df[new_df['categories']==i].nlargest(15,['views','likes'])['publish_time'].unique().astype(str).tolist()

    return jsonify(best_upload_time)

@app.route('/api/hot_titles', methods=['GET'])
def hotTitles():
    data = pd.read_csv('hottitles.csv')
    category_list = data.columns.values.tolist()
    hot_titles = {}
    for category in category_list:
        hot_titles[category] = data[category].tolist()

    return jsonify(hot_titles)

if __name__ == '__main__':
    df = pd.read_csv('cleaned_stats.csv')
    app.run(debug=True)
