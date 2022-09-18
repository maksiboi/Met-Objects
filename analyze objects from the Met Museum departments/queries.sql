--1
--I want to get information on the most popular artworks over departments so I can create my marketing campaigns

CREATE TABLE IF NOT EXISTS popular_artworks AS
(
SELECT objectid, objectname, title, department
FROM damntargetbucket
WHERE ishighlight = true
ORDER BY 2 asc
)

--2
-- I want to get information about departments with the highest count of objects/art so I can plan my budget accordingly

CREATE TABLE IF NOT EXISTS count_of_objects_per_dep AS
(
SELECT DISTINCT(department), COUNT(objectid) as number_of_art_objects
FROM damntargetbucket
GROUP BY 1
ORDER BY 2 desc
)

SELECT * FROM count_of_objects_per_dep

--3
--I want to get the number of art objects by department and accession year

CREATE TABLE IF NOT EXISTS obj_num_per_yeardep AS(
SELECT distinct(accessionyear), department,
COUNT(objectid) OVER (PARTITION BY department ORDER BY accessionyear asc) AS obj_num_for_dep
FROM damntargetbucket
ORDER BY 1 asc)

SELECT * FROM obj_num_per_yeardep LIMIT 10