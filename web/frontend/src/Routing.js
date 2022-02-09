import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css'
import {
  HashRouter as Router,
  Routes,
  Route,
  Navigate
  //Link
} from "react-router-dom";

import {DhsArticle} from "./DhsArticle"
import {ArticlesList} from "./ArticlesList"
console.log("ROOOOOOUUUUTING, basename is: ", process.env.PUBLIC_URL)


export default function Routing() {
  return (
    <Router basename={process.env.PUBLIC_URL}>
      <Routes>
        <Route path="/:language/articles/:dhsId" element={<DhsArticle />}/>
        <Route path={process.env.PUBLIC_URL+"/:language"} element={<ArticlesList />}/>
        <Route path={process.env.PUBLIC_URL+"/:language/articles"} element={<ArticlesList />}/>
        <Route exact path={process.env.PUBLIC_URL+"/"} element={<Navigate to={process.env.PUBLIC_URL+"/fr"} />} />
      </Routes>
    </Router>
  );
}
//
        