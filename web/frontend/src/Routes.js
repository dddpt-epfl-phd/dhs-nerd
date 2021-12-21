import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Navbar from "./Navbar.js"
import App from "./App.js"


import "./Routes.scss";

export default function Routes() {
  return (
    <Router>
      <div className="main">
        <Navbar/>
        <Switch>
          <Route path="/">
            <App />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}


/*

          <Route path="/about">
            <About />
          </Route>
          <Route path="/docs">
            <Switch>
              <Route path="/docs/cadaster">
                <DocCadaster />
              </Route>
              <Route path="/docs/catastici">
                <DocCatastici />
              </Route>
              <Route path="/docs/vectorization">
                <DocVectorization />
              </Route>
              <Route path="/docs">
                <Docs />
              </Route>
            </Switch>
          </Route>
*/