import './HdsThematicIndexation.css';
import { useEffect } from "react";
//import {d3} from "d3";
import * as d3 from "d3";

const categories = [
  {name:"themes", color: "#76b7b2", active:true},
    {name:"people", color: "#59a14f", active:true},
    {name:"families", color: "#f28e2c", active:true},
    {name:"spatial", color: "#af7aa1", active:true},
]

function HdsThematicIndexation({
  treeDataJsonUrl = "./tag_tree_with_ids_all.json", // "./tag_tree_with_ids_spatial.json" // 
  baseurl = ""
}) {

  useEffect(()=>{



    // toggle show/hide children of the node
    function toggleChildrenVisible(d){
      setChildrenVisible(d, !d.childrenVisible)
    }
    function setChildrenVisible(d, value){
      d.childrenVisible = value
    }

    // toggle show/hide category statistics
    function computeCategoriesVisibleStatistics(d){
      d.visibleStatistics={}
      d.visibleTotalStatistics={}
      categories.forEach(c=>{
        d.visibleStatistics[c.name] = c.active? d.statistics[c.name] : 0
        d.visibleTotalStatistics[c.name] = c.active? d.total_statistics[c.name] : 0
      })
    }

    function computeNbVisibleArticles(d){
      return categories.map(c => d.visibleTotalStatistics[c.name]).reduce((a,b)=>a+b,0)
    }

    /** recursiveFunctionCall: applies recursiveFunc on d's children.
     * 
     * recursiveFunc should take two arguments:
     * - a node n
     * - childrenResults: an array, containing the return result of recursiveFunc on n's children (0-length array for leaves)
     */
    function recursiveFunctionCall(d, recursiveFunc){
      let childrenResult = []
      if(d.children && d.children.length>0){
        childrenResult = d.children.map(c=>recursiveFunctionCall(c, recursiveFunc))
      }
      return recursiveFunc(d, childrenResult)
    }

    // ************** Generate the tree diagram	 *****************
    const margin = {top: 20, right: 120, bottom: 20, left: 120},
      width = 960 - margin.right - margin.left,
      height = 1000 - margin.top - margin.bottom;



    let i = 0,
      duration = 750,
      root;

    const tree = d3.tree()
      .size([height, width]);

    //var diagonal = d3.svg.diagonal().projection(function(d) { return [d.y, d.x]; });
    function diagonal(d) {
      const parent = d.parent? d.parent : d
      return "M" + d.y + "," + d.x
        + "C" + (d.y + parent.y) / 2 + "," + d.x
        + " " + (d.y + parent.y) / 2 + "," + parent.x
        + " " + parent.y + "," + parent.x;
    }

    var svg = d3.select("#hds-thematic-tree")
      .attr("width", width + margin.right + margin.left)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    const nodeColorChildrenVisible = "#ffffff"
    const nodeColorChildrenHidden = "lightsteelblue"
    const nodeColorLeaf = "#4682b4"

    let currentArticlesList = null
    function setArticlesList(d){
      if(currentArticlesList!=d.data.name){
        console.log("setArticlesList for d=",d)
        const articlesList = document.getElementById("articles-list")
        let newHTML ='<h3 class="hds-thematic-title">Articles for "'+d.data.name+'"</h3>'+
          '<div class="hds-thematic-metadata">'+
            '<span>facet: '+d.data.facet+'</span><br/>'+
            (d.data.full_name?'<span>full name: '+d.data.full_name+'</span>':'')+
          '</div>'
        d.data.articles.forEach(a=>{ 
          newHTML+='<div class="dhs-article">' +
            '<a class="dhs-dhs-link " href="https://dddpt-epfl-phd.github.io/dhs-nerd/#/fr/articles/'+a[1]+'" target="_blank">'+a[0]+' ('+a[1]+')</a>' +
            '<a class="dhs-real-dhs-link" href="https://hls-dhs-dss.ch/fr/articles/'+a[1]+'" target="_blank"> <img src="'+baseurl+'/hds.png" width="15px" height="15px"></a>' +
            '</div>'
        })
        articlesList.innerHTML = newHTML
        currentArticlesList = d.data.name
      }
    }
    function getTotalStatisticAbsolute(category,d, normalize=360){
      return d.data.visibleTotalStatistics[category]/normalize // absolute value
    }
    function getTotalStatisticProportion(category,d){
      //return d.data.visibleTotalStatistics[category]/360 // absolute value
      let total = categories.map(c=>d.data.visibleTotalStatistics[c.name]).reduce((a,b)=>a+b,0)
      return d.data.visibleTotalStatistics[category]/total*100
    }
    function getTotalStatisticAsProportionFromParent(category,d){
      //return d.data.visibleTotalStatistics[category]/360 // absolute value
      const par = d.parent? d.parent : d
      let total = categories.map(c=>par.data.visibleTotalStatistics[c.name]).reduce((a,b)=>a+b,0)
      return d.data.visibleTotalStatistics[category]/total*100
    }
    function getStackedBarChartOffset(category,d, valueFunc){
      let accu = 0
      for(let c of categories){
        if(c.name==category){
          return accu
        }
        accu += valueFunc(c.name,d)
      }
    }

    function update(source) {
      const getSource = (d) => source? source : d.parent
      // Compute the new tree layout.
      let nodes = d3.hierarchy(root, d=> d.childrenVisible? d.children.filter(d=>computeNbVisibleArticles(d)>0) : null)
      nodes = tree(nodes);

        // Normalize for fixed-depth.
      nodes.each(function(d) { d.y = d.depth * 180; });

        // Update the nodes…
      var node = svg.selectAll("g.node")
        .data(nodes.descendants(), function(d) { return d.data.id || (d.data.id = ++i)});

      function nodeClass(d, extraClasses=""){
        return extraClasses +" "+ (!(d.data.children && d.data.children.length>0)? "node-leaf" : (
          d.data.childrenVisible? "node-children-visible" : "node-children-hidden"
        ))
      }

      // Enter any new nodes at the parent's previous position.
      var nodeEnter = node.enter().append("g")
        .attr("class", d => nodeClass(d, "node"))
        .attr("transform", d =>  "translate(" + getSource(d).data.y0 + "," + getSource(d).data.x0 + ")")
        .on("click", nodeClick);



        nodeEnter.append("circle")
        .attr("r", 1)

      nodeEnter.append("text")
        .attr("x", d => d.data.children && d.data.children.length>0? -13 : 13)
        .attr("dy", ".35em")
        .attr("text-anchor", d => d.data.children && d.data.children.length>0? "end" : "start")
        .text(function(d) { return d.data.name; })
        .style("fill-opacity", 1)

      const gStackedBarChartEnter = nodeEnter.append("g")
        .classed("node-stacked-bar-chart",true)
        .attr("transform", d => "translate("+ (d.data.children && d.data.children.length>0? -113 : 13)+", 5)")


      const valueFunc=getTotalStatisticAsProportionFromParent//(a,b) => getTotalStatisticAbsolute(a,b,60)
      
      for(let c of categories){
        gStackedBarChartEnter.append("rect")
          .attr("class", "stacked-bar-"+c.name)
          .attr("x",d=>getStackedBarChartOffset(c.name,d, valueFunc))
          .attr("width", d=>{
            //d.data.name=="root"? console.log("gStackedBarChartEnter for ", d.data.name, ", own: ", d.data.statistics, ", total:",d.data.total_statistics,", childrenStat: ", d.data.children_statistics, " d.data.children:", d.data.children,"getStackedBarChartOffset(category,d)=",getStackedBarChartOffset(category,d), "getStackedBarChartValue(category,d)=",getStackedBarChartValue(category,d)) :""
            return c.active? valueFunc(c.name,d) : 0
          })
          .attr("height", 6)
          .style("fill", c.color)
      }
      
      nodeEnter.transition()
        .duration(duration)
        .attr("transform", d => "translate(" + d.y + "," + d.x + ")");
      
      nodeEnter.select("circle").transition()
        .duration(duration)
        .attr("r", 10)

      // Transition nodes to their new position.
      var nodeUpdate = node.transition()
        .attr("class", d => nodeClass(d, "node"))
        .duration(duration)
        .attr("transform", d => "translate(" + d.y + "," + d.x + ")");
        
        nodeUpdate.select("circle")
        .attr("r", 10)

        nodeUpdate.select("text")
        .style("fill-opacity", 1);

      const gStackedBarChartUpdate = nodeUpdate.select(".node-stacked-bar-chart")
      for(let c of categories){
        gStackedBarChartUpdate.select(".stacked-bar-"+c.name)
          .attr("x",d=>getStackedBarChartOffset(c.name,d, valueFunc))
          .attr("width", d=>{
            //d.data.name=="root"? console.log("gStackedBarChart for ", d.data.name, ", own: ", d.data.statistics, ", total:",d.data.total_statistics,", childrenStat: ", d.data.children_statistics, " d.data.children:", d.data.children,"getStackedBarChartOffset(category,d)=",getStackedBarChartOffset(category,d), "getStackedBarChartValue(category,d)=",getStackedBarChartValue(category,d)) :""
            return c.active? valueFunc(c.name,d) : 0
          })
      }

      // Transition exiting nodes to the parent's new position.
      var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", d => "translate(" + getSource(d).y + "," + getSource(d).x + ")")
        .remove();

        nodeExit.select("circle")
        .attr("r", 1e-6);

        nodeExit.select("text")
        .style("fill-opacity", 1e-6);

      // Update the links…
      var link = svg.selectAll("path.link")
        .data(nodes.descendants().slice(1), d => d.data.id+"--"+d.parent.data.id);

      // Enter any new links at the parent's previous position.
      link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", d => diagonal({x: getSource(d).data.x0, y: getSource(d).data.y0}))
        .transition()
        .duration(duration)
        .attr("d", diagonal);

      // Transition links to their new position.
      link.transition()
        .duration(duration)
        .attr("d", diagonal);

      // Transition exiting nodes to the parent's new position.
      link.exit().transition()
        .duration(duration)
        .attr("d", d => diagonal({x: getSource(d).x, y: getSource(d).y}))
        .remove();

      // Stash the old positions for transition.
      nodes.each(function(d) {
        d.data.x0 = d.x;
        d.data.y0 = d.y;
      });
    }

    // Toggle children on click.
    function nodeClick(target, d) {
      console.log("statistics for ", d.data.name, ", own: ", d.data.statistics, ", total:",d.data.total_statistics,", childrenStat: ", d.data.children_statistics, " d.data.children:", d.data.children, "d.data.articles", d.data.articles, "d", d)
      toggleChildrenVisible(d.data)
      update(d);
      setArticlesList(d)
    }

    fetch(treeDataJsonUrl).then(resp=> resp.json()).then(treeData=>{
      console.log("fetchyfetch", treeData)
      root = treeData
      const startingSource = {
        data:{
          x0: height / 2,
          y0: 0
        }
      }

      // showing categories color legend
      const categoriesLegend = d3.select("#hds-thematic-tree-legend")
      categories.forEach( (c, i) =>{
        
        const categoryDiv = categoriesLegend.append("div")
          .attr("class","categories-legend categories-legend-"+c.name+" "+ (c.active?"":"inactive"))
        const categoryCheckbox = categoryDiv.append("input")
          .attr("type", "checkbox")
          .attr("id", "checkbox-"+c.name)
          .attr("value", c.name)
        if(c.active){
          categoryCheckbox.attr("checked", c.active)
        }
        const categoryLabel = categoryDiv.append("label")
          .attr("for", "checkbox-"+c.name)
        categoryLabel.append("span")
          .attr("class","categories-legend-square")
          .style("border-color",c.color)
        categoryLabel.append("span").text(c.name)

        categoryCheckbox.on("change", e=>{
          c.active = e.target.checked
          categoryDiv.classed("inactive",!c.active)
          recursiveFunctionCall(root, computeCategoriesVisibleStatistics)
          update()
        })
      })


      //recursiveFunctionCall(root, computeNodeStatistics)
      recursiveFunctionCall(root, computeCategoriesVisibleStatistics)
      setChildrenVisible(root, true)
      root.children.forEach(c=> recursiveFunctionCall(c, c=>setChildrenVisible(c,false)))
      recursiveFunctionCall(root, n=>{
        n.children=n.children.filter(c=>c.total_statistics.spatial+c.total_statistics.themes+c.total_statistics.people+c.total_statistics.families>0)
      })
      update(startingSource);

      //d3.select(self.frameElement).style("height", "500px");
    })
  }, [])
  return (
    <div id="container">
      <svg id="hds-thematic-tree">
      </svg>  
      <div id="hds-thematic-tree-legend">
      </div>
      <div id="articles-list">
      </div>
	  </div>
  );
}

export default HdsThematicIndexation;
