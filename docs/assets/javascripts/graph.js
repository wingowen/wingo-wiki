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
      .then(function(response) { return response.json(); })
      .then(function(data) {
        graphData = data;
        console.log('[WikiGraph] Loaded:', data.nodes.length, 'nodes,', data.links.length, 'links');
        console.log('[WikiGraph] Sample links:', JSON.stringify(data.links.slice(0, 3)));
        initGraph();
      })
      .catch(function(error) {
        console.error('[WikiGraph] Load failed:', error);
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
    console.log('[WikiGraph] initGraph called, echarts:', typeof echarts);

    if (typeof echarts === 'undefined') {
      console.log('[WikiGraph] ECharts not ready, retrying...');
      var _t = setTimeout(initGraph, 500);
      return;
    }

    if (!graphData) {
      console.log('[WikiGraph] No graphData!');
      return;
    }

    console.log('[WikiGraph] Building chart with', graphData.links.length, 'links');

    if (myChart) {
      myChart.dispose();
    }

    myChart = echarts.init(document.getElementById('graph'));

    // Get current page path
    var currentPath = window.location.pathname;
    if (currentPath.endsWith('/')) {
      currentPath = currentPath.slice(0, -1);
    }

    // Build nodes array with name-based linking
    var nodes = graphData.nodes.map(function(node) {
      var isCurrentPage = currentPath === '/' + node.url.slice(0, -1);
      return {
        name: node.name,
        symbolSize: isCurrentPage ? 60 : 30,
        category: node.category,
        itemStyle: {
          color: isCurrentPage ? categoryColors[node.category % categoryColors.length] : categoryColors[node.category % categoryColors.length],
          opacity: isCurrentPage ? 1 : 0.7
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

    // Links must reference node names (ECharts resolves by name)
    var links = graphData.links.map(function(l) {
      return {
        source: l.source,
        target: l.target,
        lineStyle: {
          color: '#6366f1',
          width: 1,
          opacity: 0.6,
          curveness: 0.2
        }
      };
    });

    console.log('[WikiGraph] Links array sample:', JSON.stringify(links.slice(0, 2)));

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
          if (params.dataType === 'edge') {
            return params.data.source + ' → ' + params.data.target;
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
          nodes: nodes,
          links: links,
          roam: true,
          label: {
            show: true,
            color: '#fff',
            fontSize: 11,
            position: 'right'
          },
          lineStyle: {
            color: '#6366f1',
            width: 1,
            opacity: 0.6,
            curveness: 0.2
          },
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 2,
              color: '#818cf8',
              opacity: 1
            }
          },
          force: {
            repulsion: 400,
            edgeLength: 200,
            gravity: 0.1,
            alpha: 0.3,
            alphaDecay: 0.02,
            layoutAnimation: true
          },
          categories: categoryColors.map(function(c, i) { return { name: 'Category ' + i, itemStyle: { color: c } }; })
        }
      ]
    };

    console.log('[WikiGraph] Calling setOption...');
    myChart.setOption(option, true);
    console.log('[WikiGraph] setOption done');

    // Handle node clicks
    myChart.on('click', function(params) {
      console.log('[WikiGraph] Click:', params.dataType, params.data);
      if (params.dataType === 'node' && params.data.url) {
        window.location.href = '/' + params.data.url;
      }
    });

    // Log any chart errors
    myChart.on('error', function(params) {
      console.error('[WikiGraph] Chart error:', params);
    });

    window.addEventListener('resize', function() {
      if (myChart) {
        myChart.resize();
      }
    });

    // Give force layout time to settle then verify edges
    setTimeout(function() {
      console.log('[WikiGraph] Chart should now show edges. Check visually or in network tab.');
    }, 2000);
  }
})();
