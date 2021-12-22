import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {
  useParams
} from "react-router-dom";

import {TextLink} from "./TextLink"
import {CenteredArticleContainer} from "./Structure"

//import "../MapRegistryComponents/css/style.scss";
//import "./App.scss";




function TextWithLinks({text, textLinks=[], language="de"}){
    if(textLinks.length==0){
        console.log("textLinks.length==0", textLinks)
        return text
    }
    //console.log("textLinks: ", textLinks)
    textLinks.sort((a,b) => a.start-b.start)
    let previousTextLink = {start:0, end: 0}
    const textsAndLinks = textLinks.map((textLink,i) =>{
        //console.log("textsAndLinks mapping\npreviousTextLink:", previousTextLink, "\ntextLink: ",textLink)
        if(textLink.start>=previousTextLink.end){
            const previousTextLinkEnd = previousTextLink.end
            previousTextLink = textLink
            //console.log("textsAndLinks mapping bis, textLink: ",textLink)
            return [
                text.substring(previousTextLinkEnd, textLink.start),
                <TextLink textlink={textLink} language={language} key={i}>{text.substring(textLink.start, textLink.end)}</TextLink>
            ]
        }else{
            console.warn("Overlapping text links\npreviousTextLink:", previousTextLink, "\ntextLink: ",textLink)
        }
        return false
    }).filter(x=>x).flat()
    textsAndLinks.push(text.substring(previousTextLink.end, text.length))
    return textsAndLinks
}

function TextBlock({tag="p", textLinks = [], children="", language="de"}){
    const text = children

    //const textWithLinks = []
    switch(tag) {
        case "h1":
            return <h1>{text}</h1>
        case "h2":
            return <h2>{text}</h2>
        case "h3":
            return <h3>{text}</h3>
        case "h4":
            return <h4>{text}</h4>
        case "p":
            return <p><TextWithLinks text={text} textLinks={textLinks} language={language}/></p>
        default:
            return <div><TextWithLinks text={text} textLinks={textLinks} language={language}/></div>
      } 
}

export function DhsArticle({
    article = {},
    language="de"
}) {

    console.log("ARTICLE DHS DHS: ", article)
    console.log("ARTICLE TEXT_LINKS: ", article.text_links)
    const textBlocks = article.text_blocks? article.text_blocks.map((tb,i)=>{
        const [tag, text] = tb
        return <TextBlock tag={tag} key={i} textLinks={article.text_links[i]} language={language}>{text}</TextBlock>
    }) : "no article"

    return (
        <div className="dhs-article">
            {textBlocks}
        </div>
    );
}
//{}



export function DhsArticleContainer({
}) {
  const { language, dhsId } = useParams();
  console.log("DhsArticleContainer.js language", language, "dhsId:", dhsId)

  const articleJsonUrl = "/data/"+language+"/"+dhsId+".json"

  const [article, setArticle] = useState({})

  useEffect(()=>{
    fetch(articleJsonUrl).then(x=>x.json()).then(article=>{
      setArticle(article)
    })
  }, [articleJsonUrl])

  console.log("ARTICLE: ", article)

  return (
    <CenteredArticleContainer>
        <DhsArticle article={article} language={language}/>
    </CenteredArticleContainer>
  );
}

export default DhsArticleContainer;
