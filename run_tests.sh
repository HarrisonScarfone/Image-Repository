#! /usr/bin/env sh

sleep 30

echo Starting service tests...

UPLOAD=$(curl -s -o /dev/null -w "%{http_code}%" -X POST -F "img=@/app/test/tulips.jpg" -F "tags=flowers" app:8000/uploadimg)
IMAGEGRABKEYWORD=$(curl -s -o /dev/null -w "%{http_code}%" -X POST -F "filename=" -F "keywords=flowers" app:8000/grabimage)
IMAGEGRABNAME=$(curl -s -o /dev/null -w "%{http_code}%" -X POST -F "file_name=tulips.jpg" -F "keywords=" app:8000/grabimage)

python3 test/test.py $UPLOAD $IMAGEGRABKEYWORD $IMAGEGRABNAME