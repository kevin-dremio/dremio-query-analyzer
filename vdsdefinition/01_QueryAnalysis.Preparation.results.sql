CREATE OR REPLACE VDS 
QueryAnalysis.Preparation.results 
AS 
SELECT 
	*, 
    "finish" - ("start" - poolWaitTime) AS "totalDurationMS"	
FROM QueriesJson.results