
import requests

API_KEY = '39d6b0d3'


class Movies:

  def __init__(self, ids=['tt0111161'], img_dir='.', movies=None):
    if movies is not None:
      self.movies = movies
    else:
      self.movies = dict()

      for m in ids:
        self.movies[m] = dict()

        # download information for the movie
        result = requests.get('http://www.omdbapi.com/?i=' +
                              m + '&apikey=' + API_KEY).json()

        self.movies[m]['image'] = False
        # download movie image
        if 'Poster' in result:
          img = requests.get(result['Poster'], stream=True)

          if img.status_code == 200:
            with open(img_dir + m + '.jpg', 'wb') as f:
              for chunk in img.iter_content(chunk_size=1024):
                f.write(chunk)
              self.movies[m]['image'] = True

        # retrieve information
        self.movies[m]['id'] = m
        self.movies[m]['title'] = result['Title']
        self.movies[m]['rating'] = result['imdbRating']
        self.movies[m]['released'] = result['Released']
        self.movies[m]['duration'] = result['Runtime']
        self.movies[m]['genre'] = result['Genre']
        self.movies[m]['director'] = result['Director']

  def isExisting(self, id):
    if id in self.movies:
      return True
    else:
      return False
  
  def get_movie(self):
    return self.movies
  
  def get_movie_id(self, id):
    return self.movies[id]

  def get_image_movie(self, id):
    if id in self.movies:
      return id + '.jpg'
