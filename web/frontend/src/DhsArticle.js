import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {
  useParams
} from "react-router-dom";

import {TextLink, DhsArticleLink, RealDhsArticleLink} from "./TextLink"
import {CenteredLayout} from "./Layout"

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

export function DhsArticleContent({
    article = {},
    language="de"
}) {

    console.log("ARTICLE DHS DHS: ", article)
    console.log("ARTICLE TEXT_LINKS: ", article.text_links)
    const textBlocks = article.text_blocks? article.text_blocks.map((tb,i)=>{
        const [tag, text] = tb
        return <TextBlock tag={tag} key={i} textLinks={article.text_links[i]} language={language}>{text}</TextBlock>
    }) : "Loading..."

    return (
        <div className="dhs-article">
            {textBlocks}
        </div>
    );
}
//{}



export function DhsArticle({}) {
  const { language, dhsId } = useParams();
  console.log("DhsArticle.js language", language, "dhsId:", dhsId)

  const articleJsonUrl = "/data/"+language+"/"+dhsId+".json"

  const [article, setArticle] = useState({id:true})

  useEffect(()=>{
    fetch(articleJsonUrl).then(x=>x.json()).then(newArticle=>{
        //article.lastArticle = {id: article.lastArticle? article.lastArticle.id}
        //newArticle.lastArticle = article
        setArticle(newArticle)
    }).catch(x=>{
        console.warn("DhsArticle problem loading article: ", x)
        setArticle({lastArticle: article})
    })
  }, [articleJsonUrl])

  console.log("ARTICLE: ", article)
  if(!article.id){
      return <MissingDhsArticle lastArticle={article.lastArticle}/>
  }

  return (
    <CenteredLayout>
        <DhsArticleContent article={article} language={language}/>
    </CenteredLayout>
  );
}

export function MissingDhsArticle({lastArticle={}}) {
  const { language, dhsId } = useParams();
  console.log("MissingDhsArticle.js language", language, "dhsId:", dhsId, "lastArticle.id: ", lastArticle.id)

  return (
    <CenteredLayout>
        <h1>Erreur 404: Article pas encore traité</h1>
        <p>Cet article n'a pas encore été linké par entity-fishing. La moulinette tourne, revenez plus tard.</p>
        <p>
            <a href="#" onClick={()=>window.history.back()}>Revenir en arrière {lastArticle.title? "("+lastArticle.title+")":""}</a>
        </p>
        {dhsId?
        <p>
            <RealDhsArticleLink dhsId={dhsId}>Visiter l'article du DHS original</RealDhsArticleLink>
        </p>: ""}
        
    </CenteredLayout>
  );
}

export default DhsArticle;
