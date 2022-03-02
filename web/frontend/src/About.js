import React from "react";
import {CenteredLayout} from "./Layout"
import {CopyrightFooter} from "./CopyrightFooter"

export const AboutPage = (originalPageLink="")=> {
    return (
        <CenteredLayout>

            <div id="about-content">

                <p>
                    This website is a demonstration interface for a linked Historical Dictionary of Switzerland (HDS).
                    <a href="https://github.com/dddpt-epfl-phd/dhs-nerd/raw/master/reports/HDS%20Named%20Entity%20Linking%20Report.pdf">A full report for this small project is available here.</a>
                    Here is the abstract:
                </p>
                <p id="report-abstract">
                    In this work, our aim is to create a cross-linked version of the <a href="https://hls-dhs-dss.ch" rel="nofollow">the Historical Dictionary of Switzerland (HDS)</a>, a trilingual online encyclopedia on the history of Switzerland in French, German and Italian.
                    We carried out and evaluated named entity recognition and linking on the 36’000 articles of the HDS.
                    For named entity recognition and linking we used the entity-fishing tool.
                    Based on the results, we created a demonstration web interface for a cross-linked HDS in the three languages.
                    The cross-linked HDS has an average of 6 HDS links per 1000 characters against 1 HDS link in the current version of the HDS.
                    However, around 60% of entities present in the HDS cannot be linked with our approach as those entities are absent from entity-fishing’s training set, Wikipedia.
                    The cross-linked HDS demonstration interface is available here: https://dddpt-epfl-phd.github.io/dhs-nerd/. It allows for a more enticing exploration experience of the HDS.
                </p>
                <p>
                    <CopyrightFooter/>
                </p>
            </div>
        </CenteredLayout>
    )
}