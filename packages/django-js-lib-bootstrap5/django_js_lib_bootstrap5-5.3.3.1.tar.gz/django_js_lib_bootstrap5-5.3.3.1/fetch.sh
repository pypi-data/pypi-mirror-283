#!/bin/bash
set +ex

VERSION="5.3.3"
URL="https://github.com/twbs/bootstrap/releases/download/v$VERSION/bootstrap-$VERSION-dist.zip"
OUTPUT_ZIP="bootstrap-$VERSION-dist.zip"
curl -L -o $OUTPUT_ZIP $URL
unzip $OUTPUT_ZIP
rm $OUTPUT_ZIP

rm -dr js_lib_bootstrap5/static/js-lib-bootstrap5
mv bootstrap-$VERSION-dist js_lib_bootstrap5/static/js-lib-bootstrap5
