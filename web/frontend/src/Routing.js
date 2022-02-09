import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css'
import {
  HashRouter as Router,
  Routes,
  Route,
  Navigate,
  //Link
  useLocation
} from "react-router-dom";

import {DhsArticle} from "./DhsArticle"
import {ArticlesList} from "./ArticlesList"
console.log("ROOOOOOUUUUTING, basename is: ", process.env.PUBLIC_URL)


export default function Routing() {
  console.log("doin' the routin', basename is: ", process.env.PUBLIC_URL)
  return (
    <Router basename={process.env.PUBLIC_URL}>
      <Routes>
        <Route path="/:language/articles/:dhsId" element={<DhsArticle />}/>
        <Route path={process.env.PUBLIC_URL+"/:language"} element={<ArticlesList />}/>
        <Route path={process.env.PUBLIC_URL+"/:language/articles"} element={<ArticlesList />}/>
        <Route exact path={process.env.PUBLIC_URL+"/"} element={<Navigate to={process.env.PUBLIC_URL+"/fr"} />} />
        <Route path='*' element={"HOLA HOLA HOW YOU DOIN?"} />
      </Routes>
    </Router>
  );
}
//
        