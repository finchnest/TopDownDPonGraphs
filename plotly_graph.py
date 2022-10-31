import plotly.graph_objects as go
import networkx as nx
from utils import *

node_attributes = ['user_id', 'public', 'completion_percentage', 'gender', 'region', 'last_login', 'registration', 'AGE', 'body', 'I_am_working_in_field', 'spoken_languages', 'hobbies', 'I_most_enjoy_good_food', 'pets', 'body_type', 'my_eyesight', 'eye_color', 'hair_color', 'hair_type', 'completed_level_of_education', 'favourite_color', 'relation_to_smoking', 'relation_to_alcohol', 'sign_in_zodiac', 'on_pokec_i_am_looking_for', 'love_is_for_me', 'relation_to_casual_sex', 'my_partner_should_be', 'marital_status', 'children', 'relation_to_children', 'I_like_movies', 'I_like_watching_movie', 'I_like_music', 'I_mostly_like_listening_to_music', 'the_idea_of_good_evening', 'I_like_specialties_from_kitchen', 'fun', 'I_am_going_to_concerts', 'my_active_sports', 'my_passive_sports', 'profession', 'I_like_books', 'life_style', 'music', 'cars', 'politics', 'relationships', 'art_culture', 'hobbies_interests', 'science_technologies', 'computers_internet', 'education', 'sport', 'movies', 'travelling', 'health', 'companies_brands', 'more']
MAX_NODE=50
df = pd.read_csv('./toy_example_500.csv')
missing = load_missing()
graph = create_network(df, node_attributes, MAX_NODE, missing)

edge_df = pd.read_csv('toy_example_edge_50.csv')
src, tgt = edge_df['source'].tolist(), edge_df['target'].tolist()

edge_trace = go.Scatter(
    x=src, y=tgt,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')


