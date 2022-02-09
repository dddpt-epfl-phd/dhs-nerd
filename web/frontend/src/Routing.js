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

const Route404 = ({})=><div>THIS IS A DEFAULT ROUTE</div>
export default function Routing() {
  console.log("doin' the routin', basename is: ", process.env.PUBLIC_URL)
  return (
    <>
    HOLLA HOWDY
    <Router basename={process.env.PUBLIC_URL}>
      <Routes>
          <Route path="/:language/articles/:dhsId" element={<DhsArticle />}/>
          <Route path="/:language" element={<ArticlesList />}/>
          <Route path="/:language/articles" element={<ArticlesList />}/>
          <Route exact path="/" element={<Navigate to="/fr" />} />
          <Route path='*' element={<Route404/>} />
      </Routes>
    </Router>
    </>
  );
}
//
        