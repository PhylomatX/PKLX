var apiUri = ""

var nodes, edges, network;

var instructionText = 'Click on nodes to <b>find additional relations</b>. SHIFT+click to <b>collapse nodes</b>. The green node was the starting point.'
var retrievalText = "Retrieving data. Please wait...";
var noMoreDataText = "No more data found...";

var HttpClient = function() {
    this.get = function(url, aCallback) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() { 
            if (xhr.readyState == 4 && xhr.status == 200)
                aCallback(JSON.parse(xhr.responseText));
        }
        xhr.open( "GET", url, true );            
        xhr.send( null );
    }
    this.post = function(url, body, aCallback) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() { 
            if (xhr.readyState == 4 && xhr.status == 200)
                aCallback(JSON.parse(xhr.responseText));
        }

        xhr.open( "POST", url, true );            
        xhr.setRequestHeader('Content-type', 'application/json')
        xhr.send( body );
    }
}

function start() {
    var client = new HttpClient();
    let names_box = $('#names_box');
    client.get(apiUri + "/nodes", function(response) {
          $("#names_box").select2({
              data: response
          });
          names_box.val(response[0].id);
          names_box.select2().trigger('change');
          init(response[0].id);
    });
}

function instruction() {
    document.getElementById('statement').innerHTML = noMoreDataText ;
    setTimeout(function () { document.getElementById('statement').innerHTML = instructionText }, 1000);
};

function visualise(entities, links, position) {
    for (var i = 0; i < entities.length; i++) {
        if (nodes.get(entities[i].id) == null) {
            if (position != null) {
                entities[i].x = position.x;
                entities[i].y = position.y;
            }
            nodes.add(entities[i])
        }
    }
    for (var i = 0; i < links.length; i++) {
        if (edges.get(links[i].id) == null) {
            edges.add(links[i])
        }
    }
}

function init(node) {
    draw();
    getRelated(node);
};

function getRelated(node) {
    document.getElementById('statement').innerHTML = retrievalText;
    var client = new HttpClient();
    var body = JSON.stringify({ request: node})
    endpoint = "/related";
    client.post(apiUri + endpoint, body, function(response) {
        try {
            position = network.getPositions(node)[node];
        }
        catch (err) { position = null };
        visualise(response.nodes, response.links, position);
        instruction();
    });
};

function draw() {
    nodes = new vis.DataSet([]);
    edges = new vis.DataSet([]);
    var container = document.getElementById('network');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        interaction: {
            hover: true,
            hoverConnectedEdges: true,
        },
        "edges": {
            font: {
                face: 'arial',
                color: '#FFFFFF',
                strokeWidth: 0
            },
            arrows: {
                to: {
                    enabled: true, 
                    scaleFactor: 0.25
                }
            },
            arrowStrikethrough: false,
            color : {
                inherit: false
            }
        },
        "nodes": {
            "font": {
                face: 'arial',
                color: '#FFFFFF'
            },
        },
        "physics": {
            "forceAtlas2Based": {
                "centralGravity": 0.007,
                "springConstant": 0.09,
                "damping": 0.9
            },
            "solver": "forceAtlas2Based",
            "maxVelocity": 10,
            "minVelocity": 3,
            "timestep": 0.4,
        },
        "interaction": { 
            hover: true 
        }
    };
    network = new vis.Network(container, data, options);
    network.fit();
    network.on("click", function (params) {
        if (params.nodes[0] != null) {
            if (params.event.srcEvent.shiftKey) {
                network.selectNodes([params.nodes[0]])
                network.deleteSelected()
            } else {
                getRelated(params.nodes[0]);
            }
        } 
    });
    $(document).ready(function(){
        $('#names_box').on('select2:select', function (e) {
            init($('#names_box').val())
          });

          $('#names_box').select2({
            minimumInputLength: 1
          });
    });
    $(document).on('keydown', function (event) {
        if (event.shiftKey) {
            $('#network').css('cursor', 'not-allowed');
        }
    });
    $(document).on('keyup', function (event) {
        $('#network').css('cursor', 'auto');
    });
}