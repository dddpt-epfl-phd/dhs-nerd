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
      HOLLA HOWDY
      <Routes>
          <Route path="/:language/articles/:dhsId" element={<DhsArticle />}/>
          <Route path="/:language" element={<ArticlesList />}/>
          <Route path="/:language/articles" element={<ArticlesList />}/>
          <Route exact path="/" element={<Navigate to="/fr" />} />
          <Route path='*' element={"HOLA HOLA HOW YOU DOIN?"} />
      </Routes>
    </Router>
  );
}
//
        