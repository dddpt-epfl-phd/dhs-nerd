import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useLocation,
  useSearchParams,
  useParams,
  useNavigate
} from "react-router-dom";
import {Form, Button} from "react-bootstrap"



export function searchInIndex(completeIndex, searchTerm){
  const lowerCaseSearchTerm = searchTerm.toLowerCase()
  return completeIndex.filter(aid => aid[1].toLowerCase().indexOf(lowerCaseSearchTerm)!=-1)
}


export function ArticleSearch({setSearchTerm=()=>{}}){

  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams();
  const { language } = useParams();

  const onSearchFormSubmit = (event)=>{
    event.preventDefault()
    event.stopPropagation()
    const searchTerm = document.getElementById('dhs-article-text-search').value
    // go to root of given language
    navigate("/"+language)
    if(searchTerm){
      // set URL get parameters ?q=XXX
      setSearchParams({"q": searchTerm})
    }
  }

  return (
      <>
        <Form id="dhs-article-search"  onSubmit={onSearchFormSubmit}>
          <Form.Group className="mb-3" controlId="dhs-article-text-search">
            <Form.Control type="text" placeholder="Search in articles' titles..." name="q"/>
          </Form.Group>
          <Button variant="primary" type="submit">
            Search
          </Button>
        </Form>
      </>
  );
}

export default ArticleSearch;
