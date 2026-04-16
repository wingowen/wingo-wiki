// Interactive Graph for Material for MkDocs
// Based on Apache ECharts

// Create floating button immediately when script loads
(function() {
  // Create graph container
  var container = document.createElement('div');
  container.id = 'graph-container';
  container.innerHTML = '<div id="graph" style="width: 100%; height: 100%;"></div><button id="close-graph" style="position: absolute; top: 20px; right: 20px; background: #333; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 14px; z-index: 10000;">Close</button>';
  container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.95); z-index: 9999; display: none;';
  document.body.appendChild(container);

  // Create floating graph button
  var button = document.createElement('button');
  button.id = 'floating-graph-btn';
  button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
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
    initGraph();
  };

  // Close graph
  document.getElementById('close-graph').onclick = function() {
    document.getElementById('graph-container').style.display = 'none';
  };

  // Map node names to URLs
  var nodeUrlMap = {
    'AI Agent': 'entities/ai-agent/',
    'Agent Architecture': 'concepts/agent-architecture/',
    'Agent Skills': 'concepts/agent-skills/',
    'Agent Framework Theory': 'concepts/agent-framework-theory/',
    'Agent Framework Practice': 'concepts/agent-framework-practice/',
    'Building Effective Agents': 'concepts/building-effective-agents/',
    'LangGraph': 'concepts/langgraph/',
    'ReAct': 'concepts/react/',
    'Context Engineering': 'concepts/context-engineering/',
    'Context Management': 'concepts/context-management/',
    'Effective Context Engineering': 'concepts/effective-context-engineering/',
    'Dual Memory System': 'concepts/dual-memory-system/',
    'RAG': 'concepts/rag/',
    'HyDE': 'concepts/hyde/',
    'Contextual Retrieval': 'concepts/contextual-retrieval/',
    'MCP': 'concepts/mcp/',
    'MCP Deep Dive': 'concepts/mcp-deep-dive/',
    'MCP Code Execution': 'concepts/mcp-code-execution/',
    'Multi-Agent': 'concepts/multi-agent/',
    'Multi-Agent Research': 'concepts/multi-agent-research/',
    'Claude Code': 'entities/claude-code/',
    'Claude Agent SDK': 'concepts/claude-agent-sdk/',
    'Claude Code Best Practices': 'concepts/claude-code-best-practices/',
    'Claude Desktop Extensions': 'concepts/claude-desktop-extensions/',
    'Claude Postmortem': 'concepts/claude-postmortem/',
    'Anthropic': 'entities/anthropic/',
    'Tool Use': 'concepts/tool-use/',
    'Advanced Tool Use': 'concepts/advanced-tool-use/',
    'Writing Effective Tools': 'concepts/writing-effective-tools/',
    'Think Tool': 'concepts/think-tool/',
    'Slash Commands': 'concepts/slash-commands/',
    'Beyond Permission Prompts': 'concepts/beyond-permission-prompts/',
    'Long Running Agents': 'concepts/long-running-agents/',
    'Prompt Injection': 'concepts/prompt-injection/',
    'SWE Bench': 'concepts/swe-bench/'
  };

  // Initialize graph function
  function initGraph() {
    if (typeof echarts !== 'undefined') {
      var myChart = echarts.init(document.getElementById('graph'));

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
            data: [
              {name: 'AI Agent', symbolSize: 50, category: 0, itemStyle: {color: '#ef4444'}},
              {name: 'Agent Architecture', symbolSize: 45, category: 0, itemStyle: {color: '#ef4444'}},
              {name: 'Agent Skills', symbolSize: 30, category: 0, itemStyle: {color: '#ef4444'}},
              {name: 'Building Effective Agents', symbolSize: 25, category: 0, itemStyle: {color: '#ef4444'}},
              {name: 'Long Running Agents', symbolSize: 25, category: 0, itemStyle: {color: '#ef4444'}},
              {name: 'LangGraph', symbolSize: 40, category: 1, itemStyle: {color: '#f97316'}},
              {name: 'ReAct', symbolSize: 35, category: 1, itemStyle: {color: '#f97316'}},
              {name: 'Context Engineering', symbolSize: 40, category: 2, itemStyle: {color: '#eab308'}},
              {name: 'Context Management', symbolSize: 35, category: 2, itemStyle: {color: '#eab308'}},
              {name: 'Effective Context Engineering', symbolSize: 25, category: 2, itemStyle: {color: '#eab308'}},
              {name: 'Dual Memory System', symbolSize: 30, category: 2, itemStyle: {color: '#eab308'}},
              {name: 'RAG', symbolSize: 40, category: 3, itemStyle: {color: '#22c55e'}},
              {name: 'HyDE', symbolSize: 30, category: 3, itemStyle: {color: '#22c55e'}},
              {name: 'Contextual Retrieval', symbolSize: 25, category: 3, itemStyle: {color: '#22c55e'}},
              {name: 'MCP', symbolSize: 45, category: 4, itemStyle: {color: '#06b6d4'}},
              {name: 'MCP Deep Dive', symbolSize: 35, category: 4, itemStyle: {color: '#06b6d4'}},
              {name: 'MCP Code Execution', symbolSize: 30, category: 4, itemStyle: {color: '#06b6d4'}},
              {name: 'Multi-Agent', symbolSize: 35, category: 5, itemStyle: {color: '#3b82f6'}},
              {name: 'Multi-Agent Research', symbolSize: 30, category: 5, itemStyle: {color: '#3b82f6'}},
              {name: 'Claude Code', symbolSize: 35, category: 6, itemStyle: {color: '#8b5cf6'}},
              {name: 'Claude Agent SDK', symbolSize: 30, category: 6, itemStyle: {color: '#8b5cf6'}},
              {name: 'Claude Code Best Practices', symbolSize: 25, category: 6, itemStyle: {color: '#8b5cf6'}},
              {name: 'Claude Desktop Extensions', symbolSize: 25, category: 6, itemStyle: {color: '#8b5cf6'}},
              {name: 'Claude Postmortem', symbolSize: 25, category: 6, itemStyle: {color: '#8b5cf6'}},
              {name: 'Anthropic', symbolSize: 40, category: 7, itemStyle: {color: '#ec4899'}},
              {name: 'Tool Use', symbolSize: 35, category: 8, itemStyle: {color: '#64748b'}},
              {name: 'Advanced Tool Use', symbolSize: 25, category: 8, itemStyle: {color: '#64748b'}},
              {name: 'Writing Effective Tools', symbolSize: 25, category: 8, itemStyle: {color: '#64748b'}},
              {name: 'Think Tool', symbolSize: 20, category: 8, itemStyle: {color: '#64748b'}},
              {name: 'Slash Commands', symbolSize: 20, category: 8, itemStyle: {color: '#64748b'}},
              {name: 'Beyond Permission Prompts', symbolSize: 20, category: 8, itemStyle: {color: '#64748b'}},
              {name: 'Prompt Injection', symbolSize: 20, category: 9, itemStyle: {color: '#94a3b8'}},
              {name: 'SWE Bench', symbolSize: 20, category: 9, itemStyle: {color: '#94a3b8'}}
            ],
            links: [
              {source: 'AI Agent', target: 'Agent Architecture'},
              {source: 'AI Agent', target: 'Agent Skills'},
              {source: 'AI Agent', target: 'Building Effective Agents'},
              {source: 'AI Agent', target: 'Long Running Agents'},
              {source: 'AI Agent', target: 'LangGraph'},
              {source: 'AI Agent', target: 'ReAct'},
              {source: 'AI Agent', target: 'RAG'},
              {source: 'AI Agent', target: 'MCP'},
              {source: 'AI Agent', target: 'Multi-Agent'},
              {source: 'AI Agent', target: 'Tool Use'},
              {source: 'Agent Architecture', target: 'LangGraph'},
              {source: 'Agent Architecture', target: 'ReAct'},
              {source: 'Agent Skills', target: 'Tool Use'},
              {source: 'Agent Skills', target: 'Writing Effective Tools'},
              {source: 'Building Effective Agents', target: 'Agent Architecture'},
              {source: 'Building Effective Agents', target: 'Agent Skills'},
              {source: 'Long Running Agents', target: 'Context Management'},
              {source: 'Context Engineering', target: 'Context Management'},
              {source: 'Context Engineering', target: 'Effective Context Engineering'},
              {source: 'Context Engineering', target: 'Dual Memory System'},
              {source: 'Context Engineering', target: 'RAG'},
              {source: 'Context Management', target: 'Dual Memory System'},
              {source: 'RAG', target: 'HyDE'},
              {source: 'RAG', target: 'Contextual Retrieval'},
              {source: 'MCP', target: 'MCP Deep Dive'},
              {source: 'MCP', target: 'MCP Code Execution'},
              {source: 'MCP', target: 'Tool Use'},
              {source: 'Multi-Agent', target: 'Multi-Agent Research'},
              {source: 'Anthropic', target: 'Claude Code'},
              {source: 'Anthropic', target: 'Claude Agent SDK'},
              {source: 'Anthropic', target: 'Claude Code Best Practices'},
              {source: 'Anthropic', target: 'Claude Desktop Extensions'},
              {source: 'Anthropic', target: 'Claude Postmortem'},
              {source: 'Anthropic', target: 'AI Agent'},
              {source: 'Claude Code', target: 'Claude Code Best Practices'},
              {source: 'Claude Code', target: 'Claude Desktop Extensions'},
              {source: 'Tool Use', target: 'Advanced Tool Use'},
              {source: 'Tool Use', target: 'Writing Effective Tools'},
              {source: 'Tool Use', target: 'Think Tool'},
              {source: 'Tool Use', target: 'Slash Commands'},
              {source: 'Tool Use', target: 'Beyond Permission Prompts'},
              {source: 'Prompt Injection', target: 'Tool Use'},
              {source: 'SWE Bench', target: 'AI Agent'}
            ],
            roam: true,
            label: {
              show: true,
              color: '#fff',
              fontSize: 11
            },
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)',
              curveness: 0.3,
              width: 2
            },
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 4,
                color: 'rgba(255, 255, 255, 0.6)'
              }
            },
            force: {
              repulsion: 600,
              edgeLength: 80,
              gravity: 0.1
            }
          }
        ]
      };

      myChart.setOption(option);

      // Handle node clicks
      myChart.on('click', function(params) {
        if (params.dataType === 'node') {
          var nodeName = params.data.name;
          var url = nodeUrlMap[nodeName];
          if (url) {
            window.location.href = '/' + url;
          }
        }
      });

      window.addEventListener('resize', function() {
        myChart.resize();
      });
    } else {
      console.log('ECharts not loaded yet, retrying...');
      setTimeout(initGraph, 500);
    }
  }
})();