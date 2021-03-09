CREATE OR REPLACE VDS 
QueryAnalysis.Business.SelectQueryData 
AS 
SELECT 
    queryId, 
    queryTextFirstChunk AS queryText, 
	queryChunkSizeBytes, 
	nrQueryChunks, 
    TO_TIMESTAMP("start"/1000.0) AS startTime, 
    TO_TIMESTAMP("finish"/1000.0) AS finishTime, 
    CAST(totalDurationMS/60000.000 AS DECIMAL(10,3)) AS totalDurationMinutes, 
    CAST(totalDurationMS/1000.000 AS DECIMAL(10,3)) AS totalDurationSeconds, 
    "totalDurationMS", 
    outcome, 
    username, 
    requestType, 
    queryType, 
    parentsList, 
    queueName, 
    poolWaitTime, 
    planningTime, 
    enqueuedTime, 
    executionTime, 
    accelerated, 
    inputRecords, 
    inputBytes, 
    outputRecords, 
    outputBytes, 
    queryCost, 
    CONCAT('http://<DREMIO_HOST>:9047/jobs?#', "queryId") AS "profileUrl" 
FROM QueryAnalysis.Preparation.results AS results 
-- We only want select statements 
WHERE SUBSTR(UPPER("queryTextFirstChunk"), STRPOS(UPPER("queryTextFirstChunk"), 'SELECT')) LIKE 'SELECT%'
AND UPPER("queryTextFirstChunk") NOT LIKE 'CREATE TABLE%'
