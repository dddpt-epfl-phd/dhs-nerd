import React, { useState, useRef, useEffect, createRef, useCallback } from "react";
import {
    Link
  } from "react-router-dom";

import {TextLink} from "./TextLink"

//import "../MapRegistryComponents/css/style.scss";
//import "./App.scss";





function TextWithLinks({text, textLinks=[]}){
    if(textLinks.length==0){
        console.log("textLinks.length==0", textLinks)
        return text
    }
    console.log("textLinks: ", textLinks)
    textLinks.sort((a,b) => a.start-b.start)
    let previousTextLink = {start:0, end: 0}
    const textsAndLinks = textLinks.map((textLink,i) =>{
        console.log("textsAndLinks mapping\npreviousTextLink:", previousTextLink, "\ntextLink: ",textLink)
        if(textLink.start>=previousTextLink.end){
            const previousTextLinkEnd = previousTextLink.end
            previousTextLink = textLink
            console.log("textsAndLinks mapping bis, textLink: ",textLink)
            return [
                text.substring(previousTextLinkEnd, textLink.start),
                <TextLink textlink={textLink} zulu="43">{text.substring(textLink.start, textLink.end)}</TextLink>
            ]
        }else{
            console.warn("Overlapping text links\npreviousTextLink:", previousTextLink, "\ntextLink: ",textLink)
        }
        return false
    }).filter(x=>x).flat()
    textsAndLinks.push(text.substring(previousTextLink.end, text.length))
    return textsAndLinks
}

function textBlockToTag(textBlock, key, textLinks = []){
    const [tag, text] = textBlock

    const textWithLinks = [<TextWithLinks text={text} textLinks={textLinks}/>]
    console.log("textWithLinks", textWithLinks)
    switch(tag) {
        case "h1":
            return <h1 key={key}>{textWithLinks}</h1>
        case "h2":
            return <h2 key={key}>{textWithLinks}</h2>
        case "h3":
            return <h3 key={key}>{textWithLinks}</h3>
        case "h4":
            return <h4 key={key}>{textWithLinks}</h4>
        case "p":
            return <p key={key}>{textWithLinks}</p>
        default:
            return <div key={key}>{textWithLinks}</div>
      } 
}

function DhsArticle({
    article = {}
}) {

    console.log("ARTICLE DHS DHS: ", article)
    console.log("ARTICLE TEXT_LINKS: ", article.text_links)
    const textBlocks = article.text_blocks? article.text_blocks.map((tb,i)=> textBlockToTag(tb,i, article.text_links[i])) : "no article"

    return (
        <div className="dhs-article">
            {textBlocks}
            <TextLink/>
        </div>
    );
}

export default DhsArticle;
//{}