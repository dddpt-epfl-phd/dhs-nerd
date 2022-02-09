import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useParams,
  useLocation
} from "react-router-dom";
import {Form, Button} from "react-bootstrap"


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


export function ArticlesList({}) {
  // DEBUG START
  console.log("ArticlesList ArticlesList ArticlesList ArticlesList")
  const location = useLocation();
  console.log("ArticlesList location.pathname: ", location.pathname); // path is /contact
  // /DEBUG FIN

  const { language } = useParams();
  console.log("ArticlesList.js language", language)

  const indexJsonUrl = "/data/indices/"+language+".json"

  const [index, setIndex] = useState([])
  const [completeIndex, setCompleteIndex] = useState([])

  useEffect(()=>{
    fetch(indexJsonUrl).then(x=>x.json()).then(index=>{
      setCompleteIndex(index)
      setIndex(index)
    })
  }, [indexJsonUrl])

  const onSearchFormSubmit = (event)=>{
    const searchTerm = document.getElementById('dhs-article-text-search').value
    setIndex(searchInIndex(completeIndex, searchTerm))
    event.preventDefault()
    event.stopPropagation()
  }

  //console.log("ArticlesList indexJsonUrl: ", indexJsonUrl, " index:", index)

  return (
    <CenteredLayout>
      <Form id="dhs-article-search" onSubmit={onSearchFormSubmit}>
        <Form.Group className="mb-3" controlId="dhs-article-text-search">
          <Form.Control type="text" placeholder="Search in articles' titles..." />
        </Form.Group>
        <Button variant="primary" type="submit">
          Search
        </Button>
      </Form>
      {index.filter((a,i)=>i<NB_MAX_DISPLAYED_ARTICLES).map((item,i)=> <ArticlesListItem key={i} dhsId={item[0]} articleTitle={item[1]}/>)}
    </CenteredLayout>
  );
}

export default ArticlesList;

// <Form.Label>Search</Form.Label>
/*

*/