#!/bin/bash
wget -O allPolls 127.0.0.1:8000/polls
wget -O allFaculty 127.0.0.1:8000/getfaculty
rm -rf Poll
mkdir Poll
rm list.html
IP=($(sed -n 's/.*href="\([^"]*\).*/\1/p' allPolls))
echo "<html>" >> list.html
for each in "${IP[@]}"
do
  if [[ ${each:0:3} == "/po" ]] ; then
    ST=${each:7}
    ST=${ST%?}
    echo $ST
    wget -O $ST.html 127.0.0.1:8000$each
    Question=$(grep -o '<h1>.*</h1>' $ST.html | sed 's/\(<h1>\|<\/h1>\)//g')1
    Answers=$(grep -o '<label.*>.*</label>' $ST.html )
    Answers=($(echo $Answers | sed 's/<\/\?[^>]\+>//g'))
    rm $ST.html
    echo "<html>" >> $ST.html
    echo "<form action=\"../sign.php\" method=\"post\">" >> $ST.html
    echo "<fieldset><legend>$Question</legend>" >> $ST.html 
    for option in "${Answers[@]}" ; do
        echo "<input type=\"radio\" value=\"$option\" name=\"vote\"><label>$option</label>" >> $ST.html
        echo "<br>" >> $ST.html
    done
    echo "</fieldset>" >> $ST.html
    echo "<fieldset>" >> $ST.html 
    echo "<legend>Public Key</legend>" >>$ST.html
    echo "<textarea name=\"pubkey\" placeholder=\"Enter your public key\"></textarea>" >>$ST.html
    echo "<legend>Private Key</legend>" >>$ST.html
    echo "<textarea name=\"prikey\" placeholder=\"Enter your private key\"></textarea>" >>$ST.html
    echo "</fieldset>" >> $ST.html
    echo "<input type=\"text\" name=\"pollno\" value=\"$ST\" readonly hidden>" >>$ST.html
    echo "<input type=\"submit\" value=\"Vote\">" >> $ST.html
    echo "</form>" >> $ST.html
    echo "<a href=\"Poll/$ST.html\">$Question</a>" >> list.html
    echo "<br>" >> list.html
    echo "</html>" >> $ST.html
    mv $ST.html Poll/
  fi
done
echo "</html>" >> list.html
rm allPolls
