import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useParams,
  useSearchParams
} from "react-router-dom";
import {Alert} from "react-bootstrap"


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

export function searchInIndex(completeIndex, searchTerm){
  const lowerCaseSearchTerm = searchTerm.toLowerCase()
  return completeIndex.filter(aid => aid[1].toLowerCase().indexOf(lowerCaseSearchTerm)!=-1)
}


export function ArticlesList({baseurl=""}) {
  const { language } = useParams();
  console.log("ArticlesList.js language", language, "----------------------------------")
  
  const indexJsonUrl = baseurl+"/data/indices/"+language+".json"

  const [index, setIndex] = useState([])
  const [completeIndex, setCompleteIndex] = useState([])

  const [searchParams] = useSearchParams();
  const query = searchParams.get("q")
  console.log("AL searchParams query", query)

  useEffect(() => {
    document.title = "The Linked HDS"
  }, []);

  // filter index based on URL get parameter ?q=XX
  useEffect(()=>{
    if(query){
      console.log("ArticlesList filtering based on query:", query)
      setIndex(searchInIndex(completeIndex, query))
    }else{
      setIndex(completeIndex)  
    }
  }, [query, completeIndex])

  // fetch index json
  useEffect(()=>{
    fetch(indexJsonUrl).then(x=>x.json()).then(loadedIndex=>{
      setCompleteIndex(loadedIndex)
      setIndex(loadedIndex)
    })
  }, [indexJsonUrl])

  //console.log("ArticlesList indexJsonUrl: ", indexJsonUrl, " index:", index)

  return (
    <CenteredLayout>
      <Alert className="dhs-article-info" variant="info">
          Using the search bar above you can search for articles.<br/>
          Search is only performed on articles' titles (exact match).<br/>
      </Alert>
      {
        completeIndex.length===0? "Loading articles index..." : (
          index.length>0 ?
            index.filter((a,i)=>i<NB_MAX_DISPLAYED_ARTICLES).map((item,i)=> <ArticlesListItem key={i} dhsId={item[0]} articleTitle={item[1]}/>) :
            'No articles with title matching "'+query+'".'
        )
      }
    </CenteredLayout>
  );
}

export default ArticlesList;

// <Form.Label>Search</Form.Label>
/*

*/