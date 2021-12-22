import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useParams
} from "react-router-dom";

import {CenteredLayout} from "./Layout"


const NB_MAX_DISPLAYED_ARTICLES = 100

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

  useEffect(()=>{
    fetch(indexJsonUrl).then(x=>x.json()).then(index=>{
      setIndex(index)
    })
  }, [indexJsonUrl])


  //console.log("ArticlesList indexJsonUrl: ", indexJsonUrl, " index:", index)

  return (
    <CenteredLayout>
        {index.filter((a,i)=>i<NB_MAX_DISPLAYED_ARTICLES).map((item,i)=> <ArticlesListItem key={i} dhsId={item[0]} articleTitle={item[1]}/>)}
    </CenteredLayout>
  );
}

export default ArticlesList;

