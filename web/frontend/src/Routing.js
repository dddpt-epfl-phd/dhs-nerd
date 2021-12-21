import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route
  //Link
} from "react-router-dom";
import Navbar from "./Navbar.js"
import App from "./App.js"


import "./Routing.scss";

export default function Routing() {
  return (
    <Router>
      <div className="main">
        <Navbar/>
        <Routes>
          <Route path="/" element={<App />}/>
        </Routes>
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