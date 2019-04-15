#!/bin/bash
wget -O allFaculty 127.0.0.1:8000/getfaculty

wget -O allPolls 127.0.0.1:8000/polls
rm -rf Poll
mkdir Poll
rm list.html
IP=($(sed -n 's/.*href="\([^"]*\).*/\1/p' allPolls))
echo "<html>" >> list.html
echo "<head><link href=\"../poll.css\" rel=\"stylesheet\"></head><body><div id=\"main\"><div id=\"first\">" >> list.html
echo "<h1>Polls Available</h1>" >>list.html
for each in "${IP[@]}"
do
    if [[ ${each:0:3} == "/po" ]] ; then
      ST=${each:7}
      ST=${ST%?}
      echo $ST
      wget -O $ST.html 127.0.0.1:8000$each
      Question=$(grep -o '<h1>.*</h1>' $ST.html | sed 's/\(<h1>\|<\/h1>\)//g')
      Answers=$(grep -o '<label.*>.*</label>' $ST.html )
      Answers=($(echo $Answers | sed 's/<\/\?[^>]\+>//g'))
      rm $ST.html
      echo "<html>" >> $ST.html
      echo "<head><link href=\"../poll.css\" rel=\"stylesheet\"></head><body><div id=\"main\"><div id=\"first\">" >> $ST.html
      echo "<form action=\"../sign.php\" method=\"post\">" >> $ST.html
      echo "<h1>$Question</h1>" >> $ST.html
      i=0
      for option in "${Answers[@]}" ; do
          echo "<input type=\"radio\" value=\"$i\" name=\"vote\"><label>$option</label>" >> $ST.html
          echo "<br>" >> $ST.html
          i=$(($i+1))
      done
      echo "<input type=\"text\" name=\"pollno\" value=\"$ST\" readonly hidden>" >>$ST.html
      echo "<div class=\"container\"><input type=\"submit\" value=\"Vote\"></div>" >> $ST.html
      echo "</form>" >> $ST.html
      echo "<form action=\"../reveal.php\" method=\"post\">" >> $ST.html
      echo "<input type=\"text\" name=\"pollno\" value=\"$ST\" readonly hidden>" >>$ST.html
      echo "<div class=\"container\"><input type=\"submit\" value=\"Reveal\"></div>" >> $ST.html
      echo "</form></div></div></body>" >> $ST.html

      echo "<a href=\"Poll/$ST.html\">$Question</a>" >> list.html
      echo "<br><br>" >> list.html
      echo "</html>" >> $ST.html
      mv $ST.html Poll/
    fi
done
echo "</div></div></body></html>" >> list.html
rm allPolls

# wget -O allReveals 127.0.0.1:8000/reveal
# rm -rf Reveal 
# mkdir Reveal 
# rm listR.html
# IP=($(sed -n 's/.*href="\([^"]*\).*/\1/p' allReveals))
# echo "<html>" >> listR.html
# for each in "${IP[@]}"
# do
#     if [[ ${each:0:3} == "/re" ]] ; then
#       ST=${each:7}
#       ST=${ST%?}
#       echo $ST
#       wget -O $ST.html 127.0.0.1:8000$each
#       Question=$(grep -o '<h1>.*</h1>' $ST.html | sed 's/\(<h1>\|<\/h1>\)//g')
#       Answers=$(head -n 1 ${ST}vote.html)
#       rm $ST.html
#       echo "<html>" >> $ST.html
#       echo "<form action=\"../reveal.php\" method=\"post\">" >> $ST.html
#       echo "<fieldset><legend>$Question</legend>" >> $ST.html
#       echo "<h1>$Answers</h1>" >>$ST.html
#       echo "</fieldset>" >> $ST.html
#       echo "<input type=\"text\" name=\"pollno\" value=\"$ST\" readonly hidden>" >>$ST.html
#       echo "<input type=\"submit\" value=\"Reveal\">" >> $ST.html
#       echo "</form>" >> $ST.html
#       echo "<a href=\"Poll/$ST.html\">$Question</a>" >> listR.html
#       echo "<br>" >> listR.html
#       echo "</html>" >> $ST.html
#       mv $ST.html Reveal/
#     fi
# done
# echo "</html>" >> listR.html
# rm allReveals

