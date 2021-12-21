import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css'
import {
  BrowserRouter as Router,
  Routes,
  Route
  //Link
} from "react-router-dom";
import NavBarHeader from "./Navbar.js"
import App from "./App.js"


import "./Routing.scss";

export default function Routing() {
  return (
    <Router>
      <div className="main">
        <NavBarHeader/>
        <Routes>
          <Route path="/" element={<App />}/>
        </Routes>
      </div>
    </Router>
  );
}
