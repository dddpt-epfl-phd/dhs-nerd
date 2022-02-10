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

const Route404 = ({tadu="DEFAULT"})=><div>THIS IS A {tadu} ROUTE</div>
export default function Routing() {
  return (
    <>
    <Router>
      <Routes basename={process.env.PUBLIC_URL}>
          <Route path="/:language/articles/:dhsId" element={<DhsArticle baseurl={process.env.PUBLIC_URL}/>}/>
          <Route path="/:language" element={<ArticlesList  baseurl={process.env.PUBLIC_URL}/>}/>
          <Route path="/:language/articles" element={<ArticlesList  baseurl={process.env.PUBLIC_URL}/>}/>
          <Route exact path="/" element={<Navigate to="/fr" />} />
          <Route path='*' element={<Route404/>} />
      </Routes>
    </Router>
    </>
  );
}
//
        