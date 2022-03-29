# Custom script to move the linked-dhs github pages website build correctly
# DO NOT RUN ALONE, is run as part of the "npm run-script build-gh-pages" npm command
# 
# What it does:
# - copy-pastes the react build into the gh-pages branch docs/ folder
# - ...while carefully preserving the gh-pages branch docs/data/ folder
# - git stages the changes to the gh-pages branch
# 
# At the end of the process, you end up on the gh-pages branch, ready to commit and push to github.
# 

fail_msg="build-gh-pages FAIL"
done_msg="[build-gh-pages.sh] DONE...\n"

echo "[build-gh-pages.sh] moving react build out of repo..."
mv build ../../gh-pages-build  || { echo "$fail_msg" ; exit 1; }
echo "$done_msg"

echo "[build-gh-pages.sh] git checkout gh-pages..."
git checkout gh-pages || { echo "$fail_msg" ; exit 1; }
echo "$done_msg"

fail_msg="build-gh-pages FAIL\n\tnote: you are now on gh-pages branch"

echo "[build-gh-pages.sh] moving docs/data/ out of the way..."
mv ../../docs/data ../../gh-pages-docs-data || { echo "$fail_msg" ; exit 1; }
echo "$done_msg"

echo "[build-gh-pages.sh] rm docs/..."
rm -r ../../docs || { echo "$fail_msg" ; exit 1; }
echo "$done_msg"

echo "[build-gh-pages.sh] move react build to docs/..."
mv ../../gh-pages-build ../../docs || { echo "$fail_msg" ; exit 1; }
echo "$done_msg"

echo "[build-gh-pages.sh] ensuring no docs/data folder from react build..."
if [ -d ../../docs/data ]; then
    echo "\tit exists... removing docs/data folder from react build..."
    rm -r ../../docs/data || { echo "$fail_msg" ; exit 1; }
fi
echo "$done_msg"

echo "[build-gh-pages.sh] moving gh-pages data back into docs/data/..."
mv ../../gh-pages-docs-data ../../docs/data || { echo "$fail_msg" ; exit 1; }
echo "$done_msg"

echo "[build-gh-pages.sh] git add docs/..."
git add ../../docs/*
echo "$done_msg"


echo "[build-gh-pages.sh] build successful, showing off git status"
git status

echo "[build-gh-pages.sh] building gh-pages: FINISHED with success\n\tnote: you are now on gh-pages branch"
