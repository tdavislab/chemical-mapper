let that = this;

this.side_bar = new DataLoader([], []);

// Load Resulting Mapper Graphs // 
$("#import_graph").click(function(){
    $("#graph_directory").click();
})
d3.select("#graph_directory")
    .on("change",()=>{

        let files = $('#graph_directory')[0].files;
        for(let i = 0; i<files.length;i++)
        {
            if(files[i].webkitRelativePath.includes('.json'))
            {
                filename = files[i].webkitRelativePath;
            }
        }

            $.ajax({
                type: "POST",
                url: "/mapper_data_process",
                data: filename,
                dataType:'text',
                success: function (response) {
                    res = JSON.parse(response);
                    that.graph = new Graph(res.mapper, res.col_keys, res.connected_components, res.categorical_cols, that.side_bar.other_cols, filename);
                    //that.side_bar = new DataLoader(response.columns, response.categorical_columns, response.other_columns);
                },
                error: function (error) {
                    console.log("error",error);
                    alert("Incorrect data format!");
                }
            })
            d3.select(".columns-group")
                .style("max-height","1000px")
                .style("visibility", "visible")

    })


//let folder = document.getElementById("graph_directory");
//folder.onchange=function(){
//    console.log("GG")
//    let files = folder.files;
//    that.mapper_folder_name = files[0].webkitRelativePath.split("/")[0];
//    let mapper_files = [];
//    for(let i=0;i<files.length;i+=1){
//        let filename_i = files[i].name;
//        if(filename_i.startsWith("mapper") && filename_i.endsWith(".json")){
//            mapper_files.push(filename_i)
//        }
//    }
//    console.log(mapper_files);
//    let mapper_list_container = document.getElementById("mapper-list-container-inner");
//    mapper_list_container.style.maxHeight = "450px";
    // draw sliders
//    draw_mapper_param_sliders();
    // draw dropdown meun
//    let fg = d3.select("#mapper_list_selection").selectAll("option").data(mapper_files);
//    fg.exit().remove();
//    fg = fg.enter().append("option").merge(fg)
//        .classed("select-items", true)
//        .html(d=>d);
//  }


//  d3.select("#import_graph")
//    .on("click", ()=>{
//        let mapper_list_dropdown = document.getElementById("mapper_list_selection");
//        if(mapper_list_dropdown.options){
//            let mapper_filename = mapper_list_dropdown.options[mapper_list_dropdown.selectedIndex].text;
//            $.ajax({
//                type: "POST",
//                url: "/mapper_data_process",
//                data: that.mapper_folder_name+"/"+mapper_filename,
//                dataType:'text',
//                success: function (response) {
//                    response = JSON.parse(response);
//                    console.log(response)
                    // that.graph = new Graph(response.mapper, {}, response.connected_components);
//                    that.graph = new Graph(response.mapper, response.col_keys, response.connected_components, response.categorical_cols);
                    // that.side_bar = new DataLoader(response.columns, response.categorical_columns, response.other_columns);
//                },
//                error: function (error) {
//                    console.log("error",error);
//                }
//            })
//        }
//    })

function draw_mapper_param_sliders(){
    console.log("draw sliders")
    let intervals = [10, 20, 30, 40, 50];
    let overlaps = [0.25, 0.30, 0.35];

    let width = $(d3.select("#workspace-load_result").select(".block_body-inner").node()).width();
    let height = 30;
    let margin = {"left":5, "top":15, "right":10, "bottom":15};

    let interval_scale = d3.scaleLinear()
                            // .domain([0, Math.max(Math.max(...intervals),100)])
                            .domain([0, Math.max(...intervals)+10])
                            .range([margin.left, width-margin.right]);
    let overlap_scale = d3.scaleLinear()
                            .domain([0, 0.7])
                            // .domain([0, Math.max(...overlaps)+0.1])
                            .range([margin.left, width-margin.right]);


    let interval_svg = d3.select("#mapper_interval_sliders")
        .attr("width", width)
        .attr("height", height);
    // interval 
    interval_svg.append("rect")
        .attr("rx", 3)
        .attr("ry", 3)
        .attr("x", margin.left)
        .attr("y", margin.top)
        .attr("width", width-margin.left-margin.right)
        .attr("height", 5)
        .attr("fill", "#e1e1e1")
        .attr("stroke", "#e1e1e1")
    let interval_group = interval_svg.append("g").attr("id", "interval_selection_group");
    interval_svg.append("rect")
        .attr("id", "interval_slider")
        .classed("slider_handler", true)
        .attr("x", margin.left)
        .attr("y", margin.top-3)
        .attr("width", 8)
        .attr("height", 11)
        .attr("fill", "#4CAF50")
        .attr("stroke", "#4CAF50")
        .on("mouseover", ()=>{
            d3.select("#interval_slider").classed("highlighted", true);
        })
        .on("mouseout", ()=>{
            d3.select("#interval_slider").classed("highlighted", false);
        })
        .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
    let that=this;
    function dragstarted(d) {
        that.dragStarted = true;
    }
    function dragged(d) {
        d3.select("#interval_slider").attr("x", d3.event.x);
    }
    function dragended (d) {
        let min_dist = 1000;
        let dx = d3.event.x;
        let dy = d3.event.y;
        let final_x = d3.event.x;
        let final_i = intervals[0];
        intervals.forEach(i=>{
            let dist = Math.abs(dx-interval_scale(i));
            if(dist<min_dist){
                min_dist = dist;
                final_x = interval_scale(i);
                final_i = i;
            }
        })
        d3.select("#interval_slider").attr("x", final_x+2);
        d3.select("#mapper_interval_label").html(final_i);
        that.dragStarted = false;
    }

    let ig = interval_group.selectAll("rect").data(intervals);
    ig.exit().remove();
    ig = ig.enter().append("rect").merge(ig)
        .attr("x", d=>interval_scale(d))
        .attr("y", margin.top-5)
        .attr("width",12)
        .attr("height",15)
        .attr("fill", "white")
        .attr("stroke", "grey")
        .attr("stroke-width", 2);
    

    let overlap_svg = d3.select("#mapper_overlap_sliders")
        .attr("width", width)
        .attr("height", height);
    overlap_svg.append("rect")
        .attr("rx", 3)
        .attr("ry", 3)
        .attr("x", margin.left)
        .attr("y", margin.top)
        .attr("width", width-margin.left-margin.right)
        .attr("height", 5)
        .attr("fill", "#e1e1e1")
        .attr("stroke", "#e1e1e1")
    let overlap_group = overlap_svg.append("g").attr("id", "overlap_selection_group");
    overlap_svg.append("rect")
        .attr("id", "overlap_slider")
        .classed("slider_handler", true)
        .attr("x", margin.left)
        .attr("y", margin.top-3)
        .attr("width", 8)
        .attr("height", 11)
        .attr("fill", "#4CAF50")
        .attr("stroke", "#4CAF50")
        .on("mouseover", ()=>{
            d3.select("#overlap_slider").classed("highlighted", true);
        })
        .on("mouseout", ()=>{
            d3.select("#overlap_slider").classed("highlighted", false);
        })
        .call(d3.drag()
                .on("start", ()=>{
                    this.dragStarted = true;
                })
                .on("drag", ()=>{
                    d3.select("#overlap_slider").attr("x", d3.event.x);
                })
                .on("end", ()=>{
                    let min_dist = Infinity;
                    let dx = d3.event.x;
                    let final_x = d3.event.x;
                    let final_i = overlaps[0];
                    overlaps.forEach(i=>{
                        let dist = Math.abs(dx-overlap_scale(i));
                        if(dist<min_dist){
                            min_dist = dist;
                            final_x = overlap_scale(i);
                            final_i = i;
                        }
                    })
                    d3.select("#overlap_slider").attr("x", final_x+2);
                    d3.select("#mapper_overlap_label").html(parseInt(final_i*100));
                    this.dragStarted = false;
                }));
    let og = overlap_group.selectAll("rect").data(overlaps);
    og.exit().remove();
    og = og.enter().append("rect").merge(og)
        .attr("x", d=>overlap_scale(d))
        .attr("y", margin.top-5)
        .attr("width",12)
        .attr("height",15)
        .attr("fill", "white")
        .attr("stroke", "grey")
        .attr("stroke-width", 2);


}

d3.select("#load-raw-data")
    .on("click", ()=>{
        let file_name = "3d-horse.csv";
        console.log(file_name)
        $.ajax({
            type: "POST",
            url: "/data_process",
            data: file_name,
            dataType:'text',
            success: function (response) {
                response = JSON.parse(response);
                that.side_bar = new DataLoader(response.columns, response.categorical_columns, response.other_columns);
            },
            error: function (error) {
                console.log("error",error);
                alert("Incorrect data format!");
            }
        })
        d3.select(".columns-group")
            .style("max-height","1000px")
            .style("visibility", "visible");
    })



// Load Raw Data // 
$("#import").click(function(){
    $("#files").click();
})
d3.select("#files")
    .on("change",()=>{
        let files = $('#files')[0].files[0];
        let fileReader = new FileReader();
        fileReader.onload = function(fileLoadedEvent) {
            let textFromFileLoaded = fileLoadedEvent.target.result;
            $.ajax({
                type: "POST",
                url: "/data_process",
                data: textFromFileLoaded,
                dataType:'text',
                success: function (response) {
                    response = JSON.parse(response);
                    that.side_bar = new DataLoader(response.columns, response.categorical_columns, response.other_columns);
                },
                error: function (error) {
                    console.log("error",error);
                    alert("Incorrect data format!");
                }
            })
            d3.select(".columns-group")
                .style("max-height","1000px")
                .style("visibility", "visible")
        }
        fileReader.readAsText(files, "UTF-8");
    })


d3.select("#mapper_loader")
    .on("click",()=>{
        const that = this;
        if(that.side_bar.all_cols.length>0){
            that.get_mapper_parameters();
            $.post("/mapper_loader",{
                data: JSON.stringify(that.mapper_data)
            }, function(res){
                //res = JSON.parse(res);
                that.graph = new Graph(res.mapper, res.col_keys, res.connected_components, res.categorical_cols, that.side_bar.other_cols, './CLI_examples/final.json');
                //that.graph = new Graph(res.mapper, that.side_bar.all_cols, res.connected_components, that.side_bar.categorical_cols, that.side_bar.other_cols,'./CLI_examples/final.json');
                //that.regression = new Regression(that.side_bar.all_cols);
            })
        } else{
            alert("Please import a dataset first!");
        } 
    })

d3.select("#pca")
    .on("click", ()=>{
            let that=this;
            let selected_nodes = [...that.graph.selected_nodes];
            $.post("/pca", {
                data: JSON.stringify({"nodes":selected_nodes})
            }, function(res){
                that.pca = new PCA(selected_nodes);
                that.pca.draw_PCA(JSON.parse(res.pca));
            })
        //}
    })


d3.select("#KNN")
    .on("click", ()=>{
        $.post("/knn", {
            data: JSON.stringify({"min_samples":window.side_bar.config.clustering_alg_params.min_samples})
            //dataType: 'text'
        }, function(res){
            draw_KNN(res.s_dist)  
        })
    })

function send_component(a,filename)
{
    that = this;
    a = a.toString();
    console.log(filename);

    $.ajax({
        type: "POST",
        url: "/send_component",
        data: JSON.stringify({ name: filename, component: a }),
        contentType: "application/json",

        success: function (response) {
            res = response;
            d3.select('#graphSVG').selectAll('*').remove();
            d3.select('#chemicalSVG').selectAll('*').remove();
            that.graph = new Graph(
                res[0].mapper,
                res[0].col_keys,
                res[0].connected_components,
                res[0].categorical_cols,
                that.side_bar.other_cols,
                res[1]
            );
        },

        error: function (error) {
            console.log("error", error);
            alert("Incorrect data format!");
        }
    });
}

function swap_decomposition(cur_file)
{
    that = this;
    //Let us first do stars
    console.log(cur_file);
    $.ajax({
        type: "POST",
        url: "/swap_load",
        data: cur_file,
        dataType:'text',
        success: function (response) {
            res = JSON.parse(response);
            d3.select('#graphSVG').selectAll('*').remove();
            d3.select('#chemicalSVG').selectAll('*').remove();
            that.graph = new Graph(res[0].mapper, res[0].col_keys, res[0].connected_components, res[0].categorical_cols, that.side_bar.other_cols,res[1]);
        },
        error: function (error) {
            console.log("error",error);
            alert("Incorrect data format!");
        }
    })
}

function export_pv(cur_file)
{
    that = this;
    console.log(cur_file)
    $.ajax({
        type: "POST",
        url: "/export_pv",
        data: JSON.stringify({data: that.graph.nodes,name:cur_file}),
        contentType: "application/json", 
        success: (response)=> {
            console.log("Success");
        },
        error: function (error) {
            console.log("error",error);
            alert("Incorrect data format!");
        }
    })

}

let coll  = document.getElementsByClassName("block_title");
for(let i=0; i<coll.length; i++){
    coll[i].addEventListener("click", function(){
        this.classList.toggle("collapsed")
        let block_body = this.nextElementSibling;
        console.log(block_body.id)
        if (block_body.style.maxHeight){
            block_body.style.maxHeight = null;
        } else {
            // block_body.style.maxHeight = block_body.scrollHeight + "px";
            if(block_body.id === "block_body_histogram"){
                block_body.style.maxHeight = "500px";
            } else{
                block_body.style.maxHeight = "1000px";
            }
        } 
    })
}

let filtering_para_range1 = document.getElementById("filtering-para-range1");
let filtering_range_containers1 = document.getElementsByClassName("param-range-container-inner_filtering1")
filtering_para_range1.addEventListener("click", function(){
    for(let i=0; i<filtering_range_containers1.length; i++){

        if(filtering_range_containers1[i].style.maxHeight){
            filtering_range_containers1[i].style.maxHeight = null;
        } else{
            filtering_range_containers1[i].style.maxHeight = filtering_range_containers1[i].scrollHeight + "px";
        }
    }
})

let filtering_para_range2 = document.getElementById("filtering-para-range2");
let filtering_range_containers2 = document.getElementsByClassName("param-range-container-inner_filtering2")
filtering_para_range2.addEventListener("click", function(){
    for(let i=0; i<filtering_range_containers2.length; i++){

        if(filtering_range_containers2[i].style.maxHeight){
            filtering_range_containers2[i].style.maxHeight = null;
        } else{
            filtering_range_containers2[i].style.maxHeight = filtering_range_containers2[i].scrollHeight + "px";
        }
    }
})

let clustering_para_range = document.getElementById("clustering-para-range");
let clustering_range_containers = document.getElementsByClassName("param-range-container-inner_clustering");
clustering_para_range.addEventListener("click", function(){
    for(let i=0; i<clustering_range_containers.length; i++){
        if(clustering_range_containers[i].style.maxHeight){
            clustering_range_containers[i].style.maxHeight = null;
        } else{
            clustering_range_containers[i].style.maxHeight = clustering_range_containers[i].scrollHeight + "px";
        }
    }
})



// Extendability
$.post("/module_extension",{
    data: ""
}, function(res){
    console.log(res);
    if(res.modules){
        let modules = res.modules;
        console.log(modules)
        modules.forEach(m_info => {
            let module_i = new New_Module(m_info);
            d3.select("#"+module_i.module_id+"_button")
                .on("click", ()=>{
                    console.log(module_i.module_name)
                    if(that.graph){
                        let selected_nodes = [...that.graph.selected_nodes];
                        console.log(selected_nodes);
                        $.post("/module_computing",{
                            data: JSON.stringify({"nodes":selected_nodes, "module_info": m_info})
                        }, function(res){
                            console.log(res)
                            module_i.data = res.s_dist.map(x=>+x);
                            // module_i.data = JSON.parse(res.module_result);
                            module_i.components.forEach(c=>{
                                module_i.add_component(c);
                            })
                        })
                    }
                });
        })    
    }
    
})

function get_mapper_parameters(){
    const that = this;
    if(that.side_bar.config.filter[0] === "Density"){
        that.side_bar.config.density_bandwidth = parseFloat(d3.select("#density_bandwidth_values").node().value);
        let density_kernel_dropdown = document.getElementById("density_kernel_selection");
        that.side_bar.config.density_kernel = density_kernel_dropdown.options[density_kernel_dropdown.selectedIndex].text;

    } else if(that.side_bar.config.filter[1] === "Density"){
        that.side_bar.config.density_bandwidth = parseFloat(d3.select("#density_bandwidth_values2").node().value);
        let density_kernel_dropdown = document.getElementById("density_kernel_selection2");
        that.side_bar.config.density_kernel = density_kernel_dropdown.options[density_kernel_dropdown.selectedIndex].text;
    }
    if(that.side_bar.config.filter[0] === "Eccentricity"){
        that.side_bar.config.eccent_p = parseFloat(d3.select("#eccent_p_values").node().value);
        let eccent_dist_dropdown = document.getElementById("eccent_dist_selection")
        that.side_bar.config.eccent_dist = eccent_dist_dropdown.options[eccent_dist_dropdown.selectedIndex].text;
    } else if(that.side_bar.config.filter[1] === "Eccentricity"){
        that.side_bar.config.eccent_p = parseFloat(d3.select("#eccent_p_values2").node().value);
        let eccent_dist_dropdown = document.getElementById("eccent_dist_selection2")
        that.side_bar.config.eccent_dist = eccent_dist_dropdown.options[eccent_dist_dropdown.selectedIndex].text;
    }
    that.mapper_data = {"cols":that.side_bar.selected_cols, "all_cols":that.side_bar.all_cols, "categorical_cols":that.side_bar.categorical_cols, "config":that.side_bar.config};

}


//Commented because not used in chemical mapper project.
// function get_enhanced_mapper_parameters(){
//     that.mapper_data.enhanced_config = {};
//     let ic_dropdown = document.getElementById("information_criterion_selection");
//     let ic_type = ic_dropdown.options[ic_dropdown.selectedIndex].text;
//     if(ic_type === "BIC"){
//         that.mapper_data.enhanced_config.bic = true;
//     } else {
//         that.mapper_data.enhanced_config.bic = false;
//     }
//     let max_iter = 5;
//     let delta = 0;

//     if($('#converg-iter').prop("checked")===true){
//         console.log("-----checked",d3.select("#converg-iter-value").property("value"))
//         max_iter = parseInt(d3.select("#converg-iter-value").property("value"));
//     }
//     if($('#converg-delta').prop("checked")===true){
//         delta = parseFloat(d3.select("#converg-delta-value").property("value"));
//     }

//     that.mapper_data.enhanced_config.max_iter = max_iter;
//     that.mapper_data.enhanced_config.delta = delta;

//     let sa_dropdown = document.getElementById("search_alg_selection");
//     let sa_type = sa_dropdown.options[sa_dropdown.selectedIndex].text;
//     that.mapper_data.enhanced_config.method = sa_type;
// }

//Commented because not used in chemical mapper project.
// d3.select("#enhanced_mapper_loader")
//     .on("click", ()=>{
//         if(that.side_bar.all_cols.length>0){
//             if(that.side_bar.config.filter.length>1){
//                 alert("Only 1D enhanced mapper is implemented.")
//             } else{
//                 that.get_mapper_parameters();
//                 that.get_enhanced_mapper_parameters();
//                 console.log(that.mapper_data)
//                 $.post("/enhanced_mapper_loader",{
//                     data: JSON.stringify(that.mapper_data)
//                 }, function(res){
//                     console.log(res);
//                     that.graph = new Graph(res.mapper, that.side_bar.all_cols, res.connected_components, that.side_bar.categorical_cols, that.side_bar.other_cols);
//                     that.regression = new Regression(that.side_bar.all_cols);
//                     //that.side_bar.draw_adaptive_cover(res.classic_cover, res.adaptive_cover);
//                 })
//             }
//         } else{
//             alert("Please import a dataset first!");
//         } 
//     })

//Commented because not used in chemical mapper project.
// d3.select("#linear_regression")
//     .on("click", ()=>{
//         if(that.graph){
//             let selected_nodes = [...that.graph.selected_nodes];
//             $.post("/linear_regression", {
//                 data: JSON.stringify({"nodes":selected_nodes, "dep_var":that.regression.dependent_var, "indep_vars":that.regression.indep_vars_selected})
//             }, function(res){
//                 console.log(res)
//                 that.regression.draw_reg_result(res);
//             })
//         }
//     })

//Commented because not useful in chemical mapper project.
//let label_column_dropdown = document.getElementById("label_column_selection");
// label_column_dropdown.onchange = function(){
//     let label_column = label_column_dropdown.options[label_column_dropdown.selectedIndex].text;
//     console.log(label_column)
//     if(that.graph){
//         let labels;
//         if(label_column != "row index"){
//             $.ajax({
//                 type: "POST",
//                 url: "/update_cluster_details",
//                 data: label_column,
//                 dataType:'text',
//                 success: function (response) {
//                     labels = JSON.parse(response).labels;
//                     that.graph.label_column = label_column;
//                     that.graph.labels = labels;        
//                     that.graph.text_cluster_details(that.graph.selected_nodes, label_column, labels);

//                 },
//                 error: function (error) {
//                     console.log("error",error);
//                 }
//             })
//         } else {
//             that.graph.label_column = label_column;
//             that.graph.labels = labels;  
//             that.graph.text_cluster_details(that.graph.selected_nodes, label_column, labels);
//         }
//     }
// }