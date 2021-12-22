import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useParams
} from "react-router-dom";

import {CenteredArticleContainer} from "./Structure"

//import "../MapRegistryComponents/css/style.scss";
import "./App.scss";

export function ArticlesListItem({articleTitle, dhsId}){
  return <div className="dhs-articles-list-item">
    <DhsArticleLink dhsId={dhsId}>
      <span className="dhs-articles-list-item-id">{dhsId+" "}</span>
      <span className="dhs-articles-list-item-title">{articleTitle}</span>
    </DhsArticleLink>
  </div>
}

export function ArticlesList({}) {
  const { language } = useParams();
  console.log("ArticlesList.js language", language)

  const indexJsonUrl = "/data/indices/"+language+".json"

  const [index, setIndex] = useState([])

  console.log("ArticlesList indexJsonUrl: ", indexJsonUrl)
  useEffect(()=>{
    fetch(indexJsonUrl).then(x=>x.json()).then(index=>{
      setIndex(index)
    })
  }, [indexJsonUrl])

  console.log("INDEX: ", index)

  return (
    <CenteredArticleContainer>
        {index.map(item=> <ArticlesListItem dhsId={item[0]} articleTitle={item[1]}/>)}
    </CenteredArticleContainer>
  );
}

export default ArticlesList;

