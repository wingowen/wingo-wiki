import React from 'react';
import CardPreview from './components/CardPreview';
import FormInput from './components/FormInput';
import TemplateSelector from './components/TemplateSelector';
import StyleSettings from './components/StyleSettings';
import ExportOptions from './components/ExportOptions';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">个人信息卡片生成器</h1>
          <p className="text-xl text-gray-600">创建专业的个人信息卡片，轻松分享您的联系方式</p>
        </header>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 左侧编辑区 */}
          <div className="space-y-6">
            <FormInput />
            <TemplateSelector />
            <StyleSettings />
            <ExportOptions />
          </div>
          
          {/* 右侧预览区 */}
          <div className="bg-white rounded-lg shadow-md">
            <CardPreview />
          </div>
        </div>
        
        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>© 2024 个人信息卡片生成器 | 轻松创建专业的个人名片</p>
        </footer>
      </div>
    </div>
  );
};

export default App;