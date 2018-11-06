document -refers to the webpage
var -to declare any variable in javascript
#To start the script we start with
<script language="javascript" type="text/javascript">
<!--Hide javascript


-->
</script>
#if web page does not support javascript
<onscript><h3>page does not support the javascript</h3></noscript>

#to print in the page
document.write("hello");

#Comment in js - //

#bool -true and false

#clear console
clear()

#to find the length of string
<string>.length

#undefined means it was created with nothing

# nulll means data unknown

#alert function is used to output the data to screen
#console.log function is used to output to console
#prompt function is used to take the input from the user

#operators
== is comparing (“2” == 2 is true)
=== is comparing with datatype (“2” == 2 is false)
&& || !
Note: Avoid using == 

If (condition){
} else if {
}else {
}

For (var i; i < length; i++){}

#to know the datatype
typeof <variable>

#type cast
parseInt()

DOM
myvariable.textContent - This returns just the text
myvariable.innerHTML - This returns the actual html
myvariable.getAttribute() - This returns the original attribute
myvariable.setAttribute() - This allowed you to set an attribute
Jquary
$('a')
Selecting all elements from the class "container"
$(".container")
Selecting all elements with id "special"
$("#special")

$ to access
.eq(0) - get array element

Keypress
$('input').eq(0).keypress(function() {
  $('h3').toggleClass("turnRed");
})

*************************************************************
#output the messages to the console
console.log() #Takes a string/number
console.error() #Takes a string
console.warn() #Takes a string

ex:-
console.log("%cHello world","color:blue") #%c is the css attahced to it
console.log("%cHello world","color:blue;backgroundcolor:pink")
**********************************************************************









