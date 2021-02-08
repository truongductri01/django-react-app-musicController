import React, { Component } from "react";
import { render } from "react-dom";
import Homepage from "./Homepage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <div className="center">{<Homepage />}</div>;
  }
}

// Render the component and display onto the window
render(<App />, document.getElementById("app"));
