WITH target_links AS (
    SELECT
        pl_target_id
    FROM
        pagelinks
    WHERE
        pl_from = {page_id}
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