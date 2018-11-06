//How to create a css file and link to a js file
//*****************************************************************************************
//How to dynamically edit classes
//App.js
let classes = []; // Create a classes array
if (this.state.persons.length <=2) {
  classes.push('red'); //push the styles

}


return (
  <div className="App">
      <h1> Hi, Im a React App</h1>
       <p className={classes.join(' ')}>This is working</p> //add classname with classes.
       //Note classes should be a string.
      <button
      style = {style}
      onClick={this.togglepersonhandler}>Switch Name</button>
      {persons}
  </div>
);
//**********************************************************************************
//App.css
//Create a class in css. App.css is a global css 
/*.red {
  color: 'red';
}*/