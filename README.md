## The service

You are tasked to implement a RESTful API that provides the following two basic functionalities to retrieve movie metadata from a content catalogue.

The data used for this comes from two sources
- Typically, our own movie data would come from a database, but to simplify this we use the static json files in `./movies` as our content catalogue.
- OMDb movie metadata can be retrieved as follows:
    - `http://www.omdbapi.com/?i=<imdb movie id>&apikey=<apikey>&plot=full`
    - You can use the following API key: `68fd98ab` (Limited to 1000 requests per day)
    - Please see http://www.omdbapi.com for details

#### Getting enriched movie metadata (title, description, ..) 

The first task is to merge movie metadata from our systems with movie metadata from the Open Movie Database (OMDb).

- Calling `GET /api/movies/:id` should return a JSON object representing the merged movie object.
- `:id` is an alphanumeric value that can either refer to OMDb movie ids or our internal ids.
- When merging the two objects with the same fields (i.e. both JSON objects have a `title` / `Title`), it depends on the name of the field, which metadata should be used.
- The following rules apply, with capitalized field names (i.e. `Title` vs `title`) always referring to OMDb data
    - `Title` overwrites `title`
    - `Plot` overwrites `description`
    - `duration` overwrites `Runtime`
    - `userrating` will become part of `Ratings`, applying a similar logic than `Ratings` currently has
    - `Director`, `Writer` and `Actors` should be transformed from `String` to an `String[]`
    
- Fields not covered by any of these rules should be merged into the resulting JSON without transformation
- If fields are unclear, make reasonable assumptions and choose your implementation accordingly

#### Search movies in our catalogue

We want to be able to search movies in our catalogue. To that end, we implement a simple search that returns a movie object if **all** search terms are true. A search term is a query param in your REST call in the form of `<search_field>=<search value>`

- If no search term is provided, return all movies
- Search terms are **case-insensitve**
- Search is performed on the merged json objects of movies
- If `<search_field>` is of type `Number` or `String` in the movie metadata, the search matches if the values are equal, i.e. `?title=Sin City` matches `3532674.json`
- If `<search_field>` is of type `Array` in the movie metadata, the search matches if the `<search value>` is contained in the array, i.e. `?director=Frank Miller` matches `3532674.json` / the corresponding OMBd object
- Calling `GET /api/movies?<search_field>=<search value>` should return a JSON array representing all movies that match the search criteria

## Constraints

- Use Python (minimum 3.5),java or nodejs
- Do not introduce any system dependencies (databases, caches, search engines, docker, ..) to solve this task. This task is about your problem solving skills and not about creating a production ready system. It should not require more than installing the dependency (for e.g: `pip install`) and  running the application (for e.g: `python <your_script>.py`) to have a running service.

