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
import {AboutPage} from "./About"
import HdsThematicIndexation from './HdsThematicIndexation';
import NavBarHeader from "./Navbar.js"

const Route404 = ({tadu="DEFAULT"})=><div>THIS IS A {tadu} ROUTE</div>
export default function Routing() {

  const HdsThematicIndexationURL = process.env.PUBLIC_URL+"/data/indices/tag_tree_with_ids_all.json"
  return (
    <>
    <Router>
      <Routes basename={process.env.PUBLIC_URL}>
          <Route path="/:language/articles/:dhsId" element={<DhsArticle baseurl={process.env.PUBLIC_URL}/>}/>
          <Route path="/:language" element={<ArticlesList  baseurl={process.env.PUBLIC_URL}/>}/>
          <Route path="/:language/articles" element={<ArticlesList  baseurl={process.env.PUBLIC_URL}/>}/>
          <Route path="/:language/themes" element={<>
            <NavBarHeader/>
            <HdsThematicIndexation  treeDataJsonUrl={HdsThematicIndexationURL} baseurl={process.env.PUBLIC_URL}/>
          </>}/>
          <Route path="/:language/about" element={<AboutPage/>}/>
          <Route exact path="/" element={<Navigate to="/fr" />} />
          <Route path='*' element={<Route404/>} />
      </Routes>
    </Router>
    </>
  );
}
//
        