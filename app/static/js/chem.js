
//This is for the chemistry molecule
function chem_draw(hover_node,nodes)
{
    let vertices = []
    let node_index = 0

    let ids = []
    nodes.forEach(node => { ids.push(node.id)});

    node_index = ids.indexOf(hover_node);
    vertices = nodes[node_index].vertices
    vertices = vertices.toString();

    $.ajax({
        type: "POST",
        url: "/send_structure",
        data: vertices,
        dataType:'text',
        success: function (response) {
            d3.select('#chemicalSVG').selectAll('*').remove();
            response = JSON.parse(response);
            for(let i = 0; i<Object.keys(response).length-1; i++)
            {
                byteCharacters = atob(response[i]['image']);
                    byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    byteArray = new Uint8Array(byteNumbers);
                var blob = new Blob([byteArray], {'type': 'image/png'});
                var url = URL.createObjectURL(blob);
                d3.select('#chemicalSVG').append('svg:image').attr("xlink:href",url).attr('x',response[i]['group']*280).attr('y',(response[i]['vertex']*275)).attr('height',250).attr('width',250)
            }
            
        },
        error: function (error) {
            console.log("error",error);
            alert("Incorrect data format!");
        }
    })
}


function geom_draw(hover_node,nodes)
{
    let vertices = []
    let node_index = 0

    let ids = []
    nodes.forEach(node => { ids.push(node.id)});

    node_index = ids.indexOf(hover_node);
    vertices = nodes[node_index].vertices
    vertices = vertices.toString();

    $.ajax({
        type: "POST",
        url: "/send_geometry",
        data: vertices,
        dataType:'text',
        success: function (response) {
            d3.select('#chemicalSVG').selectAll('*').remove();
            response = JSON.parse(response);
            for(let i = 0; i<Object.keys(response).length-1; i++)
            {
                byteCharacters = atob(response[i]['image']);
                    byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    byteArray = new Uint8Array(byteNumbers);
                var blob = new Blob([byteArray], {'type': 'image/png'});
                var url = URL.createObjectURL(blob);
                d3.select('#chemicalSVG').append('svg:image').attr("xlink:href",url).attr('x',response[i]['group']*500).attr('y',(response[i]['vertex']*500)).attr('height',480).attr('width',480)
            }
            
        },
        error: function (error) {
            console.log("error",error);
            alert("Incorrect data format!");
        }
    })
}