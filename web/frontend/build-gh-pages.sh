
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
