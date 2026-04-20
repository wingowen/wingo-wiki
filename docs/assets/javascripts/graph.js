// Interactive Graph for Material for MkDocs
// Based on Apache ECharts

// Create floating button immediately when script loads
(function() {
  var graphData = null;
  var myChart = null;

  // Create graph container
  var container = document.createElement('div');
  container.id = 'graph-container';
  container.innerHTML = '<div id="graph" style="width: 100%; height: 100%;"></div><button id="close-graph" style="position: absolute; top: 20px; right: 20px; background: #333; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 14px; z-index: 10000;">Close</button>';
  container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.95); z-index: 9999; display: none;';
  document.body.appendChild(container);

  // Create floating graph button
  var button = document.createElement('button');
  button.id = 'floating-graph-btn';
  button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21 3 6"></polygon><line x1="9" y1="3" x2="9" y2="18"></line><line x1="15" y1="6" x2="15" y2="21"></line></svg>';
  button.title = 'Open Knowledge Graph';
  button.style.cssText = 'position: fixed; bottom: 30px; right: 30px; width: 56px; height: 56px; border-radius: 50%; background: #4f46e5; color: white; border: none; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4); cursor: pointer; z-index: 9998; display: flex; align-items: center; justify-content: center; transition: transform 0.2s, box-shadow 0.2s;';
  
  // Button hover effect
  button.onmouseover = function() {
    this.style.transform = 'scale(1.1)';
    this.style.boxShadow = '0 6px 16px rgba(79, 70, 229, 0.5)';
  };
  button.onmouseout = function() {
    this.style.transform = 'scale(1)';
    this.style.boxShadow = '0 4px 12px rgba(79, 70, 229, 0.4)';
  };
  
  document.body.appendChild(button);

  // Open graph
  button.onclick = function() {
    document.getElementById('graph-container').style.display = 'block';
    loadGraphData();
  };

  // Close graph
  document.getElementById('close-graph').onclick = function() {
    document.getElementById('graph-container').style.display = 'none';
  };

  // Category colors
  var categoryColors = [
    '#ef4444', '#f97316', '#eab308', '#22c55e', '#06b6d4', 
    '#3b82f6', '#8b5cf6', '#ec4899', '#64748b', '#94a3b8'
  ];

  // Load graph data from JSON
  function loadGraphData() {
    if (graphData) {
      initGraph();
      return;
    }

    fetch('/assets/graph-data.json')
      .then(response => response.json())
      .then(data => {
        graphData = data;
        console.log('[WikiGraph] Loaded graph data:', data.nodes.length, 'nodes,', data.links.length, 'links');
        initGraph();
      })
      .catch(error => {
        console.error('[WikiGraph] Failed to load graph data:', error);
        loadFallbackGraph();
      });
  }

  // Fallback to static data if dynamic data fails
  function loadFallbackGraph() {
    graphData = {
      nodes: [
        {name: 'AI Agent', url: 'entities/ai-agent/', category: 0},
        {name: 'Agent Architecture', url: 'concepts/agent-architecture/', category: 0},
        {name: 'RAG', url: 'concepts/rag/', category: 3},
        {name: 'MCP', url: 'concepts/mcp/', category: 4}
      ],
      links: [
        {source: 'AI Agent', target: 'Agent Architecture'},
        {source: 'AI Agent', target: 'RAG'},
        {source: 'AI Agent', target: 'MCP'}
      ]
    };
    initGraph();
  }

  // Initialize graph function
  function initGraph() {
    if (typeof echarts === 'undefined') {
      console.log('ECharts not loaded yet, retrying...');
      setTimeout(initGraph, 500);
      return;
    }

    if (!graphData) {
      return;
    }

    if (myChart) {
      myChart.dispose();
    }

    myChart = echarts.init(document.getElementById('graph'));

    // Get current page path
    var currentPath = window.location.pathname;
    if (currentPath.endsWith('/')) {
      currentPath = currentPath.slice(0, -1);
    }

    var nodes = graphData.nodes.map(function(node, index) {
      var isCurrentPage = currentPath === '/' + node.url.slice(0, -1);
      
      return {
        name: node.name,
        symbolSize: isCurrentPage ? 60 : 30,
        category: node.category,
        itemStyle: {
          color: isCurrentPage ? categoryColors[node.category % categoryColors.length] : 'rgba(100, 100, 100, 0.6)',
          opacity: isCurrentPage ? 1 : 0.6
        },
        emphasis: {
          itemStyle: {
            color: categoryColors[node.category % categoryColors.length],
            opacity: 1
          }
        },
        url: node.url
      };
    });

    var option = {
      title: {
        text: 'Wingo Wiki Knowledge Graph',
        left: 'center',
        top: 20,
        textStyle: {
          color: '#fff',
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          if (params.dataType === 'node') {
            return '<div style="font-weight: bold;">' + params.data.name + '</div><div style="font-size: 12px; color: #aaa;">Click to open</div>';
          }
          return params.data.name;
        },
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        borderColor: '#4f46e5',
        borderWidth: 1
      },
      series: [
        {
          type: 'graph',
          layout: 'force',
          data: nodes,
          links: graphData.links,
          roam: true,
          label: {
            show: true,
            color: '#fff',
            fontSize: 11
          },
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.6)',
            curveness: 0.3,
            width: 1.5,
            opacity: 0.8
          },
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 3,
              color: 'rgba(255, 255, 255, 0.9)',
              opacity: 1
            }
          },
          force: {
            repulsion: 300,
            edgeLength: 150,
            gravity: 0.2,
            layoutAnimation: true
          },
        }
      ]
    };

    myChart.setOption(option);

    // Handle node clicks
    myChart.on('click', function(params) {
      if (params.dataType === 'node' && params.data.url) {
        window.location.href = '/' + params.data.url;
      }
    });

    window.addEventListener('resize', function() {
      if (myChart) {
        myChart.resize();
      }
    });
  }
})();