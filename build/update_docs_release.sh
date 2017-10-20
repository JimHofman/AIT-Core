#!/bin/bash

cd ..
git checkout master
git pull
sphinx-apidoc --separate --force --no-toc -o doc/source bliss bliss/test
python setup.py build_sphinx
git checkout gh-pages
\cp doc/build/html/*.html .
\cp doc/build/html/*.js .
\cp doc/build/html/objects.inv .
\cp -r doc/build/html/_static .
\cp -r doc/build/html/_images .
git add *.html *.js _static _images

echo
echo "*** Documentation update complete ***"
echo
echo "Please review staged files, commit, and push"
echo "the changes (git push origin gh-pages)"
echo 
echo "When finished run 'git checkout master'"
