CREATE VIEW `BOOK_INFO` AS

WITH       `BOOK_WITH_AUTHOR`(`Name`, `Image`, `ISBN`, `Publisher`, `Price`, `Date`, `Storage`, `Content`, `Author`) AS
(SELECT    B.`Name`, B.`Image`, B.`ISBN`, B.`Publisher`, B.`Price`, B.`Date`, B.`Storage`, B.`Content`, A.`Author`
 FROM      `BOOK` B, `AUTHOR` A
 WHERE     B.`ISBN`=A.`ISBN`)

SELECT      B.`Name`, B.`Image`, B.`ISBN`, B.`Publisher`, B.`Author`, B.`Price`, B.`Date`, B.`Storage`, B.`Content`, S.`Star`
FROM        `BOOK_WITH_AUTHOR` B LEFT OUTER JOIN `AVG_SCORE` S
ON          B.`ISBN`=S.`ISBN`;