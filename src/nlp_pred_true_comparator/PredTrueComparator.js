

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



var VIZ_HTML_CLASSES_PROPERTY = "visualizationHtmlClasses"
var END_OF_LINE_PROPERTY = "EndOfLine"
var END_OF_PARAGRAPH_PROPERTY = "EndOfParagraph"

// css classes for tokens
var NLP_LABELLED_TOKEN_CLASS = "nlp-labelled-token"
var NLP_ACTIVE_TOKEN_CLASS = "nlp-active-token"

// css classes for token prediction status
var TRUE_NEGATIVE_LABEL = "true-negative"
var TRUE_POSITIVE_LABEL = "true-positive"
var FALSE_NEGATIVE_LABEL = "false-negative"
var FALSE_POSITIVE_LABEL = "false-positive"
var WRONGLY_PREDICTED_POSITIVE_LABEL = "wrongly-predicted-positive"

function checkTokensAreIdentical(tokens1, tokens2){
    if(tokens1.length != tokens2.length){ return false }
    for(let i=0; i<tokens1.length; i++){
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
    const attributesString = Object.keys(attributes).map(attr=> `${attr}="${attributes[attr]}"`).join(" ")
    const text = `<span class="${cssClasses.join(" ")}" ${attributesString}>${content}</span>`
    return text
}

function tokenToText(token, relevantFields=[], onMouseOver=""){
    const cssClasses = VIZ_HTML_CLASSES_PROPERTY in token? token[VIZ_HTML_CLASSES_PROPERTY] : []
    if(!cssClasses.includes(TRUE_NEGATIVE_LABEL)){
        cssClasses.push(NLP_LABELLED_TOKEN_CLASS)
    }
    const attributes = {
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

var activeTokenHtmlTag = {}
function updateTokenPredTrueComparisonSnapshot(snapshotDivId, tokenHtmlTag, predField){
    if( !htmlTagHasClass(tokenHtmlTag, TRUE_NEGATIVE_LABEL) ){
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
    
    document.updateTokenPredTrueComparisonSnapshot = updateTokenPredTrueComparisonSnapshot
    relevantFields.push("pred"+newpredField)
    const contentDiv = visualizeDocument(tokens, relevantFields, otmo)
    console.log("visualizePredTrueComparison(), snapShotDiv: ", snapShotDiv, ", contentDiv: ", contentDiv)
    const styleTag = `<style>${CSS_AS_STRING}</style>`
    return `<div>\n`+styleTag+"\n"+snapShotDiv+"\n"+contentDiv+"</div>"
}
