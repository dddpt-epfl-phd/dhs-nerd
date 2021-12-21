import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {Container, Row, Col} from "react-bootstrap"

import DhsArticle from "./DhsArticle"

//import "../MapRegistryComponents/css/style.scss";
import "./App.scss";


function App({
  articleUrl = "/data/001620.json"
}) {
  const [article, setArticle] = useState({})

  useEffect(()=>{
    fetch(articleUrl).then(x=>x.json()).then(articlestr=>{
      setArticle(JSON.parse( articlestr))
    })
  }, [articleUrl])

  console.log("ARTICLE: ", article)

  return (
    <Container className="dhs-article-container">
      <Row className="justify-content-md-center">
        <Col lg="7" className="justify-content-md-center dhs-article-content">
            <DhsArticle article={article}/>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
