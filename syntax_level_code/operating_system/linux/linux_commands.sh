# Shortcuts in linux
clt+shift+c : copy in terminal
clt+shift+c : paste in terminal
clt+c       : to stop the running process in terminal
clt+shift+x : to cut in terminal
clt+l       : to clear screen

*************************************************************************************************************************************
#cp file from one server to another
$ scp foobar.txt your_username@remotehost.edu:/some/remote/directory
 
what is scp ?
#scp allows files to be copied to, from, or between different hosts. It uses ssh for data transfer and provides the same authentication and same level of security as ssh.
http://www.hypexr.org/linux_scp_help.php

#how to copy file from remote server to local using key(only file can be copied)
scp -i <key_file> <remoteuser@ipaddress:<filepath/filename> <filepath>/
ex.
scp -i ~/ace-aws1.pem ubuntu@ec2-54-163-155-227.compute-1.amazonaws.com:/mnt/data/kendavar/missing_documents.txt /home/vulcantech/kendavar/Ace/ace_pr/
#if directory add -r
scp -i ~/ace-aws1.pem -r ubuntu@ec2-54-163-155-227.compute-1.amazonaws.com:/mnt/data/kendavar/ace /home/vulcantech/kendavar/Ace/ace_pr/

#how to copy file from local to remote server(only file can be copied)
scp -i <keyfile> <filepath>/<filename> <remoteuser@ipaddress:<filepath>/
ex.
scp -i ~/ace-aws1.pem /home/vulcantech/kendavar/Ace/missing_document_png/10ebe753d9e18abed9b50943d1114575_png  ubuntu@ec2-54-163-155-227.compute-1.amazonaws.com:/mnt/data/kendavar/missing_doc_png/
*************************************************************************************************************************************
# ssh to remote host 
ssh remote_username@remote_host

what is ssh?
#SSH, or Secure Shell, is a protocol used to securely log onto remote systems. It is the most common way to access remote Linux and Unix-like servers, such as VPS instances.
*************************************************************************************************************************************
# to create the tunnel between two machine 
$ ssh -L 6606:localhost:3306 -o ServerAliveInterval=60 srinithi@192.168.1.100
 "port has to be ur own number for connection"
$ mysql -P 6606 -h 192.168.1.100 -u root -p 


#used to convert first page of pdf to png image
$ Convert pdfname.pdf[0] <imagename>.png
e.g. $ convert ExMan_CSC.pdf[0] ex.png

#using pdfcario convert first page pdf to image
pdftocairo -png -singlefile <pdfname>.pdf <filepath/name> #dont give the formate its automatically made
pdftocairo -png -singlefile ExMan_CSC.pdf cario

#Shortcuts in nano
Select: ALT + M + A
Copy: ALT + 6
Paste: CTRL + U
**************************************************************************************************************************************
#cp directory in linux
cp -r <directoryname> <folderpath>
ex, cp -r src /mnt/data/kendavar/palani/

#copy file in linux
cp <filename> <folderpath>
ex. cp merlot.py /mnt/data/kendavar/ace/saintleo_oer_v2/merlot/
************************************************************************************************************************************************
#screen
#Screen is a full-screen software program that can be used to multiplexes a physical console between several processes (typically interactive shells). It offers a user to open several separate terminal instances inside a one single terminal window manager.
$ screen
Ctrl-A to see all the comands
Ctrl-A + d to exit

#When you have more than 1 screen session, you need to type the screen session ID. Use screen -ls to see how many screen are available.
$ screen -ls

#re attach a screen
"After you detach the screen, let say you are disconnecting your SSH session and going home. In your home, you start to SSH again to your server and you want to see the progress of your download process. To do that, you need to restore the screen." 
screen -r

#logging the screen
"With this screen logging, you don’t need to write down every single command that you have done. To activate screen logging function, just press “Ctrl-A” and “H“. (Please be careful, we use capital ‘H’ letter. Using non capital ‘h’, will only create a screenshot of screen in another file named hardcopy)."
Ctrl-A + H
screen -L

#set password
mkpasswd <password>

#open allready attached screen
Attach to a session which is already attached elsewhere (multi-display mode). Screen refuses to attach from within itself. But when cascading multiple screens, loops are not detected; take care.
screen -x <screenname>

#name a screen
#Set the name of the new session to sessionname. This option can be used to specify a meaningful name for the session in place of the default tty.host suffix. This name identifies the session for the screen -list and screen -r commands. 
screen -S <screename>

#how to move the cursor in the screen 
Ctrl-A+esc+up arrow
--to exit press esc 

#how to switch in screen
cltr+a+n

#how to check what screen I am in
echo $STY 
 
*************************************************************************************************************************************
#To check if the links is broken or not in a link
wget --spider -r -nd -nv  -l 1 -w 2 -o error.log <link>

#To check if the pattern is present in file or not 
grep -Po '(?<=href=")[^"]*' *.html > link.html
-p is perl regex
***************************************************************************************************************************************
#how to open a tab in terminal
ctl+shift+t

#how to search for a command in linux
clt+r

#double click copy
double click select 
shift+insert
*************************************************************************************************************
#vi editor
Martin is an IT consultant. Martin likes
snowboarding and mountain biking. Martin has
worked on UNIX systems for over 15 years. Martin also
worked for many years before that on mainframes.
Martin lives in London.

:%s/^\(Martin\)/Mr \1 Wicks/g
Here's a breakdown of the command into its components:
:%s - Instructs vi to perform a substitution.
/ - Pattern separator.
^\(Martin\) - Look for lines starting with the string Martin, and save the string in buffer 1.
/ - Pattern separator.
Mr \1 Wicks - Substitute the string located with the string Mr, followed by the contents of buffer 1 followed by the string Wicks.
/ - Pattern separator.
g - Global change (that is, change every occurrence on every line matched).'

*************************************************************************************************
#sending mail using ,mutt
echo "This is the message body" | mutt -a "/path/to/file.to.attach" -s "subject of message" -- recipient@domain.com
echo <message> | mutt -a "<filename/filepath>" -- -s "<subject>"  <to> -c <cc>
-- to tell the end of the file

echo "I love you body" | mutt -s "ZIP" -e 'my_hdr From:AdOps_AutoMailer <AdOps_AutoMailer@amazon.com>' -- aggrajat@amazon.com

*********************************************************************************************************
#pdf spliting using pdftk
I did exactly that using pdktk, a command-line tool.

If pdftk is not already installed, install it like this on a Debian or Ubuntu-based computer.

$ sudo apt-get update
$ sudo apt-get install pdftk
Then, to make a new pdf with just pages 1, 2, 4, and 5 from the old pdf, do this:

$ pdftk myoldfile.pdf cat 1 2 4 5 output mynewfile.pdf
Note that cat and output are special pdftk keywords. cat specifies the operation to perform on the input file. output signals that what follows is the name of the output pdf file.

You can specify page ranges like this:

$ pdftk myoldfile.pdf cat 1-2 4-5 output mynewfile.pdf
pdftk has a few more tricks in its back pocket. For example, you can specify a burst operation to split each page in the input file into a separate output file.

$ pdftk myoldfile.pdf burst 
By default, the output files are named pg_0001.pdf, pg_0002.pdf, etc.

pdftk is also capable of merging multiple pdf files into one pdf.

$ pdftk pg_0001.pdf pg_0002.pdf pg_0004.pdf pg_0005.pdf output mynewfile.pdf 
That would merge the files corresponding to the first, second, fourth and fifth pages into a single output pdf.
***************************************************************************************************************************
#dowload files from the web
sudo apt-get install wget
wget url
wget -o url >filename
wget -spder url #check the status of the url

**************************************************************************************************
 chmod 400 vulcan.pem

***********************************************************************************************************************
$rename "repace regex string" files.extinction 
regex string 's/\<match>$/\<to>/' 
rename 's/\.pdf$/\_pdf/' *.pdf

****************************************************************************************************************************************
alias :-
#It makes possible a command or group of command to run on a pre-set string.
#Ex:-
alias p="pwd" 
alias a="ps -ef | grep 'python'"
#Aternative:-
unalias :-
#ex:-
unalias p #resets the previous alias p="pwd" to pwd
unalias -a #resets all the entires from the current list of alias 




