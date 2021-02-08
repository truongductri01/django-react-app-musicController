import React, { Component } from "react";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";
import JoinRoomPage from "./JoinRoomPage";
import Room from "./Room";

class Homepage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roomCode: null,
    };
    this.clearRoomCode = this.clearRoomCode.bind(this);
  }
  // life cycle function
  async componentDidMount() {
    fetch("/api/user_in_room")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ roomCode: data.code });
      });
  }

  renderHomePage() {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h3" component="h3">
            House Party
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link}>
              Join a Room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create a Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    );
  }

  clearRoomCode() {
    this.setState({
      roomCode: null,
    });
  }

  render() {
    console.log(this.state);
    return (
      <Router>
        <Switch>
          <Route path="/join" component={JoinRoomPage}></Route>
          <Route path="/create" component={CreateRoomPage}></Route>
          <Route
            path="/room/:roomCode"
            render={(props) => (
              <Room {...props} leaveRoomCallback={this.clearRoomCode}></Room>
            )}
          ></Route>
          <Route
            path="/"
            render={() => {
              return this.state.roomCode ? (
                <Redirect to={`/room/${this.state.roomCode}`}></Redirect>
              ) : (
                this.renderHomePage()
              );
            }}
          ></Route>
        </Switch>
      </Router>
    );
  }
}

export default Homepage;
