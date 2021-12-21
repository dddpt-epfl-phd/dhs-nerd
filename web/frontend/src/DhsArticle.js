import React, { useState, useRef, useEffect, createRef, useCallback } from "react";

//import "../MapRegistryComponents/css/style.scss";
//import "./App.scss";


function textBlockToTag(textBlock, key, blockLinks = []){
    const [tag, text] = textBlock

    switch(tag) {
        case "h1":
            return <h1 key={key}>{text}</h1>
        case "h2":
            return <h2 key={key}>{text}</h2>
        case "h3":
            return <h3 key={key}>{text}</h3>
        case "p":
            return <p key={key}>{text}</p>
        default:
            return <div key={key}>{text}</div>
      } 
}

function DhsArticle({
    article = {}
}) {

    console.log("ARTICLE DHS DHS: ", article)
    const textBlocks = article.text_blocks? article.text_blocks.map((tb,i)=> textBlockToTag(tb,i)) : "no article"
    const textBlocksTags = new Set(article.text_blocks? article.text_blocks.map((tb,i)=> tb[0]) : ["no article"])
    console.log(textBlocksTags)

    return (
        <div className="dhs-article">
            {textBlocks}
        </div>
    );
}

export default DhsArticle;
//{}