import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
  //Link
} from "react-router-dom";

import {DhsArticle} from "./DhsArticle"
import {ArticlesList} from "./ArticlesList"



export default function Routing() {
  return (
    <Router>
      <Routes>
        <Route path="/:language/articles/:dhsId" element={<DhsArticle />}/>
        <Route path="/:language" element={<ArticlesList />}/>
        <Route path="/:language/articles" element={<ArticlesList />}/>
        <Route exact path="/" element={<Navigate to="/fr" />} />
      </Routes>
    </Router>
  );
}
//
        