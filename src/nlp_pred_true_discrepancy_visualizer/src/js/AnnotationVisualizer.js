
/**
 * Discussion 1.12.2021 12H25:
 * - is this code too complicated for my uses???
 * 
 * needs:
 * - display at token-level: predicted-true, predicted-false, unpredicted-true + labels
 * - 
 * new proposition:
 * - parse conllu files in list of js token obj
 * - functions:
 *      + visualizeDocument() shows list of tokens with html-classes
 *      + comparePredTrue() combine pred&true lists of tokens in single token list
 *      + visualizePredTrueComparison() combines both functions for the best
 * - token: unclassed JS obj with fields
 *      - text: text of token
 *      - EndOfLine: for <br/>
 *      - endOfParagraph (optional) for <p>...</p>
 * - visualizeDocument() arguments:
 *      + tokens, with visualizationHtmlClasses property
 *      + relevantFields, list of fields to display for each token
 */

function parseConlluTsv(conlluTsvStr){

}

class Annotation{
    /**
     * 
     * @param {*} start 
     * @param {*} end not inclusive
     * @param {*} mention 
     * @param {*} fields 
     */
    constructor(start, end, fields, mention=""){
        this.start = start
        this.end = end
        this.fields = fields
        this.mention = mention
    }
}


/** Sort Annotations from first to last, in place, returns annotations
 * 
 * If 2 annotations have same start, the one which ends last is placed first (for proper nesting)
 */
 function sortAnnotations(annotations, alreadySorted=false){
    if(!alreadySorted){
        annotations.sort(a,b=>b.end-a.end) // first, sort descending according to end
        annotations.sort(a,b=>a.start-b.start) // second, sort ascending according to start    
    }
    return annotations
}

/** Gives annotations nesting level, 0 being unnested, 1 being nested inside 1 other annotation, etc...
 * 
 * @param {Array[Annotation]} annotations 
 * @param {Boolean} alreadySorted whether annotations is already sorted or not 
 * @returns an array with same length as annotations with corresponding nesting levels
 */
function getAnnotationsNestingLevel(annotations, alreadySorted=false){
    sortAnnotations(annotations, alreadySorted)
    nesting_levels = (new Array(annotations.length)).fill(0)
    if(annotations.length <= 1){
        return nesting_levels
    }
    for(i=0; i<annotations.length-1; i++){
        a = annotations[i]
        for(j=i+1; j<annotations.length; j++){
            a2 = annotations[j]
            if(a2.start<a.end){
                nesting_levels[j] = nesting_levels[i]+1
            }else{
                break
            }
        }
    }
    return nesting_levels
}
class NestedAnnotation extends Annotation{
    constructor(start, end, fields, children=[], mention=""){
        super(start, end, fields, mention)
        this.children = children
    }
    static fromAnnotations(annotations, alreadySorted=false){
        sortAnnotations(annotations, alreadySorted)

    }
}

/** Returns true if any annotations overlap
 * 
 * Consecutive sorted Annotations a1 and a2 overlap if:
 * - a2.start < a1.end
 * - a2.end > a1.end
 */
function areAnnotionsOverlapping(annotations, alreadySorted=false){
    sortAnnotations(annotations, alreadySorted)
    for(i=0; i<(annotations.length-1); i++){
        a1 = annotations[i]
        a2 = annotations[i+1]
        if( (a2.start<a1.end) && (a2.end>a1.end) ){
            return true
        }
    }
    return false
}

/** Returns a string containing html visualizing the annotations in the text
 * 
 * AnnotationVisualization.css style should be added to html page for proper styling.
 * Double line returns in text (if any) are used as <p> delimitations.
 * Doesn't handle annotations overlap at the moment (nesting no problem though)
 * 
 * 
 * @param {String} text: simple str containing the text
 * @param {Array[String]} relevantFields: array of the fields to be displayed for each annotation
 * @param {Array[Annotation]} annotations: annotation, with optional field "visualizationHtmlClasses" for viz
 *   field listing extra html classes to be given to this annotation's span
 * 
 * algorithm for nested annotation:
 * - 
 */
function visualizeAnnotations(text, annotations, relevantFields){
    sortAnnotations(annotations)
    if(areAnnotionsOverlapping(annotations, true)){
        throw Error(`visualizeAnnotations() overlapping annotations not handled yet. Annotations: ${annotations}, text: ${text}`)
    }

    annotations.map(a=>{
        visHtmlClassesStr = "visualizationHtmlClasses" in a? a.visualizationHtmlClasses.join(" ") : ""
        annotationSpanStart = `<span class='${visHtmlClassesStr}'>`
        annotationSpanEnd = `</span>`


    })
}

