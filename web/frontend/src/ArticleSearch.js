import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useParams,
  useLocation
} from "react-router-dom";
import {Form, Button} from "react-bootstrap"



export function searchInIndex(completeIndex, searchTerm){
  const lowerCaseSearchTerm = searchTerm.toLowerCase()
  return completeIndex.filter(aid => aid[1].toLowerCase().indexOf(lowerCaseSearchTerm)!=-1)
}


export function ArticleSearch({setSearchTerm=()=>{}}){

  const onSearchFormSubmit = (event)=>{
    event.preventDefault()
    event.stopPropagation()
    const searchTerm = document.getElementById('dhs-article-text-search').value
    setSearchTerm(searchTerm)
    // TODO set URL query parameters
  }

  return (
      <>
        <Form id="dhs-article-search" onSubmit={onSearchFormSubmit}>
          <Form.Group className="mb-3" controlId="dhs-article-text-search">
            <Form.Control type="text" placeholder="Search in articles' titles..." />
          </Form.Group>
          <Button variant="primary" type="submit">
            Search
          </Button>
        </Form>
      </>
  );
}

export default ArticleSearch;
