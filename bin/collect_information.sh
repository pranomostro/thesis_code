#!/usr/bin/env sh

export PROJECT=$(basename $(pwd))

cd src/test/java

find . -regex '.*\.java$' | grep -Ev 'MyTestExecutionListener|MyRunListener' >$PROJECT-tests.txt

while read p; do
	tr '\n' ' ' <$p >>"$PROJECT-bbox.txt"
	echo '' >>"$PROJECT-bbox.txt"
done <$PROJECT-tests.txt

sed -i 's/^\.\///;s/\.java$//;s/\//./g' $PROJECT-tests.txt

cd ../../..

cd src/main/java

find . -regex '.*\.java$' | grep -v '\/test\/' | xargs -L 1 wc -l | sed 's/\.\///' >source-lines.txt

cd ../../..

mvn org.pitest:pitest-maven:mutationCoverage >main.log

LASTPIT=target/pit-reports/$(ls target/pit-reports/ | sort -n | tail -1)/mutations.xml

xmllint --format ${LASTPIT} >mutations.xml

if [ ! $(tail -1 mutations.xml) = "</mutations>" ]; then
	echo 'FAIL: mutation coverage not finished';
	exit
fi

mvn -X test >>main.log

cd target/jacoco/

RESDIR=$(ls | grep -E '^20' | sort -n | tail -1)

/home/adrian/bachelor/teamscale-jacoco-agent/bin/convert -s 1000000 -t -c /home/adrian/bachelor/$PROJECT/target/classes/ -i ${RESDIR} -o ./out

jq <out-1.json >../../coverage.json

cd ../..

mkdir /home/adrian/bachelor/data/$PROJECT

mv main.log mutations.xml coverage.json src/test/java/$PROJECT-tests.txt src/main/java/source-lines.txt src/test/java/$PROJECT-bbox.txt /home/adrian/bachelor/data/$PROJECT

cd /home/adrian/bachelor/data/$PROJECT

extract_matrix.py $PROJECT
extract_coverage.py $PROJECT
