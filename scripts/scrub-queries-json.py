import gzip
import json
import math
import os
import sys

chunkSize = 4096

if len(sys.argv) < 4:
    print('This script is used to scrub the queries*.json files in a folder to break up'
          'the queryText field into 4096 character chunks. This is to ensure the resulting queries.json file '
          'can be used as a data source in Dremio and analysis can be made upon it via VDSs. '
          'The script also renames elements in queries.json for Dremio 4.5 and above to make the data compatible with earlier Dremio versions.'
          'It requires three input parameters, the first is the full path to the Dremio logs directory, the second is '
          'the full path to the directory where we want to place the scrubbed files and the third is the '
          'hostname where the queries.json files came from.\n\n'
          'USAGE: python scrub-queries-json.py <full_path_to_dremio_log_dir> <full_path_to_scrubbed_dir> <hostname>')
    sys.exit(1)

for queriesFile in os.listdir(sys.argv[1]):
    if queriesFile.endswith(".json") or queriesFile.endswith(".gz"):
        queriesFileName = os.path.basename(queriesFile)
        queriesPath = os.path.join(sys.argv[1], queriesFile)
        queriesHeaderPath = os.path.join(sys.argv[2], 'header.' + sys.argv[3] + "." + queriesFileName + ('.gz' if queriesPath[-3:] != '.gz' else ''))
        queriesChunksPath = os.path.join(sys.argv[2], 'chunks.' + sys.argv[3] + "." + queriesFileName + ('.gz' if queriesPath[-3:] != '.gz' else ''))
        if queriesPath[-3:] == '.gz':
            infile = gzip.open(queriesPath, "rt")
        else:
            infile = open(queriesPath, "r")
        headerFile = gzip.open(queriesHeaderPath, 'wt')
        chunksFile = gzip.open(queriesChunksPath, 'wt')
        data = [json.loads(line) for line in infile]
        for item in data:
            # if Dremio 4.5+ elements are present, rename them to make them compatible with existing VDS definitions
            if 'queuedTime' in item:
                item['enqueuedTime'] = item['queuedTime']
                del item['queuedTime']
            if 'runningTime' in item:
                item['executionTime'] = item['runningTime']
                del item['runningTime']
            # if outcomeReason is present, make sure it fits inside 32k character limit for Dremio string field
            if 'outcomeReason' in item:
                outcomeReason = item['outcomeReason'];
                if len(outcomeReason) > 32000:
                    item['outcomeReason'] = outcomeReason[0:31999]
            queryText = item['queryText']
            queryId = item['queryId']
            outitem = item
            del outitem['queryText']
            lenQueryText = len(queryText)
            nrChunks = math.ceil(float(lenQueryText)/chunkSize)
            outitem['queryChunkSizeBytes'] = chunkSize
            outitem['nrQueryChunks'] = nrChunks
            queryTextFirstChunk = ''
            for j in range(0, int(nrChunks)):
                sqlChunk = queryText[j * chunkSize:(j + 1) * chunkSize]
                if j == 0:
                    queryTextFirstChunk = sqlChunk
                queryChunkDict = {'queryId': queryId, 'queryChunk': j, 'queryChunkText': sqlChunk}
                chunkBytes = chunksFile.write(json.dumps(queryChunkDict) + '\n')

            outitem['queryTextFirstChunk'] = queryTextFirstChunk
            headerBytes = headerFile.write(json.dumps(outitem) + '\n')

        headerFile.close()
        chunksFile.close()
        infile.close()