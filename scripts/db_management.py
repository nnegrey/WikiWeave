import os
from dotenv import load_dotenv

import mysql.connector

load_dotenv()

mydb = mysql.connector.connect(
    host="localhost",
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DBNAME"),
)

# ***** PAGE table *****
# (265,612, /*page_namespace=*/  0, /*page_is_redirect=*/ 0)
# (104,536, /*page_namespace=*/  0, /*page_is_redirect=*/ 1)
# ( 79,996, /*page_namespace=*/ 14, /*page_is_redirect=*/ 0)
# (      5, /*page_namespace=*/ 14, /*page_is_redirect=*/ 1)

# ***** PAGELINKS table *****
# (17,633,711,  /*pl_from_namespace=*/  0)
# (   733,083,  /*pl_from_namespace=*/ 14)
# (18,366,794 total)

mycursor = mydb.cursor()

sql = """
SELECT
    *
FROM
    categorylinks
WHERE
    cl_to = 'Months'
LIMIT 50
"""

category_sql = """
SELECT
    *
FROM
    category
WHERE
    cat_title = 'Months'
LIMIT 50
"""
# (1, b'Months', b'', (2025, 2, 17), b'*04', b'', b'page', 1, 2376443)
# (1, b'Webarchive_template_wayback_links', b'', (2025, 2, 17), b'', b'', b'page', 1, 1375777)
# (2, b'Months', b'', (2025, 2, 17), b'*08', b'', b'page', 1, 2376443)

page_of_category = """
SELECT
    *
FROM
    page
WHERE page_id IN (1,2)
"""

query_sql = """
SELECT
    *
FROM
    page
WHERE
    -- CONVERT(page_title USING utf8) = 'Federal_Ministry_for_Economic_Affairs_and_Climate_Action'
    page_title = 'Federal_Ministry_for_Economic_Affairs_and_Climate_Action'
"""

embededing_sql = """
SELECT
    title,
    content,
    embedding
FROM
    page_embeddings
WHERE
    title IN ('Arthur_C._Clarke', 'Custard', 'English_Channel', 'National_Women''s_Hockey_League_(1999–2007)', 'Thyroid_cancer', 'Mark_Knopfler', 'Young_Frankenstein', 'Agarn', 'Brooks_Brothers')
"""

lazy_random_record_sql = """
SELECT *
FROM page
WHERE page_id >= RAND() * (SELECT MAX(page_id) FROM page)
ORDER BY page_id
LIMIT 10;
"""

use_rand_sql = """
SELECT *
FROM page
WHERE
    page_namespace = 0
    AND page_is_redirect = 0
    AND page_random >= RAND()
ORDER BY page_random
LIMIT 2;
"""

page_links = """
 SELECT
    *
FROM
    pagelinks
WHERE
    pl_from = 7284
"""

pages = """
SELECT
    *
FROM
    linktarget
WHERE
    lt_id IN(12213, 12217, 41018, 206177, 208972, 215368, 427391, 427421, 427423)
"""

simplified_sql = """
WITH target_links AS (
    SELECT
        pl_target_id
    FROM
        pagelinks
    WHERE
        pl_from = 59165
),
page_titles AS (
    SELECT
        linktarget.lt_title
    FROM linktarget
    JOIN target_links ON linktarget.lt_id = target_links.pl_target_id
    WHERE lt_namespace = 0
)
SELECT
    page.page_id,
    CONVERT(page.page_title USING utf8) AS page_title,
    pe.content,
    pe.embedding
FROM
    page
    JOIN page_titles
        ON page.page_title = page_titles.lt_title
    JOIN page_embeddings pe
        ON CONVERT(page.page_title USING utf8) = pe.title
WHERE
    page.page_namespace = 0
    AND page.page_is_redirect = 0
"""


# ('United_States',)
# ('Australia',)
# ('Europe',)
# ('Asia',)
# ('Illinois',)
# ('Canada',)
# ('1935',)
# ('USA',) -- redirect to United_States
# ('Motorcycle_club',) -- no page
# ('Mc_Cook',) -- no page

# (27, 'Australia')
# (216, 'Europe')
# (1994, 'Asia')
# (8260, '1935')
# (11192, 'Illinois')
# (219587, 'United_States')
# (219589, 'Canada')


mycursor.execute(embededing_sql)

results = mycursor.fetchall()
for row in results:
    print(row)

mydb.close()
