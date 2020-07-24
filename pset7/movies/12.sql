SELECT movies.title FROM movies
INNER JOIN stars ON movies.id = stars.movie_id
INNER JOIN people ON stars.person_id = people.id
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE stars.person_id IN (SELECT people.id FROM people GROUP BY people.id HAVING people.name = "Johnny Depp")

INTERSECT

SELECT movies.title FROM movies
INNER JOIN stars ON movies.id = stars.movie_id
INNER JOIN people ON stars.person_id = people.id
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE stars.person_id IN (SELECT people.id FROM people GROUP BY people.id HAVING people.name = "Helena Bonham Carter")