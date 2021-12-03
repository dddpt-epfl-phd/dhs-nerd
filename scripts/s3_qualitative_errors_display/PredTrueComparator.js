

/**
 * needs:
 * - display at token-level:
 *      + true-positive: correct prediction
 *      + false-positive: prediction on a non-entity token
 *      + wrongly-predicted-positive: wrong prediction on an entity-token
 *      + false-negative: predicted nothing on an entity-token
 *      + labels
 * 
 * Proposition:
 * - parse conllu files in list of js token obj
 * - functions:
 *      + comparePredTrue() combine pred&true lists of tokens in single token list with html-classes pt, pf, ut, l
 *      + visualizeDocument() shows list of tokens with html-classes
 *      + visualizePredTrueComparison() combines both functions for the best
 * - token: unclassed JS obj with fields
 *      - text: text of token
 *      - separator (optional): str, separator(s) specification after the token by default a space, can contain:
     *      - EndOfLine (optional): boolean for <br/>
 *          - EndOfParagraph (optional): boolean for <p>...</p>
 *          - NoSpaceAfter (optional): whether to add a space after
 * - visualizeDocument() arguments:
 *      + tokens, with visualizationHtmlClasses property
 *      + relevantFields, list of fields to display for each token
 */



VIZ_HTML_CLASSES_PROPERTY = "visualizationHtmlClasses"
END_OF_LINE_PROPERTY = "EndOfLine"
END_OF_PARAGRAPH_PROPERTY = "EndOfParagraph"

// css classes for tokens
CSS_AS_STRING = '\n.nlp-token-snapshot-div{\n    height: 2.5em;\n    margin-bottom: 1em;\n    background-color: #cfe2ff;\n    border: 1px solid #b6d4fe;\n    color: #084298;\n    padding: 0.5em;\n    border-radius: 5px;\n}\n\n.nlp-labelled-token {\n    border-radius: 3px;\n    padding: 1px 3px 2px;\n    font-weight: bold;\n    /*color: #ffffff;*/\n}\n.nlp-active-token{\n    box-shadow: 0px 3px 4px 2px #aaaaaa;\n}\n\n/*.true-negative {\n    background-color: beige;\n}*/\n\n\n.true-positive {\n    color: #0f5132;\n    background-color: #d1e7dd;\n}\n\n\n.false-negative {\n    color: #842029;\n    background-color: #f0a8ae;\n}\n\n\n.false-positive {\n    color: #990099;\n    background-color: #ffccff;\n\n}\n\n\n.wrongly-predicted-positive {\n    color: #664d03;\n    background-color: #ffe799;\n}\n\n'
NLP_LABELLED_TOKEN_CLASS = "nlp-labelled-token"
NLP_ACTIVE_TOKEN_CLASS = "nlp-active-token"

// css classes for token prediction status
TRUE_NEGATIVE_LABEL = "true-negative"
TRUE_POSITIVE_LABEL = "true-positive"
FALSE_NEGATIVE_LABEL = "false-negative"
FALSE_POSITIVE_LABEL = "false-positive"
WRONGLY_PREDICTED_POSITIVE_LABEL = "wrongly-predicted-positive"

function checkTokensAreIdentical(tokens1, tokens2){
    if(tokens1.length != tokens2.length){ return false }
    for(i=0; i<tokens1.length; i++){
        if(tokens1[i].text != tokens2[i].text){ return false }
    }
    return true
}

function htmlTagHasClass(htmlTag, className) {
    return (' ' + htmlTag.className + ' ').indexOf(' ' + className+ ' ') > -1;
}

function cleanTokenPredField(token, predField, newpredField){
    token[newpredField] = token[predField]
    if(token[newpredField]=="" || token[newpredField]=="-"){
        token[newpredField] = undefined
    }
}

/** Combines True and prediction token in a single list.
 * 
 * Adds prediction class to "visualizationHtmlClasses" property of true tokens with possible values:
 * - true-positive: correct prediction
 * - false-positive: prediction on a non-entity token
 * - wrongly-predicted-positive: wrong prediction on an entity-token
 * - false-negative: predicted nothing on an entity-token
 */
function combinePredTrue(predTokens, trueTokens, predField, relevantFields=[]){
    if( !checkTokensAreIdentical(predTokens, trueTokens) ){
        throw Error(`combinePredTrue() unidentical predTokens and trueTokens\npredTokens: ${predTokens}\ntrueTokens: ${trueTokens}`)
    }
    if( !relevantFields.includes(predField)){
        relevantFields.push(predField)
    }
    
    trueTokens.forEach((trueToken,i)=>{
        // getting the prediction status
        let predToken = predTokens[i]

        let predictionStatus = ""
        if( trueToken[predField]!==undefined ){
            if( predToken[predField]===undefined ){
                predictionStatus = FALSE_NEGATIVE_LABEL
            } else if( trueToken[predField] == predToken[predField] ){
                predictionStatus = TRUE_POSITIVE_LABEL
            } else{
                predictionStatus = WRONGLY_PREDICTED_POSITIVE_LABEL
            }
        } else{
            if( predToken[predField]!==undefined ){
                predictionStatus = FALSE_POSITIVE_LABEL
            } else{
                predictionStatus = TRUE_NEGATIVE_LABEL
            }
        }
        //console.log("combinePredTrue, token.text: ", trueToken.text, " true: ",trueToken[predField] , " pred:", predToken[predField], " true==pred: ", trueToken[predField] == predToken[predField], " predictionStatus:", predictionStatus)
        //adding predToken relevant fields to trueToken
        relevantFields.forEach(rf => {
            trueToken["pred"+rf] = predToken[rf]
        })
        // adding prediction status to trueToken.visualizationHtmlClasses
        if( VIZ_HTML_CLASSES_PROPERTY in trueToken){
            trueToken[VIZ_HTML_CLASSES_PROPERTY].push(predictionStatus)
        } else{
            trueToken[VIZ_HTML_CLASSES_PROPERTY] = [predictionStatus]
        }
    })
    return trueTokens
}

function span(content, cssClasses=[], attributes={}){
    attributesString = Object.keys(attributes).map(attr=> `${attr}="${attributes[attr]}"`).join(" ")
    text = `<span class="${cssClasses.join(" ")}" ${attributesString}>${content}</span>`
    return text
}

function tokenToText(token, relevantFields=[], onMouseOver=""){
    cssClasses = VIZ_HTML_CLASSES_PROPERTY in token? token[VIZ_HTML_CLASSES_PROPERTY] : []
    if(!cssClasses.includes(TRUE_NEGATIVE_LABEL)){
        cssClasses.push(NLP_LABELLED_TOKEN_CLASS)
    }
    attributes = {
        "onmouseover": onMouseOver
    }
    relevantFields.forEach(f => {
        attributes[`data-${f}`] = token[f]
    })
    // dataString = relevantFields.map(f => `data-${f}="${token[f]}"`).join(" ")
    // ending = token[END_OF_PARAGRAPH_PROPERTY]? "</p>\n<p>" : (token[END_OF_LINE_PROPERTY]? "<br/>" : " ")
    // text = `<span class="${cssClasses}" ${dataString} onmouseover="${onMouseOver}">${token.text}</span>`+ending
    const tokenStr = span(token.text, cssClasses, attributes)
    //console.log("tokenToText() token:", token, ", tokenStr: ", tokenStr)
    return tokenStr
}

/**
 * 
 * @param {*} tokens 
 * @param {*} relevantFields 
 */
function visualizeDocument(tokens, relevantFields=[], onTokenMouseOver = ""){
    const tokensStr = tokens.map(t=> tokenToText(t, relevantFields, onTokenMouseOver)).join("\n")
    console.log("visualizeDocument(), tokensStr: ", tokensStr)
    return "<div><p>" + tokensStr + "</p></div>"
}

activeTokenHtmlTag = {}
function updateTokenPredTrueComparisonSnapshot(snapshotDivId, tokenHtmlTag, predField){
    const snapShotDiv = document.getElementById(snapshotDivId)
    document.tokenHtmlTag = tokenHtmlTag
    document.snapShotDiv = snapShotDiv
    if( snapShotDiv!== null ){
        const trueValue = tokenHtmlTag.dataset[predField]
        const predValue = tokenHtmlTag.dataset["pred"+predField]
        console.log("updateTokenPredTrueComparisonSnapshot() predField: ", predField, ", tokenHtmlTag.dataset: ", tokenHtmlTag.dataset)

        //filling prediction part:
        let predTrueComparisonTag = ""

        if( htmlTagHasClass(tokenHtmlTag, TRUE_NEGATIVE_LABEL) ){
            predTrueComparisonTag = span(
                tokenHtmlTag.innerHTML,
                [TRUE_NEGATIVE_LABEL]
            ) + ` was <strong>correctly</strong> predicted as nothing.`
        } else if( htmlTagHasClass(tokenHtmlTag, TRUE_POSITIVE_LABEL) ){
            predTrueComparisonTag = span(
                tokenHtmlTag.innerHTML,
                [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
            ) + ` was <strong>correctly</strong> predicted to ` +
            span(predValue, [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS])
        } else if( htmlTagHasClass(tokenHtmlTag, FALSE_NEGATIVE_LABEL) ){
            predTrueComparisonTag = span(
                tokenHtmlTag.innerHTML,
                [FALSE_NEGATIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
            ) + ` was <strong>missed</strong>, should have been ` +
            span(trueValue, [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS])
        } else if( htmlTagHasClass(tokenHtmlTag, FALSE_POSITIVE_LABEL) ){
            predTrueComparisonTag = span(
                tokenHtmlTag.innerHTML,
                [FALSE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
            ) + ` was <strong>superfluously predicted</strong> to ` +
            span(predValue, [FALSE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS]) +
            `, there is nothing to see here.`
        } else if( htmlTagHasClass(tokenHtmlTag, WRONGLY_PREDICTED_POSITIVE_LABEL) ){
            predTrueComparisonTag = span(
                tokenHtmlTag.innerHTML,
                [WRONGLY_PREDICTED_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
            ) + ` was <strong>wrongly</strong> predicted to ` +
            span(predValue, [WRONGLY_PREDICTED_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS]) +
            `, should have been ` +
            span(trueValue, [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS])
        }
        if( !htmlTagHasClass(tokenHtmlTag, TRUE_NEGATIVE_LABEL) ){
            snapShotDiv.innerHTML = predTrueComparisonTag
            if(activeTokenHtmlTag[snapshotDivId]){
                activeTokenHtmlTag[snapshotDivId].classList.remove(NLP_ACTIVE_TOKEN_CLASS)
            }
            tokenHtmlTag.classList.add(NLP_ACTIVE_TOKEN_CLASS)
            activeTokenHtmlTag[snapshotDivId] = tokenHtmlTag
        }
    }

}
function visualizePredTrueComparison(predTokens, trueTokens, predField, relevantFields=[]){
    const newpredField = predField.replaceAll(/\W/ig, "x").toLowerCase()
    if( !relevantFields.includes(predField)){
        relevantFields.push(predField)
    }

    predTokens.forEach(predToken =>{
        cleanTokenPredField(predToken, predField, newpredField)
    })
    trueTokens.forEach(trueToken =>{
        cleanTokenPredField(trueToken, predField, newpredField)
    })
    
    const snapShotDivId = "nlp-token-snapshot-div-"+ Math.floor(Math.random()*100000)
    const snapShotDiv =`<div id="${snapShotDivId}" class="nlp-token-snapshot-div"></div>`
    const tokens = combinePredTrue(predTokens, trueTokens, newpredField, relevantFields)
    console.log("visualizePredTrueComparison() combined tcorrectlyokens: ", tokens)
    
    const otmo = `updateTokenPredTrueComparisonSnapshot('${snapShotDivId}', this, '${newpredField}')`
    
    relevantFields.push("pred"+newpredField)
    const contentDiv = visualizeDocument(tokens, relevantFields, onTokenMouseOver = otmo)
    console.log("visualizePredTrueComparison(), snapShotDiv: ", snapShotDiv, ", contentDiv: ", contentDiv)
    const styleTag = `<style>${CSS_AS_STRING}</style>`
    return `<div>\n`+styleTag+"\n"+snapShotDiv+"\n"+contentDiv+"</div>"
}
