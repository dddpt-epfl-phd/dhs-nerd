import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {
  useParams
} from "react-router-dom";
import {Alert} from "react-bootstrap"

import {TextLink, WikidataTextLink, WikipediaTextLink, realDhsLink, RealDhsArticleLink, getWikipediaUrlFromPageId, dhsLinkClass, wikipediaLinkClass, originalDhsLinkClass} from "./TextLink"
import {CenteredLayout} from "./Layout"
import {CopyrightFooter} from "./CopyrightFooter"



function TextWithLinks({text, textLinks=[], language="de"}){
    if(textLinks.length==0){
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
    const text = children[0]
    console.log("TextBlock children: ", children)

    //const textWithLinks = []
    switch(tag) {
        case "h1":
            return <h1>{children}</h1>
        case "h2":
            return <h2>{children}</h2>
        case "h3":
            return <h3>{children}</h3>
        case "h4":
            return <h4>{children}</h4>
        case "p":
            return <p><TextWithLinks text={text} textLinks={textLinks} language={language}/></p>
        default:
            return <div><TextWithLinks text={text} textLinks={textLinks} language={language}/></div>
      } 
}

export function DhsArticleContent({
    article = {},
    language="de",
    baseurl=""
}) {    
    //"wikidata_url": "http://www.wikidata.org/entity/Q121410",
    //"wikipedia_page_title": "District d'Aarau",
    console.log("DhsArticleContent baseurl:", baseurl)

    // hack: use the search_result_name to have a nice title
    if(article.text_blocks && article.text_blocks.length>0){
        article.text_blocks[0][1] = article.search_result_name
    }


    // externalLinks to DHS, WK, WD for the first text block, the article title
    const logoSize = "20px" 
    const wikipediaUrl = article.wikipedia_page_title? getWikipediaUrlFromPageId(language, article.wikipedia_page_title):false
    const wikidataUrl = article.wikidata_url? article.wikidata_url:false
    const wikipediaLink = wikipediaUrl? <WikipediaTextLink key="wk-tl" url={wikipediaUrl}><img src={baseurl+"/wikipedia.png"} width={logoSize} height={logoSize} /></WikipediaTextLink>:""
    const wikidataLink = wikidataUrl? <WikidataTextLink key="wdt-l" url={wikidataUrl}><img src={baseurl+"/wikidata.svg"} width={logoSize} height={logoSize} /></WikidataTextLink>: ""
    const externalLinks = <span>
        <RealDhsArticleLink key="r-dhs-tl" dhsId={article.id} language={language}> <img src={baseurl+"/hds.png"} className="real-dhs-article-external-link" width={logoSize} height={logoSize} /></RealDhsArticleLink>
        {wikipediaLink}
        {wikidataLink}
    </span>
    
    const textBlocks = article.text_blocks? article.text_blocks.map((tb,i)=>{
        const [tag, text] = tb
        return <TextBlock tag={tag} key={i} textLinks={article.text_links[i]} language={language}>{[text," ", i==0? externalLinks: ""]}</TextBlock>
    }) : "Loading..."


    return (
        <div className="dhs-article">
            {textBlocks}
            <hr/>
            <CopyrightFooter>
                <RealDhsArticleLink dhsId={article.id}>Original article</RealDhsArticleLink>
                <br/>
            </CopyrightFooter>
        </div>
    );
}
//{}



export function DhsArticle({baseurl=""}) {

  const { language, dhsId } = useParams();

  const articleJsonUrl = baseurl+"/data/"+language+"/"+dhsId+".json"

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

  console.log("DhsArticle.js language", language, "dhsId:", dhsId, ", article:", article)
  if(!article.id){
      return <MissingDhsArticle lastArticle={article.lastArticle}/>
  }

  return (
    <CenteredLayout>
        <Alert className="dhs-article-info" variant="info">
            <a className={dhsLinkClass}>Blue links</a> point to other HDS articles.<br/>
            <a className={wikipediaLinkClass}>Green links</a> point to Wikipedia articles.<br/>
            <a className={dhsLinkClass+" "+originalDhsLinkClass}>Underdashed blue links</a> are links coming from the original HDS.<br/>
        </Alert>
        <DhsArticleContent article={article} language={language} baseurl={baseurl}/>
    </CenteredLayout>
  );
}

export function MissingDhsArticle({lastArticle={}}) {
  const { language, dhsId } = useParams();
  //console.log("MissingDhsArticle.js language", language, "dhsId:", dhsId, "lastArticle.id: ", lastArticle.id)

  return (
    <CenteredLayout>
        <h1>Error 404: Article not found</h1>
        <p>
            Oops, it seems this article is missing. Are you sure the article id is correct?<br/>
        </p>
        <p>
            <a href="#" onClick={()=>window.history.back()}>Go back {lastArticle.title? "("+lastArticle.title+")":""}</a>
        </p>
        {dhsId?
        <p>
            <RealDhsArticleLink dhsId={dhsId} language={language}>Visit the original HDS article</RealDhsArticleLink>
        </p>: ""}
        
    </CenteredLayout>
  );
}

export default DhsArticle;
