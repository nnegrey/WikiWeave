WITH random_pages AS (
    SELECT
        page_id,
        CONVERT(page_title USING utf8) AS page_title
    FROM
        page
    WHERE
        page_namespace = 0
        AND page_is_redirect = 0
        AND page_random >= RAND()
    ORDER BY page_random
    LIMIT 2
)
SELECT
    rp.page_id,
    rp.page_title,
    pe.content,
    pe.embedding
FROM
    page_embeddings pe
    JOIN random_pages rp ON rp.page_title = pe.title
