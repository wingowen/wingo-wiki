from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 访问 Wiki 概念页面
    page.goto('https://wingo-wiki.netlify.app/concepts/')
    page.wait_for_load_state('networkidle')
    
    # 截图保存
    page.screenshot(path='/workspace/wiki_concepts_screenshot.png', full_page=True)
    
    # 获取页面内容
    content = page.content()
    
    # 检查页面是否包含我们添加的内容
    print("页面标题:", page.title())
    print("\n页面内容片段:")
    print(content[:1000])  # 显示前 1000 个字符
    
    # 检查是否包含我们添加的目录结构
    print("\n检查是否包含 agent-architecture:", "agent-architecture" in content)
    print("检查是否包含 claude:", "claude" in content)
    print("检查是否包含 context-engineering:", "context-engineering" in content)
    print("检查是否包含 mcp:", "mcp" in content)
    print("检查是否包含 multi-agent:", "multi-agent" in content)
    print("检查是否包含 rag:", "rag" in content)
    print("检查是否包含 tool-use:", "tool-use" in content)
    
    # 检查控制台日志
    print("\n控制台日志:")
    for entry in page.context.cookies():
        print(entry)
    
    browser.close()