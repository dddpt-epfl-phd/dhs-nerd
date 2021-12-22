import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css'
import {
  BrowserRouter as Router,
  Routes,
  Route
  //Link
} from "react-router-dom";
import NavBarHeader from "./Navbar.js"

import {DhsArticleContainer} from "./DhsArticle"
import {ArticlesList} from "./ArticlesList"



import "./Routing.scss";

export default function Routing() {
  console.log("prout")
  return (
    <Router>
      <div className="main">
        <NavBarHeader/>
        <Routes>
          <Route path="/:language/articles/:dhsId" element={<DhsArticleContainer />}/>
          <Route path="/:language" element={<ArticlesList />}/>
          </Routes>
      </div>
    </Router>
  );
}
//
        