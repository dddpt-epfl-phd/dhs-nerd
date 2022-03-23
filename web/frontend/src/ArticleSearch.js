import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {DhsArticleLink} from "./TextLink"
import {
  useSearchParams,
  useParams,
  useNavigate
} from "react-router-dom";
import {Form, Button} from "react-bootstrap"



export function searchInIndex(completeIndex, searchTerm){
  const lowerCaseSearchTerm = searchTerm.toLowerCase()
  return completeIndex.filter(aid => aid[1].toLowerCase().indexOf(lowerCaseSearchTerm)!=-1)
}


export function ArticleSearch(){

  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchTerm, setSearchTerm] = useState(searchParams.get("q"));
  const { language } = useParams();

  // set searchTerm on form submit
  const onSearchFormSubmit = (event)=>{
    event.preventDefault()
    event.stopPropagation()
    setSearchTerm(document.getElementById('dhs-article-text-search').value)
  }

  // if search term changed -> go to search apge
  useEffect(()=>{
    if(searchTerm){
      // go to articles list page in given language
      navigate("/"+language)
      // set URL get parameters ?q=XXX
      setSearchParams({"q": searchTerm})
    }
  }, [searchTerm])

  return (
    <Form id="dhs-article-search" onSubmit={onSearchFormSubmit}>
      <Form.Control id='dhs-article-text-search' type="text" placeholder="Search in articles' titles..." defaultValue={searchTerm} name="q"/>
      <Button variant="primary" type="submit">
        Search
      </Button>
    </Form>
  );
}

export default ArticleSearch;
