

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

var TRUE_VALUE_PROP = "truevalue"
var PRED_VALUE_PROP = "predvalue"
var PRED_FIELD = "nlpComparePredTrueField"
var SNAPSHOT_DIV_CLASS = "nlp-token-snapshot-div"

// css classes for tokens
var NLP_LABELLED_TOKEN_CLASS = "nlp-labelled-token"
var NLP_ACTIVE_TOKEN_CLASS = "nlp-active-token"
var NLP_POPOVER_WRAPPER_CLASS = "popover-wrapper"
var NLP_POPOVER_CONTENT_CLASS = "popover-content"


// css classes for token prediction status
var TRUE_NEGATIVE_LABEL = "true-negative"
var TRUE_POSITIVE_LABEL = "true-positive"
var FALSE_NEGATIVE_LABEL = "false-negative"
var FALSE_POSITIVE_LABEL = "false-positive"
var WRONGLY_PREDICTED_POSITIVE_LABEL = "wrongly-predicted-positive"
var NLP_STATUS_LABELS = [
    TRUE_NEGATIVE_LABEL, TRUE_POSITIVE_LABEL, FALSE_NEGATIVE_LABEL, FALSE_POSITIVE_LABEL, WRONGLY_PREDICTED_POSITIVE_LABEL
]

function checkTokensAreIdentical(tokens1, tokens2){
    if(tokens1.length != tokens2.length){ return false }
    for(let i=0; i<tokens1.length; i++){
        if(tokens1[i].text != tokens2[i].text){ return false }
    }
    return true
}

function cleanTokenPredField(token, predField){
    if(token[predField]=="" || token[predField]=="-"){
        return undefined
    }
    return token[predField]
}

/** Combines True and prediction token in a single list.
 * 
 * Adds prediction class to "visualizationHtmlClasses" property of true tokens with possible values:
 * - true-positive: correct prediction
 * - false-positive: prediction on a non-entity token
 * - wrongly-predicted-positive: wrong prediction on an entity-token
 * - false-negative: predicted nothing on an entity-token
 */
function combinePredTrue(predTokens, trueTokens, predField){
    if( !checkTokensAreIdentical(predTokens, trueTokens) ){
        throw Error(`combinePredTrue() unidentical predTokens and trueTokens\npredTokens: ${predTokens}\ntrueTokens: ${trueTokens}`)
    }
    
    const newTokens = trueTokens.map((trueToken,i)=>{
        let predToken = predTokens[i]
        const newToken = {
            "text": trueToken.text,
            "pred": predToken,
            "true": trueToken,
            "predvalue": cleanTokenPredField(predToken, predField),
            "truevalue": cleanTokenPredField(trueToken, predField),
            "predictionStatus": undefined
        }

        // getting the prediction status
        if( newToken.truevalue!==undefined ){
            if( newToken.predvalue===undefined ){
                newToken.predictionStatus = FALSE_NEGATIVE_LABEL
            } else if( newToken.truevalue == newToken.predvalue ){
                newToken.predictionStatus = TRUE_POSITIVE_LABEL
            } else{
                newToken.predictionStatus = WRONGLY_PREDICTED_POSITIVE_LABEL
            }
        } else{
            if( newToken.predvalue!==undefined ){
                newToken.predictionStatus = FALSE_POSITIVE_LABEL
            } else{
                newToken.predictionStatus = TRUE_NEGATIVE_LABEL
            }
        }
        // adding prediction status to trueToken.visualizationHtmlClasses
        if( VIZ_HTML_CLASSES_PROPERTY in trueToken){
            newToken[VIZ_HTML_CLASSES_PROPERTY] = trueToken[VIZ_HTML_CLASSES_PROPERTY].map(x=>x)
            newToken[VIZ_HTML_CLASSES_PROPERTY].push(newToken.predictionStatus)
        } else{
            newToken[VIZ_HTML_CLASSES_PROPERTY] = [newToken.predictionStatus]
        }
        return newToken
    })
    return newTokens
}

function span(content, cssClasses=[], attributes={}){
    const attributesString = Object.keys(attributes).map(attr=> `${attr}="${attributes[attr]}"`).join(" ")
    const text = `<span class="${cssClasses.join(" ")}" ${attributesString}>${content}</span>`
    return text
}

function tokenToHTML(token, relevantFields=[], onMouseOver=""){
    const cssClasses = VIZ_HTML_CLASSES_PROPERTY in token? token[VIZ_HTML_CLASSES_PROPERTY] : []
    const attributes = {
        "onmouseover": onMouseOver
    }
    relevantFields.forEach(f => {
        attributes[`data-${f}`] = token[f]
    })


    if(!cssClasses.includes(TRUE_NEGATIVE_LABEL)){
        cssClasses.push(NLP_LABELLED_TOKEN_CLASS)

        //attributes[`data-token`] = JSON.stringify(token).replaceAll('"', "'")
    }
    //const popoverStr = getPredTrueComparisonTag(predValue, trueValue, nlpStatus, tokenText)
    // dataString = relevantFields.map(f => `data-${f}="${token[f]}"`).join(" ")
    // ending = token[END_OF_PARAGRAPH_PROPERTY]? "</p>\n<p>" : (token[END_OF_LINE_PROPERTY]? "<br/>" : " ")
    // text = `<span class="${cssClasses}" ${dataString} onmouseover="${onMouseOver}">${token.text}</span>`+ending
    const tokenStr = span(token.text, cssClasses, attributes)
    //console.log("tokenToHTML() token:", token, ", tokenStr: ", tokenStr)
    return tokenStr
}


var globalTokens = []
var GLOBAL_TOKENS_INDEX_PROP = "globaltokensindex"
function addGlobalTokens(tokens){
    let newGlobalTokensStart = globalTokens.length
    globalTokens = globalTokens.concat(tokens)
    console.log("addGlobalTokens() new globalTokens: ", globalTokens)
    for(let i = newGlobalTokensStart; i<globalTokens.length; i++){
        globalTokens[i][GLOBAL_TOKENS_INDEX_PROP] = i
    }
}

/**
 * 
 * @param {*} tokens 
 * @param {*} relevantFields 
 */
function visualizeDocument(tokens, relevantFields=[], onTokenMouseOver = ""){
    addGlobalTokens(tokens)
    relevantFields.push(GLOBAL_TOKENS_INDEX_PROP)
    const tokensStr = tokens.map(t=> tokenToHTML(t, relevantFields, onTokenMouseOver)).join("\n")
    //console.log("visualizeDocument(), tokensStr: ", tokensStr)
    return "<div class='nlp-content-div'><p>" + tokensStr + "</p></div>"
}

function getNlpStatus(tokenHtmlTag){
    return NLP_STATUS_LABELS.find(label => tokenHtmlTag.classList.contains(label))
}

function getPredTrueComparisonTag(predValue, trueValue, nlpStatus, tokenText){
    let predTrueComparisonTag = ""

    if( nlpStatus == TRUE_NEGATIVE_LABEL ){
        predTrueComparisonTag = span(
            tokenText,
            [TRUE_NEGATIVE_LABEL]
        ) + ` was <strong>correctly</strong> predicted as nothing.`
    } else if( nlpStatus == TRUE_POSITIVE_LABEL ){
        predTrueComparisonTag = span(
            tokenText,
            [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
        ) + ` was <strong>correctly</strong> predicted to ` +
        span(predValue, [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS])
    } else if( nlpStatus == FALSE_NEGATIVE_LABEL ){
        predTrueComparisonTag = span(
            tokenText,
            [FALSE_NEGATIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
        ) + ` was <strong>missed</strong>, should have been ` +
        span(trueValue, [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS])
    } else if( nlpStatus == FALSE_POSITIVE_LABEL ){
        predTrueComparisonTag = span(
            tokenText,
            [FALSE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
        ) + ` was <strong>superfluously predicted</strong> to ` +
        span(predValue, [FALSE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS]) +
        `, there is nothing to see here.`
    } else if( nlpStatus == WRONGLY_PREDICTED_POSITIVE_LABEL ){
        predTrueComparisonTag = span(
            tokenText,
            [WRONGLY_PREDICTED_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS, NLP_ACTIVE_TOKEN_CLASS]
        ) + ` was <strong>wrongly</strong> predicted to ` +
        span(predValue, [WRONGLY_PREDICTED_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS]) +
        `, should have been ` +
        span(trueValue, [TRUE_POSITIVE_LABEL, NLP_LABELLED_TOKEN_CLASS])
    }
    return predTrueComparisonTag
}

function getPredTrueRelevantFieldsTableHtml(predTrueToken, relevantFields){
    console.log("getPredTrueRelevantFieldsTableHtml() predTrueToken: ",predTrueToken,", relevantFields: ", relevantFields)
    if( relevantFields.length==0 ){
        return ""
    }
    return "<table>"+relevantFields.map(rf => "<tr>"+
            "<td><strong>"+rf+":</strong></td>"+
            "<td class='relevant-field-true'>"+predTrueToken.true[rf]+"</td>"+
            "<td class='relevant-field-pred'>(pred: "+predTrueToken.pred[rf]+")</td>"+"</tr>"
    ).join("\n")+"</table>"
}

var activeTokenHtmlTag = {}
function updateTokenPredTrueComparisonSnapshot(snapshotDivId, tokenHtmlTag, relevantFields=[]){
    console.log("updateTokenPredTrueComparisonSnapshot() relevantFields: ", relevantFields, ", tokenHtmlTag.dataset: ", tokenHtmlTag.dataset, ", tokenHtmlTag.dataset[GLOBAL_TOKENS_INDEX_PROP]: ", tokenHtmlTag.dataset[GLOBAL_TOKENS_INDEX_PROP], ", token: ", globalTokens[tokenHtmlTag.dataset[GLOBAL_TOKENS_INDEX_PROP]])
    if( !tokenHtmlTag.classList.contains(TRUE_NEGATIVE_LABEL) ){
        const snapShotDiv = document.getElementById(snapshotDivId)
        if( snapShotDiv!== null ){
            const token = globalTokens[tokenHtmlTag.dataset[GLOBAL_TOKENS_INDEX_PROP]]
            //console.log("updateTokenPredTrueComparisonSnapshot() tokenHtmlTag.dataset: ", tokenHtmlTag.dataset)

            //console.log("updateTokenPredTrueComparisonSnapshot() parsed tokenHtmlTag.dataset[token]", JSON.parse(tokenHtmlTag.dataset["token"].replaceAll("'", '"')))
            //filling prediction part:
            
            //snapShotDiv.innerHTML = getPredTrueComparisonTag(tokenHtmlTag, PRED_FIELD)
            const predValue = token.predvalue
            const trueValue = token.truevalue
            const predTrueComparisonTag = getPredTrueComparisonTag(predValue, trueValue, getNlpStatus(tokenHtmlTag), token.text)
            snapShotDiv.innerHTML = predTrueComparisonTag
            if(activeTokenHtmlTag[snapshotDivId]){
                activeTokenHtmlTag[snapshotDivId].classList.remove(NLP_ACTIVE_TOKEN_CLASS)
            }
            tokenHtmlTag.classList.add(NLP_ACTIVE_TOKEN_CLASS)
            if(!tokenHtmlTag.classList.contains(NLP_POPOVER_WRAPPER_CLASS)){

                const predTrueRelevantFieldsTableHtml = getPredTrueRelevantFieldsTableHtml(token, relevantFields)
                console.log("predTrueRelevantFieldsTableHtml: ", predTrueRelevantFieldsTableHtml)
                tokenHtmlTag.innerHTML = token.text +
                    getPopoverContentTag(
                        `<div class="${SNAPSHOT_DIV_CLASS}">${predTrueComparisonTag}</div>`+
                        predTrueRelevantFieldsTableHtml
                    )
                tokenHtmlTag.classList.add(NLP_POPOVER_WRAPPER_CLASS)
            }
            activeTokenHtmlTag[snapshotDivId] = tokenHtmlTag
        }
    }

}

function getPopoverContentTag(content){
    return `<div class="${NLP_POPOVER_CONTENT_CLASS}">${content}</div>` 
}

function visualizePredTrueComparison(predTokens, trueTokens, predField, relevantFields=[]){

    
    const snapShotDivId = "nlp-token-snapshot-div-"+ Math.floor(Math.random()*100000)
    const snapShotDiv =`<div id="${snapShotDivId}" class="${SNAPSHOT_DIV_CLASS}"></div>`
    const tokens = combinePredTrue(predTokens, trueTokens, predField)
    //console.log("visualizePredTrueComparison() combined tcorrectlyokens: ", tokens)
    
    const otmo = `updateTokenPredTrueComparisonSnapshot('${snapShotDivId}', this, ${JSON.stringify(relevantFields)})`.replaceAll('"', "'")
    console.log("visualizePredTrueComparison() updateTokenPredTrueComparisonSnapshot str: ", otmo)

    document.updateTokenPredTrueComparisonSnapshot = updateTokenPredTrueComparisonSnapshot
    const contentDiv = visualizeDocument(tokens, relevantFields, otmo)
    console.log("visualizePredTrueComparison(), snapShotDiv: ", snapShotDiv, ", contentDiv: ", contentDiv)
    const styleTag = `<style>${CSS_AS_STRING}</style>`
    return `<div>\n`+styleTag+"\n"+snapShotDiv+"\n"+contentDiv+"</div>"
}
